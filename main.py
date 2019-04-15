import nltk
from nltk.tree import *
import os
from nltk.parse import stanford
nltk.download('tagsets')
from nltk.parse import CoreNLPParser
from collections import Counter
import sys
from nltk.corpus import wordnet as wn
import re
'''
# Single sentences for testing
testSentence = ["Is the Pacific deeper than the Atlantic?"]

# Sentences required for Part 3
p3_sentences = ["Is the Pacific deeper than the Atlantic?",
             "Did Swank win the oscar in 2000?",
             "Is the Shining by Kubrik?",
             "Does the album Thriller include the track BeatIt?",
             "Who directed Hugo?",
             "Which is the scary movie by Kubrik with Nicholson?",
             "In which continent does Canada lie?",
             "With which countries does France have a border?,"
             " Where was Gaga born?",
             "In which album does Aura appear?",
             "Which album by Swift was released in 2014?"]

#Sentences from Part 1.2
sentences1_2 = ["Is Rome the capital of Italy?",
             "Is France in Europe?",
             "Is the Pacific deeper than the Atlantic?",
             "Did Neeson star in Schindler's List?",
             "Did Swank win the oscar in 2000?",
             "Is the Shining by Kubrik?",
             "Did a French actor win the oscar in 2012?",
             "Did a movie by Spielberg with Neeson win the oscar for best film?",
             "Did Madonna sing PapaDoNotPreach?",
             "Does the album Thriller include the track BeatIt?",
             "Was Beyonce' born in the USA?"]

'''

#get the file specified in argument
filepath = sys.argv[1]

#check if filepath is valid 
if not os.path.isfile(filepath):
   print("File path {} does not exist.".format(filepath))
   sys.exit()

#open file and put each line into a list
with open(filepath, 'r') as inputFile:
    sentences = inputFile.readlines()

	
#testsentence = ['dog']
#do the actual thing 
for sentence in sentences:
    print("*   *   *   *   *   *   *   *   *   *   *   *   ")
	#print sentence
    print("<QUESTION> " + sentence)
    # Lexical Parser
    parser = CoreNLPParser(url='http://localhost:9000')
    # Tokenizer
    tokens = list(parser.tokenize(sentence))
    print(tokens)
	
    #lists of key words to match similarities and categorize 
    geography = ['geography', 'Antarctic', 'places', 'location', 'locations', 'area', 'areas', 'America', 'Europe', 'Australia', 'Asia', 'Pacific', 'Italy', 'place', 'state', 'country', 'continent', 'world', 'ocean', 'oceans', 'river', 'rivers', 'mountain', 'mountains', 'desert', 'deserts', 'city', 'cities', 'town', 'towns', 'capital', 'village', 'villager', 'land', 'Atlantic', 'Indian', 'India', 'sea', 'seas']
    music = ['music', 'song', 'songs', 'notes', 'sing', 'instrument', 'album', 'artist', 'singer', 'player', 'concert', 'jazz', 'pop', 'vocalist', 'band', 'bands', 'rock', 'piano', 'guitar', 'trumpet', 'musicians', 'musician', 'blues', 'metal', 'classical']
    movies = ['movies', 'cinema', 'cinematic', 'movie', 'theater', 'theatre', 'actor', 'actress', 'show', 'showing', 'watch', 'watched', 'watching', 'view', 'see', 'screen', 'acted', 'directed', 'director', 'film', 'filmography', 'cinematography', 'video']
    #s = wn.synsets('dog')
    #t = wn.synsets('geography')
	#print(s[0].lemma_names())#gives the actual word 
    #print(s[0].name()) #prints the lemma.pos.number syntax 
    #print(wn.synsets('dog')[0].wup_similarity(wn.synsets('cat')[0])) #this is all you need to do to get similarity between two words 
    #for every word in the sentence, compare the first synset to the synsets of everything in the category lists
    #print(wn.synsets('dog')[0].wup_similarity(wn.synsets('cat')[0])) #this is all you need to do to get wu palmer similarity between two words 
    totals = [0.0, 0.0, 0.0]
    firstX = 15 #get the first X elements of each list of similarities - so that the size of the lists doesn't matter 
    firstX = min(firstX, len(geography), len(music), len(movies)) #make sure each category is equal for the average
    for token in tokens[:-1]: #exclude the question mark token - this assumes that there is a question mark token 
        geogList = []
        for ge in geography:
            var = 0
            tokSyn = wn.synsets(token)
            if len(tokSyn) != 0:
                var = tokSyn[0].wup_similarity(wn.synsets(ge)[0])
            if var is not None:
                geogList.append(var)
        #geogList.sort()
        geogList = sorted(geogList, reverse=True)
        firstXSim = 0
        for simVal in geogList[:firstX]:
            firstXSim += simVal
        totals[0] += (firstXSim/firstX) #add the average of the first X geography similarities
		
        musicList = []
        for mu in music:
            var = 0
            tokSyn = wn.synsets(token)
            if len(tokSyn) != 0:
                var = tokSyn[0].wup_similarity(wn.synsets(mu)[0])
            if var is not None:
                musicList.append(var)
        musicList = sorted(musicList, reverse=True)
        #musicList.sort()
        firstXSim = 0
        for simVal in musicList[:firstX]:
            firstXSim += simVal        
        totals[1] += (firstXSim/firstX) #add average of the first X music similarities
		
        moviesList = []
        for mo in movies:
            var = 0
            tokSyn = wn.synsets(token)
            if len(tokSyn) != 0:
                var = tokSyn[0].wup_similarity(wn.synsets(mo)[0])
            if var is not None:
                moviesList.append(var)
        #moviesList.sort()
        moviesList = sorted(moviesList, reverse=True)
        firstXSim = 0
        for simVal in moviesList[:firstX]:
            firstXSim += simVal        
        totals[2] += (firstXSim/firstX) #add average of the first X movies similarities
		

    #average the totals, the max average is the category 
    for t in totals:
        t /= (len(tokens)-1)

    if max(totals) == totals[0]:
        category = 'geography'
    elif max(totals) == totals[1]:
        category = 'music'
    elif max(totals) == totals[2]:
        category = 'movies'
    print("<CATEGORY " + category)
    print("geog: " + str(totals[0]))
    print("music: " + str(totals[1]))
    print("movies: " + str(totals[2]))
	
    # Parse raw string.
    parsedList = list(parser.raw_parse(sentence))
    #print(parsedList[0]) #prints parse tree in non pretty form 
    # makes a parse tree from an already parsed sentence
    parsetree = Tree.fromstring(str(parsedList[0]))
    #print parsetree
    print("<PARSETREE>")
    parsetree.pretty_print()
	
    print("\n")

	