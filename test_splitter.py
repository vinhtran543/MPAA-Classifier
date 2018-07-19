import requests
import os
import string
from lxml import html
import random
training_dir = "Training/"
test_dir = "Testing/"
num_test = 50

# Create Testing Set

titles_in_dir = os.listdir(test_dir)
print("## Reset Testing Dir")
for i in titles_in_dir:
    os.rename(test_dir + i, training_dir + i)
    print('\t%s'%i)

print("##Creating Test Set in: " + test_dir)
all_titles = os.listdir(training_dir)
test_files = random.sample(all_titles, num_test)
for i in test_files:
    os.rename(training_dir + i, test_dir + i)
    print('\t%s'%i)
