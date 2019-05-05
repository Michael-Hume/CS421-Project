import nltk
from nltk.tree import *
import os
from nltk.parse import stanford
from nltk.parse import CoreNLPParser
from collections import Counter
import sys
from nltk.corpus import wordnet as wn
import re

#get the file specified in argument
#filepath = sys.argv[1]

#check if filepath is valid
#if not os.path.isfile(filepath)
#print("File path {} does not exist.".format(filepath))
#sys.exit()

#open file and put each line into a list
tagsListList = []
tagDictList = []
print("*****************************************************************************************************")
with open("input2.txt", 'r') as inputFile:
    sentences = inputFile.readlines()

#inputFile = open("input.txt","r")
#sentences = inputFile.readlines()

#testsentence = ['dog']
#do the actual thing
for sentence in sentences:
    print("\n*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   ")
    sentence.replace("'", "")
    print("<QUESTION> " + sentence + "\n")
    # Lexical Parser
    parser = CoreNLPParser(url='http://localhost:9000')
    # Tokenizer
    tokens = list(parser.tokenize(sentence))
    # print("TOKENS START")
    # print(tokens)
    # print("TOKENS END")

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
        t /= (len(tokens)-1)

    if max(totals) == totals[0]:
        category = 'geography'
    elif max(totals) == totals[1]:
        category = 'music'
    elif max(totals) == totals[2]:
        category = 'movies'
    #print("<CATEGORY " + category)
    #print("geog: " + str(totals[0]))
    #print("music: " + str(totals[1]))
    #print("movies: " + str(totals[2]))

    # Parse raw string.
    parsedList = list(parser.raw_parse(sentence))
    #print("Parsed List:")
    #print(parsedList[0]) #prints parse tree in non pretty form
    # makes a parse tree from an already parsed sentence
    parsetree = Tree.fromstring(str(parsedList[0]))

    # Build the beginning of the SQL theory to add to later
    sqlQuery = "SELECT "

    # --> Convert the tree to a list
    splitTree = str(parsedList[0]).splitlines()

    # Remove question mark & first two tags (as long as the question is long enough)
    if(len(splitTree) > 2):
        del splitTree[-1]
        if (len(splitTree) > 1):
            del splitTree[:2]
    else:
        del splitTree[:1]

    num = 1
    subList = []
    questionTags = []
    questionTagsDict = {}
    #print("Split Tree: " + str(splitTree) + "\n")


    # This whole section just removes the white spaces, parentheses, etc... - - - - - - - - - - - - - - - - - - - - - - - - - -
    # It outputs the leaves in two formats:
        # tagsList - list of the tags (WP, WDT, WRB, VBZ, VBD...)
        # questionTagsDict - a dictionary with each tag as the key and it's word as the value)
    num = 1
    for i in splitTree:
        # remove leading & ending whitespace
        i.lstrip()
        i.strip()
        tempB = str(num) + " -> " + i.lstrip()
        num = num + 1

    num = 1
    tagsList = []
    for i in splitTree:
        i.lstrip()
        i.strip()
        i = i.lstrip()
        tempB = str(num) + " -> " + i

        if " " in i:
            subList = i.split("(")
            del subList[:1]
            for x in subList:
                x = x.strip()
                if " " in x:
                    tempX = x.replace(")", "")
                    print("\t" + str(num) + "->" + tempX)
                    #print("\t" + tempX)
                    tempXX = tempX.split(" ")
                    num1 = 1
                    questionTags.append(tempXX)
                    tag = tempXX[0]
                    tagsList.append(tag)
                    value = tempXX[1]

                    if tag in questionTagsDict:
                        tag = "*" + tag
                    questionTagsDict[tag] = value
                    #for z in tempXX:
                        #if not (z[0]) == "DT":
                        #print("z: " + str(z))

            num = num + 1
    print("\tQUESTION TAGS: ")
    print("\t" + str(questionTags))
    print("\n")
    print("\tQUESTION TAGS DICT: ")
    print("\t" + str(questionTagsDict))


    print("\t ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
    for tag in questionTagsDict:
        #tagsList.append(tag.replace("*", ""))
        print("\tTag: " + tag.replace("*", ""))
        print("\t\tWord: " + questionTagsDict.get(tag))
    print("\t ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n")

    if "DT" in tagsList:
        tagsList.remove("DT")
    if "IN" in tagsList:
        tagsList.remove("IN")
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    print("Tag List:")
    #tagsList.reverse()
    print(tagsList)
    print("\n")

    sent = sentence[:-1]
    sent = "\n" + sent

    # This justmakes a list of all the tags list from all the sentences, not really useful other than just viewing them
    tagsListList.append(sent)
    tagsListList.append(tagsList)
    tagDictList.append(questionTagsDict)

    # This is a list of all the colums of all the tables in the movie database, will be used later in building SQL queries
    Select_Strings = ["actor_id", "movie_id", "director_id", "id", "name", "year", "rating", "runtime", "genre", "earnings_rank", "person_id", "type", "COUNT(*)"]
    # This is a list of all the tables in the movies database
    From_Strings = ["FROM ACTOR", "FROM MOVIE", "FROM DIRECTOR", "FROM OSCAR", "FROM PERSON"]

    print("SQL Query Builder")
    print("v  v  v  v  v  v  v  v  v  v  v  v  v  v  v  v  v  v")


    # if Word is WHO or WHAT
    if tagsList[0].replace("*", "") == "WP":
        print("1st Word is WHO/WHAT")
        # From here the only way i can figure out to build queries is to
        #if tagsList[1].replace("*", "") ==

    # if Word is WHICH
    elif tagsList[0].replace("*", "") == "WDT":
        print("1st Word is WHICH")
        #if tagsList[1].replace("*", "") ==


    # if Word is WHERE or WHEN
    elif tagsList[0].replace("*", "") == "WRB":
        print("1st Word is WHERE")
        #if tagsList[1].replace("*", "") ==


    # if Word is IS or DOES
    elif tagsList[0].replace("*", "") == "VBZ":
        print("1st Word is IS/DOES")
        #if tagsList[1].replace("*", "") ==


    # if Word is DID or WAS
    elif tagsList[0].replace("*", "") == "VBD":
        print("1st Word is DID/WAS")
        #if tagsList[1].replace("*", "") ==


    # Word is IN or WITH
    # elif tagsList[0].replace("*", "") == "IN":
    #     print("1st Word is IN/WITH")
    #     if tagsList[1].replace("*", "") ==





    print("^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^")



    if "WDT" in tagsList:
        if "NN" in tagsList:
            print()
        elif "NP" in tagsList:
            print("\n")

    print("\nSQL Query: '" + sqlQuery + "'")
    print("\n*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   ")








print("\n TAG LIST LIST: ")
for x in tagsListList:
    print(x)
print("\n TAG DICTS LIST: ")
for x in tagDictList:
    print(x)
print("*****************************************************************************************************\n")