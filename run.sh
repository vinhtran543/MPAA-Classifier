#!/bin/bash

# --nolist
# Does not print out filenames and predicted response

# -- info
# Prints out accuracy, precision, recall, and f-score

python3 test_splitter.py
python3 training.py Training/ movietraining.nb
python3 classifier.py movietraining.nb Testing/ --info
