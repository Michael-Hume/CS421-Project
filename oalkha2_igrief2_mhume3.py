#Omar Al-Khatib / oalkha2
#Isaiah Grief / igrief2
#Michael Hume / mhume3
#CS421 Spring 2019
#University of Illinois at Chicago
#Project Part 1

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
from nltk.stem import WordNetLemmatizer
import sqlite3

#get the file specified in argument
filepath = sys.argv[1]

#check if filepath is valid 
if not os.path.isfile(filepath):
   print("File path {} does not exist.".format(filepath))
   sys.exit()

#open file and put each line into a list
with open(filepath, 'r') as inputFile:
    sentences = inputFile.readlines()


def CountryContinent(): #is <country> in <continent> #WHERE Countries.Name = " + country + " and Continents.Continent = " + continent  
    return "Countries INNER JOIN CountryContinents ON Countries.Id = CountryContinents.CountryID INNER JOIN Continents ON CountryContinents.ContinentID = Continents.Id "

def CapitalsCountries(): #what is the capital of <country> #SELECT Cities.Name / WHERE Countries.Name = <country> #where is <city>  #SELECT Countries.Name / WHERE Cities.Name = <city> 
    return "Capitals INNER JOIN Cities ON Cities.Id = Capitals.CityID INNER JOIN Countries ON Countries.Id = Capitals.CountryID "

    
    	
    
testsentences = ['Did Allen direct MightyAphrodite?', 'Did Allen direct Mighty Aphrodite?', 'Did a French actor win the oscar in 2012?']
testsentences2 = ['Is Rome the capital of Italy?', 'Is Madrid the capital of Germany?']
#do the actual thing 
for sentence in testsentences2: 
    print("*   *   *   *   *   *   *   *   *   *   *   *   ")
	#print sentence
    print("<QUESTION> " + sentence)
    # Lexical Parser
    parser = CoreNLPParser(url='http://localhost:9000')
    # Tokenizer
    tokens = list(parser.tokenize(sentence))
    #print(tokens)
    
    
    
    # POS Tagger
    pos_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='pos')
    pos_tags = list(pos_tagger.tag(sentence.split()))
    print(pos_tags)
    #print(pos_tags[0][1])
    
    #reduce the pos list by combining adjacent NNPs and ignoring possessives - and also gets rid of question mark at end by not appending it 
    previous = ('','')
    reducedList = []
    for i in range(0, len(pos_tags)):
        #look for adjacent NNP, NNPS, and POS tags 
        if previous[1] == '': #beginning or after pos 
            previous = pos_tags[i]
        if pos_tags[i][1] == 'NNP' or pos_tags[i][1] == 'NNPS': #concat the words with a space 
            if previous[1] == 'NNP' or previous[1] == 'NNPS':
                previous = (previous[0] + ' ' + pos_tags[i][0], 'NNP')
            else:
                reducedList.append(previous)
                previous = (pos_tags[i])
        else:
            reducedList.append(previous)
            if pos_tags[i][1] != 'POS': #if its POS, we ignore it, otherwise just continue on 
                previous = (pos_tags[i])
            else:
                previous = ('','')
    print("reduced:")
    print(reducedList) 
	#lemmas?
    lemmatizer = WordNetLemmatizer()
    #print("rocks: ", lemmatizer.lemmatize("rocks")) #default is noun 
    #print("big: ", lemmatizer.lemmatize("big", pos = "a")) #a for adjective, v for verb 
    questiontype = lemmatizer.lemmatize(reducedList[0][0].lower(), pos = "v") #'be' or 'do' for yes/no, anything else we can say is some kind of WH question 
    print("question type:")
    print(questiontype)
    
    
	
    #lists of key words to match similarities and categorize 
    geography = ['geography', 'Antarctic', 'places', 'location', 'locations', 'area', 'areas', 'America', 'Europe', 'Australia', 'Asia', 'Pacific', 'Italy', 'place', 'state', 'country', 'continent', 'world', 'ocean', 'oceans', 'river', 'rivers', 'mountain', 'mountains', 'desert', 'deserts', 'city', 'cities', 'town', 'towns', 'capital', 'village', 'villager', 'land', 'Atlantic', 'Indian', 'India', 'sea', 'seas']
    music = ['music', 'song', 'songs', 'notes', 'sing', 'instrument', 'album', 'artist', 'singer', 'player', 'concert', 'jazz', 'pop', 'vocalist', 'band', 'bands', 'rock', 'piano', 'guitar', 'trumpet', 'musicians', 'musician', 'blues', 'metal', 'classical']
    movies = ['movies', 'cinema', 'cinematic', 'movie', 'theater', 'theatre', 'actor', 'actress', 'show', 'showing', 'watch', 'watched', 'watching', 'view', 'see', 'screen', 'acted', 'directed', 'director', 'film', 'cinematography','video']
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
        t /= (len(tokens)-1) #assumes at least length 1 else there is a division by 0 error 

    #get a list of the proper nouns in the sentence (from the reduced list) 
    properNounList = []
    for x in reducedList:
        if x[1] == 'NNP' or x[1] == 'NNPS':
            properNounList.append(x[0])
            
    query = ""
    if max(totals) == totals[0]: #GEOGRAPHY 
        if questiontype == 'be' or questiontype == 'do': #yes/no questions 
            query += "SELECT COUNT(*) FROM "
            for x in reducedList:
                if x[0] == 'capital':
                    query += CapitalsCountries() 
                    query += "WHERE Cities.Name = " + properNounList[0] + " and Countries.Name = " + properNounList[1]                    
        print(query)
    elif max(totals) == totals[1]: #MUSIC 
        if questiontype == 'be' or questiontype == 'do': #yes/no questions 
            query += "SELECT COUNT(*) FROM "
    elif max(totals) == totals[2]: #MOVIES 
        if questiontype == 'be' or questiontype == 'do': #yes/no questions 
            query += "SELECT COUNT(*) FROM "
            
            
    #print("<CATEGORY " + category)
    #print("geog: " + str(totals[0]))
    #print("music: " + str(totals[1]))
    #print("movies: " + str(totals[2]))
	
    # Parse raw string.
    parsedList = list(parser.raw_parse(sentence))
    #print(parsedList[0][0][1][0][0][0][0]) #root, child, children - so in most cases the first 2 only have 1
        #i have no idea how to traverse the tree in a way that is helpful though 
            #especially since you need to have as many brackets as levels you are traversing 
    #print(parsedList[0]) #prints parse tree in non pretty form 
    # makes a parse tree from an already parsed sentence
    parsetree = Tree.fromstring(str(parsedList[0]))
    
    #attempt to traverse the tree, doesn't really work as well as I wanted it to 
    #def traverse_tree(tree):
    #    print("tree:", tree)
    #    for subtree in tree:
    #        if type(subtree) == nltk.tree.Tree:
    #            traverse_tree(subtree)
    #traverse_tree(parsetree)
    
    print("<PARSETREE>")
    print(parsetree)
    parsetree.pretty_print()
	
    print("\n")

    

conn = sqlite3.connect('oscar-movie_imdb.sqlite')
print("Opened database successfully")
cursor = conn.execute("Select Count(*) FROM Oscar O INNER JOIN Person P ON person_id = P.id WHERE P.name LIKE '%Bigelow%' AND O.type='BEST-DIRECTOR'")
for row in cursor:
    print(row[0])
conn.close()

