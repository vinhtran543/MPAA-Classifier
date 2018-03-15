import nltk
import pickle
import sys
import os

# Checks commandline arguments are atleast 3
if(len(sys.argv) < 3):
    print("Error: Insufficient commandline arguments!")
    exit()

directory = sys.argv[1]

# Get Class Types
classes = []
for f in os.listdir(directory):
    temp = f.split('-')
    #print(temp)
    if(temp[1] == '13' or temp[1] == '17'):
        temp2 = temp[0] + '-' + temp[1]
        if not(temp2 in classes):
            classes.append(temp2)
            
    if not(temp[0] in classes):
        classes.append(temp[0])

print(classes)

model = []
fileCounter = 0
# Extract Corpuses
for c in classes:
    c_corpus = nltk.corpus.PlaintextCorpusReader(directory, c + '.*.txt')
    print(c_corpus)
    c_fd = nltk.FreqDist(c_corpus.words())
    fileCounter += 1
    model.append({'label':c, 'count':fileCounter, 'fd':c_fd})

pickle.dump(model, open(sys.argv[2], 'wb'))

print('Training Data Created:')
print('\tClasses: {0}'.format(classes))
print('\tStored: {0}'.format(sys.argv[2]))


