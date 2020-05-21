import sys
import os.path
from os import path
import json
import itertools

# set vars
dict1 = "./dictionary.txt" # path to original dictionary
dict2 = "./newdict.json" # path where sorted dictionary will be saved
askend = "no" # flag for ending loop

# Function to generate a new dictionary
def updatedict():
    newdict = {}
    with open(dict1) as f:
        for line in f:
            word = line.strip()
            chars = zipsort(word)
            newdict[chars.lower()] = word

    with open(dict2,"w") as f:
        json.dump(newdict,f, sort_keys=True, separators=(',', ': '))

# Function to sort a string alphabetically and compress it
def zipsort(raw):
    zipped = ""
    count = 1
    word = sorted(raw.strip())
    zipped += word[0]
    for i in range(len(word)-1):
        if(word[i] == word[i+1]): # count while it lasts
            count += 1
        else: # stop counting
            if(count > 1):
                zipped += str(count)
            zipped += word[i+1]
            count = 1
    if(count > 1):
        zipped += str(count)
    return zipped

# Function to generate all combinations
def wordsoup(raw):
    raw = raw.strip()
    raw = raw.lower()
    combinations = []
    pretty = []
    for i in range(1, len(raw)+1): # try for each length
        combi = [list(x) for x in itertools.combinations(raw,i)]
        combinations.extend(combi)
    for blob in combinations:
        string = zipsort("".join(sorted(blob)))
        pretty.append(string)
    return list(set(sorted(pretty)))

# Function to calculate the score for a word on icanhazwords
def wordscore(raw):
    three = ["j","k","q","x","z"]
    two = ["c","f","h","l","m","p","v","w","y"]
    score = 0
    prev = 0
    for char in raw:
        if char.isnumeric() == True: # for dupes
            mult = int(char)
            score += prev * (mult-1)
        elif char in three: # normal score counting
            score += 3
            prev = 3
        elif char in two:
            score += 2
            prev = 2
        else:
            score += 1
            prev = 1
    score = score**2
    return score

# Start command dialogue
if(path.exists(dict2)): # if the dictionary exists, check if it should be updated
    askupdate = input("Update dictionary? (y/n)")
    if (askupdate == "y"):
        updatedict()
        print("Dictionary Updated!")
else: # forcibly update the dictionary if it doesn't exist
    updatedict()
with open(dict2) as f:
    dictionary = json.load(f)
askflex = input("Allow partial matches? (y/n)")
while askend != "y":
    asksearch = input("What alphabets do you want to use?")
    if(askflex == "y"): # flexible search
        soup = wordsoup(asksearch)
        score = 0 # default score
        word = ""
        for search in soup:
            if search in dictionary:
                newscore = wordscore(search)
                if newscore > score:
                    score = newscore
                    word = dictionary[search]
        if word == "":
            print("No word found!")
        else:
            print("Result:",word)
    else: # trict search
        search = zipsort(asksearch)
        if search in dictionary:
            print("Result:",dictionary[search])
        else:
            print("No word found!")
    askend = input("End search? (y/n)")
