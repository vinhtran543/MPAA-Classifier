# Run python file formatted as
# python3 classifier.py model_name.nb testing_folder_name info
# Note: info argument is optional

import nltk
import pickle
import math
import sys
from collections import defaultdict

class_prob = {}
total_count = 0
vocab_count = 0
actual_files = []
pred_files = []
info_state = ""

print()

# Check for model file and folder location in arguments
if len(sys.argv) < 3:
    print("Needs a model and a folder argument.\n")
    sys.exit()

# Specify model on first argument
model = sys.argv[1]

# Specify folder on second argument
folder = sys.argv[2]
files = ".*"

# [OPTIONAL] Specify if testing accuracy, precision, recall,
# f-score, indicated by "info" argument
if len(sys.argv) > 3:
    info_state = sys.argv[3]

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
    # Add prediction to prediction list
    pred_files.append(prediction)

    # Print prediction
    print(f + " #" + prediction + "#")

# print(model)        # Debug Info

# Print additional info if user specified
if info_state != "info":
    sys.exit()

# Construct the actual list
for f in reader.fileids():
    temp_label = ""
    # Go through each class
    for c_name in model:
        # Check if the file starts with the class name and is the largest string
        if f.startswith(c_name['label']) and c_name['label'] > temp_label:
            temp_label = c_name['label']
    # Add to actual list
    actual_files.append(temp_label)

print("\n====Accuracy====")
# Accuracy
accuracy_correct = 0
accuracy_total = 0
for i, f_a in enumerate(actual_files):
    # print(f_a + " --> " + pred_files[i])      # Debug info
    if f_a == pred_files[i]:
        accuracy_correct += 1
    accuracy_total += 1
accuracy = accuracy_correct / accuracy_total
print("Accuracy: " + str(accuracy))
print(str(accuracy_correct) + " out of " + str(accuracy_total))

# Loop through all the classes for precision, recall, and f-score
for c_name in model:
    print("\n====" + c_name['label'] + " Precision, Recall, F-Score====")
    # Precision
    precision_correct = 0
    precision_total = 0
    precision = 0
    for i, f_p in enumerate(pred_files):
        if c_name['label'] == f_p:
            if f_p == actual_files[i]:
                precision_correct += 1
            precision_total += 1
    if precision_total == 0:
        print("Invalid Precision")
    else:
        precision = precision_correct / precision_total
        print("Precision: " + str(precision))
        print(str(precision_correct) + " out of " + str(precision_total))

    # Recall
    recall_correct = 0
    recall_total = 0
    recall = 0
    for i, f_a in enumerate(actual_files):
        if c_name['label'] == f_a:
            if f_a == pred_files[i]:
                recall_correct += 1
            recall_total += 1
    if recall_total == 0:
        print("\nInvalid Recall")
    else:
        recall = recall_correct / recall_total
        print("\nRecall: " + str(recall))
        print(str(recall_correct) + " out of " + str(recall_total))

    # F-Score
    if (precision + recall) == 0:
        print("\nInvalid F-Score")
    else:
        fscore = (2 * precision * recall) / (precision + recall)
        print("\nF-Score: " + str(fscore))