#!/bin/bash

echo "Now Configure Env..."
brew install python3

echo "Now Configure Python Dependencies..."
pip3 install -qq setuptools
pip3 install -qq wheel
pip3 install -qq virtualenv

echo "Install python libraries"
virtualenv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
