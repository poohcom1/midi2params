#!/bin/bash

# set up a virtual environment
virtualenv -p python3.7 midi2params_env
cd midi2params_env
source bin/activate

# install some python packages
pip install ddsp==0.7.0
pip install pyyaml
pip install addict
pip install torch==1.2.0
pip install pretty_midi
python -m pip install ipykernel
git clone https://github.com/poohcom1/midi2params.git
cd midi2params
pip install -e .
# install the kernel into jupyter, so that it can be used
# in the notebook
python -m ipykernel install --user --name=midi2params_env

# get necessary data
./get_data.sh
./get_checkpoint.sh
./get_model.sh
