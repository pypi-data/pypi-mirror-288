# Admetica

Admetica is a command-line tool for making ADMET (Absorption, Distribution, Metabolism, Excretion, and Toxicity) predictions using pre-trained models. This tool is part of the Admetica [project](https://github.com/datagrok-ai/admetica), which aims to improve ADMET prediction tools through a global, open-source collaboration.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Predicting](#predicting)

## Installation

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chemprop)](https://badge.fury.io/py/chemprop)
[![Chemprop PyPI version](https://badge.fury.io/py/chemprop.svg)](https://badge.fury.io/py/chemprop)

Admetica is a powerful tool for making ADMET predictions and can be easily installed on any operating system. You can install it using pip, and optionally, you can set up a conda environment for better package management.

#### Creating a Conda Environment (Optional)

To create a new conda environment and install Admetica, use the following commands:

```bash
conda create --name admetica-env python=3.11
conda activate admetica-env
```

#### Installing Admetica

To install Admetica, run:

```bash
pip install admetica==1.3
```

By default, the pip installation will include all necessary dependencies for making ADMET predictions.

## Usage

### Predicting

Admetica provides a command-line interface to make predictions. To use it, run:

```bash
admetica_predict \
    --dataset-path data.csv \
    --smiles-column smiles \
    --properties Caco2,PPBR \
    --save-path predictions.csv
```

This command assumes the presence of a file named `data.csv` with SMILES strings in the column `smiles`. In addition, you should specify the properties to be calculated (e.g. `Caco2`). The predictions will be saved to `predictions.csv`.

**Supported models are:**

<div style="display: flex; justify-content: space-between;">

<div style="width: 45%;">

- Lipophilicity
- Solubility
- Caco2
- PPBR
- VDss
- CL-Micro
- CL-Hepa
- Half-Life

</div>

<div style="width: 45%;">

- CYP1A2-Inhibitor
- CYP1A2-Substrate
- CYP2C9-Inhibitor
- CYP2C9-Substrate
- CYP2C19-Inhibitor
- CYP2C19-Substrate
- CYP2D6-Inhibitor
- CYP2D6-Substrate

</div>

</div>
