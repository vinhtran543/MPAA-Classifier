import nltk
import pickle
import math
import sys

# Specify model on first argument
# Should be on same directory
model = sys.argv[1]

# Load movie model
model = pickle.load(open(model, "rb"))

print(model)