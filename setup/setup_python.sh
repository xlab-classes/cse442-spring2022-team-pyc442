#!/usr/bin/bash

virtualenv venv

source venv/bin/activate

pip install -r requirments.txt

deactivate
