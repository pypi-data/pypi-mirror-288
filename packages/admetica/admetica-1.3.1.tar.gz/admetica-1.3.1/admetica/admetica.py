import os
import joblib
import torch
import chemprop
import numpy as np
import logging
from time import time
from numpy.linalg import norm
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem
from flask import Flask, request
from io import StringIO
from admetica.constants import mean_vectors
from chemprop import data, featurizers, models
from lightning import pytorch as pl

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Path to the Models directory
MODELS_DIR = "Models"

# List of model file names
MODEL_EXTENSIONS = [
    "Caco2.ckpt", "Lipophilicity.ckpt", "Solubility.ckpt", "PPBR.ckpt", "VDss.ckpt", "CYP1A2-Inhibitor.ckpt",
    "CYP1A2-Substrate.ckpt", "CYP2C19-Inhibitor.ckpt", "CYP2C19-Substrate.ckpt", "CYP2C9-Inhibitor.ckpt",
    "CYP2C9-Substrate.ckpt", "CYP2D6-Substrate.ckpt", "CYP2D6-Inhibitor.ckpt", "CL-Hepa.ckpt", "CL-Micro.ckpt", "Half-Life.ckpt",
]

def get_model_path(model_name):
    """Get the full path for the given model name."""
    script_path = os.path.abspath(__file__)
    script_directory = os.path.dirname(script_path)
    model_file = next((file for file in MODEL_EXTENSIONS if model_name in file), None)
    if model_file:
        return os.path.join(script_directory, MODELS_DIR, model_file)
    raise ValueError(f"No matching model file found for model '{model_name}'")

def is_valid_smiles(smiles):
    """Check if the given SMILES string is valid."""
    try:
        return Chem.MolFromSmiles(smiles) is not None
    except Exception as e:
        logging.error(f"Error validating SMILES '{smiles}': {str(e)}")
        return False

def predict_chemprop(df, checkpoint_path):
    """Generate predictions using a Chemprop model."""
    model = models.MPNN.load_from_checkpoint(checkpoint_path)
    smiles_list = df['smiles']

    valid_smiles = [smi for smi in smiles_list if is_valid_smiles(smi)]
    valid_indices = [i for i, smi in enumerate(smiles_list) if is_valid_smiles(smi)]
    invalid_indices = [i for i in range(len(smiles_list)) if i not in valid_indices]

    if not valid_smiles:
        return np.full(len(smiles_list), "", dtype=object)

    test_data = [data.MoleculeDatapoint.from_smi(smi) for smi in valid_smiles]
    featurizer = featurizers.SimpleMoleculeMolGraphFeaturizer()
    test_dataset = data.MoleculeDataset(test_data, featurizer=featurizer)
    test_loader = data.build_dataloader(test_dataset, shuffle=False)

    trainer = pl.Trainer(logger=False, enable_progress_bar=True, accelerator="cpu", devices=1)
    with torch.no_grad():
        predictions = trainer.predict(model, test_loader)

    predictions = [pred.item() for batch in predictions for pred in batch]
    for index in invalid_indices:
        predictions.insert(index, "")

    return np.array(predictions, dtype=object)

def compute_fingerprint(smiles):
    """Generate a fingerprint for the given SMILES string."""
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        fingerprint = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024)
        return list(map(int, fingerprint))
    return None

def compute_similarity(mean_vector, fingerprint):
    """Compute similarity between the mean vector and fingerprint."""
    return np.dot(mean_vector, fingerprint) / (norm(mean_vector) * norm(fingerprint))

def compute_probabilities(smiles_list, model_name):
    """Calculate probabilities for each SMILES string using the Chemprop model."""
    mean_vector = mean_vectors.get(model_name)
    if not mean_vector:
        return [0.0] * len(smiles_list)

    return [
        compute_similarity(mean_vector, compute_fingerprint(smiles))
        if compute_fingerprint(smiles) else 0.0
        for smiles in smiles_list
    ]

def predict_for_model(model_name, df, include_probability):
    """Process model predictions and create a DataFrame with results."""
    model_file_path = get_model_path(model_name)
    
    if 'ckpt' in model_file_path:
        start_time = time()
        predictions = predict_chemprop(df, model_file_path)
        logging.debug(f'Chemprop prediction for {model_name} took {time() - start_time}')
        result_df = pd.DataFrame(predictions, columns=[model_name])
        if include_probability:
            probabilities = compute_probabilities(df['smiles'].tolist(), model_name)
            result_df[f'Y_{model_name}_probability'] = probabilities
    
    return result_df

def predict(file_data, model_names, include_probability, batch_size=1000):
    """Process the uploaded file data and generate predictions for the specified models."""
    model_names_list = model_names.split(",")
    result_dfs = []

    df = pd.read_csv(StringIO(file_data))
    for model_name in model_names_list:
        model_results = []
        for start_idx in range(0, len(df), batch_size):
            batch_df = df.iloc[start_idx:start_idx + batch_size]
            result_df = predict_for_model(model_name, batch_df, include_probability)
            model_results.append(result_df)
        combined_df = pd.concat(model_results, axis=0, ignore_index=True)
        result_dfs.append(combined_df)

    final_df = pd.concat(result_dfs, axis=1).loc[:, ~pd.concat(result_dfs, axis=1).columns.duplicated()]
    return final_df.to_csv(index=False)

def admetica_predict():
    """Handle file upload and generate predictions."""
    file_data = request.data
    model_names = request.args.get('models')
    include_probability = request.args.get('probability', 'false') == 'true'

    start_time = time()
    response = predict(file_data, model_names, include_probability)
    logging.debug(f'Time required: {time() - start_time}')
    return response