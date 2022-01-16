#!/bin/bash

pip install --upgrade pip
pip install -e .
pip install -r requirements.txt
python -m pytest tests/*