#!/usr/bin/env sh

pip install --upgrade pip
pip install -r requirements.txt
python --default-timeout=1000 -m spacy download en
