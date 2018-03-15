import nltk
import pickle
import math
import sys
from collections import defaultdict

class_prob = {}
total_count = 0
vocab_count = 0

# Check for model file and folder location in arguments
if len(sys.argv) < 3:
    print("Needs a model and a folder argument.\n")
    sys.exit()

# Specify model on first argument, should be on same directory
model = sys.argv[1]

# Specify folder on second argument
folder = sys.argv[2]
files = ".*"

# [OPTIONAL] Specify if testing accuracy, precision, recall,
# f-score, indicated by "info" argument
info_state = sys.argv[1]

# Load movie model
model = pickle.load(open(model, "rb"))

# Sum total number of files in model
total_count = sum(c_name['count'] for c_name in model)

# Loop through all of the classes and get its log probability
# This gives the class probability
for c_name in model:
    # Probability of of this class
    prob = c_name['count'] / total_count
    # Convert to log form
    prob = math.log(prob)
    class_prob[c_name['label']] = prob

# Combine all freq dists together and get vocab size
vocab_temp = {}
for c_name in model:
    vocab_temp.update(c_name['fd'])
vocab_count = len(vocab_temp)

# Read test files from folder
reader = nltk.corpus.PlaintextCorpusReader(folder, files)

# Iterate through the files in the folder
for f in reader.fileids():
    # Get all words in the file
    words = reader.words(f)

    # Reset the score and prediction for each file
    score = defaultdict(int)
    prediction = ''

    # Iterate through the words in the file
    for w in words:
        # Iterate through each class in model
        for c_name in model:
            # Score for this class for this word
            word_cond_prob = (c_name['fd'][w] + 1) / (c_name['fd'].N() + vocab_count)
            score[c_name['label']] = score[c_name['label']] + math.log(word_cond_prob)
    
    # Combine class probability with conditional probability as
    # final score
    for c_name in score:
        score[c_name] = score[c_name] + class_prob[c_name]

    # Compare scores to see which one is highest -- final verdict
    prediction = max(score, key=score.get)

    #### For debugging ####
    print(f + " #" + prediction + "#")

# Accuracy
accuracy_correct = 0
accuracy_total = 0