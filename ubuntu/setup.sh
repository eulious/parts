#!/bin/bash

if [ `uname` = "Linux" ]; then
    apt update
    apt install -y python3 python3-pip python3-venv wget
    # python3 -m venv venv
    # ./venv/bin/activate
    pip install diffusers ftfy spacy ipython==7.34 transformers torch omegaconf
fi