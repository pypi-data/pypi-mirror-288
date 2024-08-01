import argparse
import pandas as pd
from io import StringIO
from admetica.admetica import predict

def main():
    parser = argparse.ArgumentParser(description="Admetica CLI Tool")
    parser.add_argument('--dataset-path', required=True, help='Path to the dataset CSV file')
    parser.add_argument('--smiles-column', required=True, help='Column name containing SMILES strings')
    parser.add_argument('--properties', nargs='+', required=True, help='List of properties to predict')
    #parser.add_argument('--include-probability', action='store_true', help='Include probability of being in applicability domain')
    parser.add_argument('--save-path', default='predictions.csv', help='Path to save the predictions CSV file')

    args = parser.parse_args()

    df = pd.read_csv(args.dataset_path)

    if args.smiles_column not in df.columns:
        print(f"Error: Specified SMILES column '{args.smiles_column}' not found in dataset.")
        return

    df = df[[args.smiles_column]]
    file_data = df.to_csv(index=False)
    properties_str = ','.join(args.properties)

    result_csv = predict(file_data, properties_str, include_probability=False)

    with open(args.save_path, 'w') as output_file:
        output_file.write(result_csv)
    
    print(f"Predictions saved to {args.save_path}")

if __name__ == "__main__":
    main()