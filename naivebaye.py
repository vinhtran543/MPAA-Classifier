import nltk
import pickle
import sys
import os

# Checks commandline arguments are atleast 3
if(len(sys.argv) < 3):
    print("Error: Insufficient commandline arguments!")
    exit()

directory = sys.argv[1]

#Rating counters
fileCounter = 0
isPG13 = False
isNC17 = False
isG = False
isPG = False
isR = False

# Get dictionary Types
dictionary = {}
for f in os.listdir(directory):
    temp = f.split('-')
    #print(temp)
    if(temp[1] == '13' or temp[1] == '17' and (isPG13 == False or isNC17 == False)):
        temp2 = temp[0] + '-' + temp[1]     #create string PG-13 or NC-17
        #PG-13, NC-17 rating 
        #first time class initialization, give it file count 1
        if not(temp2 in dictionary):
            dict = {temp2: 1}
            dictionary.update(dict)
            if(temp[1] == '13'):
                isPG13 = True
            elif(temp[1] == '17'):
                isNC17= True
            continue
        
    #G, PG, R also no NC rating       
    #first time dictionary initialization, give it file count 1

    if((temp[1] != '13' and temp[1] != '17') and temp[0] != 'NC' and (isG == False or isPG == False or isR == False)):
        if not(temp[0] in dictionary):
            dict = {temp[0]: 1}
            dictionary.update(dict)
            if(temp[0] == 'G'):
                isG = True
            elif(temp[0] == 'PG'):
                isPG = True
            elif(temp[0] == 'R'):
                isR = True
            continue

    #update file count for dictionary labels that are already initialized
    if(temp[0] == 'G'):
        dictionary[temp[0]] += 1
    elif(temp[0] == 'PG' and temp[1] != '13'):
        dictionary[temp[0]] += 1
    elif(temp[0] == 'R'):
        dictionary[temp[0]] += 1
    elif(temp[1] == '13'):
        temp2 = temp[0] + '-' + temp[1]
        dictionary[temp2] += 1
    elif(temp[1] == '17'):
        temp2 = temp[0] + '-' + temp[1]
        dictionary[temp2] += 1

print(dictionary)

model = []
# Extract Corpuses
for c in dictionary:
    c_corpus = nltk.corpus.PlaintextCorpusReader(directory, c + '.*.txt')
    print(c_corpus)
    c_fd = nltk.FreqDist(c_corpus.words())

    #initialize fileCounter to hold the corresponding label file counts
    if(dictionary[c] == 'G'):
        fileCounter = dictionary[c]
    if(dictionary[c] == 'PG'):
        fileCounter = dictionary[c]
    if(dictionary[c] == 'PG-13'):
        fileCounter = dictionary[c]
    if(dictionary[c] == 'NC-17'):
        fileCounter = dictionary[c]
    if(dictionary[c] == 'R'):
        fileCounter = dictionary[c]
        
    model.append({'label':c, 'count':fileCounter, 'fd':c_fd})

pickle.dump(model, open(sys.argv[2], 'wb'))
print('Training Data Created:')
print('\tClasses: {0}'.format(dictionary))
print('\tStored: {0}'.format(sys.argv[2]))


