#!/bin/bash
export PYTHONPATH=`pwd`
export EXPERIMENTS_SUBPATH=openml

python bin/load_data/download_data_from_openml.py
python bin/load_data/preprocess_data.py
python bin/metatrain_preparation/perform_hpo_on_all_datasets.py