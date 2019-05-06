#Omar Al-Khatib / oalkha2
#Isaiah Grief / igrief2
#Michael Hume / mhume3
#CS421 Spring 2019
#University of Illinois at Chicago
#Project Part 2

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


def CountryContinent():  
    return "Countries INNER JOIN CountryContinents ON Countries.Id = CountryContinents.CountryID INNER JOIN Continents ON CountryContinents.ContinentID = Continents.Id "

def CapitalsCountries():
    return "Capitals INNER JOIN Cities ON Cities.Id = Capitals.CityID INNER JOIN Countries ON Countries.Id = Capitals.CountryID "

def ArtistTrack(): 
    return "Artist INNER JOIN Album ON Artist.id = Album.artsitID INNER JOIN Track ON Track.albumID = Album.albumID "
    
def MovieBorn():
    return "Person "
    
def Movie():
    return "Movie "
    
def OscarMovie():
    return "Movie INNER JOIN Oscar ON Movie.id = Oscar.movie_id "

def JoinMovieDirector(): #joins movie table with director table (and person table)
    return "INNER JOIN Director ON Movie.id = Director.movie_id INNER JOIN Person ON Director.director_id = Person.id "

def JoinMovieActor(): #joins movie table with actor table (and person table)
    return "INNER JOIN Actor ON Movie.id = Actor.movie_id INNER JOIN Person ON Actor.actor_id = Person.id "

    
def QueryYesNo(query, database, queryDone):
    #print("yes no")
    print('<QUERY>')
    print(query)
    print('<ANSWER>')
    if queryDone:
        conn = sqlite3.connect(database)
        cursor = conn.execute(query)
        row = cursor.fetchone() #for count(*) this should be the only one 
       #print(row[0])
        if row[0] >= 1:
            print("Yes")
        else:
            print("No")
        conn.close()
    else: 
        print("I don't know")
        
def QueryWH(query, database, queryDone):
    #print("wh")
    print('<QUERY>')
    print(query)
    print('<ANSWER>')
    if queryDone:
        conn = sqlite3.connect(database)
        cursor = conn.execute(query)
        row = cursor.fetchone()
        if row == None:
            print("I don't know")
        else:
            print(row[0])
        conn.close()
    else: 
        print("I don't know")
        
def AddWhere(query, addition):
    if 'WHERE' in query: #dont repeat wheres, just add with ANDS
        return query + " AND " + addition
    else:
        return query + " WHERE " + addition
        
        
def grammarList(grammar, parent):
    child = ""
    isLeaf = False
    for node in parent:
        if not isinstance(node, str):
            child += node.label() + " "
            grammar = grammarList(grammar, node)
        else:
            child += node
            isLeaf = True
    if not isLeaf:
        child = child[:-1]
    grammar.append((parent.label(), child))
    return grammar
        
testsentences = ['Did Allen direct MightyAphrodite?', 'Did Allen direct Mighty Aphrodite?', 'Did a French actor win the oscar in 2012?']
testsentences2 = ['Is Rome the capital of Italy?', 'Is Madrid in Germany?', 'What is the capital of France?', 'Where is London?']
testsentences3 = ["Was Birdman the best movie in 2015?", "Did Swank win the oscar in 2000?", "Did Neeson star in Schindler's List?", "Is Mighty Aphrodite by Allen?"] 
#do the actual thing 
for sentence in sentences: 
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
    #print(pos_tags)
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
    #print("reduced:")
    #print(reducedList) 
	#lemmas?
    lemmatizer = WordNetLemmatizer()
    #print("rocks: ", lemmatizer.lemmatize("rocks")) #default is noun 
    #print("big: ", lemmatizer.lemmatize("big", pos = "a")) #a for adjective, v for verb 
    questiontype = lemmatizer.lemmatize(reducedList[0][0].lower(), pos = "v") #'be' or 'do' for yes/no, anything else we can say is some kind of WH question 
    #print("question type:")
    #print(questiontype)
    
    
	
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

    if max(totals) == totals[0]:
        category = 'geography'
    elif max(totals) == totals[1]:
        category = 'music'
    else:
        category = 'movies'
        
    #overriding categorization so that we can actually answer most of the movies questions: 
    for x in reducedList:
        if x[0] == 'actor' or x[0] == 'actress' or x[0] == 'oscar' or x[0] == 'directed' or x[0] == 'movie':
            category = 'movies'
        elif x[0] == 'album':
            category = 'music'
    
    #get a list of the proper nouns in the sentence (from the reduced list) 
    properNounList = []
    for x in reducedList:
        if x[1] == 'NNP' or x[1] == 'NNPS':
            properNounList.append(x[0])
            
    query = ""
    
    queryDone = False
    posConcat = ""
    for x in reducedList: #get a concatenated list of pos tags to match patterns 
        posConcat += x[1] + " "
    if category == 'geography': #GEOGRAPHY 
       # print("THIS IS GEOGRAPHY")
        if questiontype == 'be' or questiontype == 'do': #yes/no questions 
            query += "SELECT COUNT(*) FROM "
            for x in reducedList:
                if x[0] == 'capital':
                    query += CapitalsCountries() 
                    query += "WHERE Cities.Name = " + "'" + properNounList[0] + "'" + " and Countries.Name = " + "'" + properNounList[1] + "'"
                    queryDone = True 
                    break
            if not queryDone: 
                if "NNP IN NNP" in posConcat:
                    query += CountryContinent()
                    query += "WHERE Countries.Name = " + "'" + properNounList[0] + "'" + " and Continents.Continent = " + "'" + properNounList[1] + "'" 
                    queryDone = True
            QueryYesNo(query, 'WorldGeography.sqlite', queryDone)
        else: #WH questions 
            if questiontype == 'what':
                query += "SELECT Cities.Name FROM "
                for x in reducedList:
                    if x[0] == 'capital':
                        query += CapitalsCountries() 
                        query += "WHERE Countries.Name = " + "'" + properNounList[0] + "'"
                        queryDone = True 
                        break
            elif questiontype == 'where':
                query += "SELECT Countries.Name FROM "
                if "WRB VBZ NNP" in posConcat: #format for this question 
                    query += CapitalsCountries()
                    query += "WHERE Cities.Name = " + "'" + properNounList[0] + "'"
                    queryDone = True 
            QueryWH(query, 'WorldGeography.sqlite', queryDone)
    elif category == 'music': #MUSIC 
       # print("THIS IS MUSIC")
        if questiontype == 'be' or questiontype == 'do': #yes/no questions 
            query += "SELECT COUNT(*) FROM "
            query += ArtistTrack()
            if(len(properNounList) >= 2):
                query = AddWhere(query, "Artist.name LIKE " + "'%" + properNounList[0] + "%'")
                query = AddWhere(query, "Track.name LIKE " + "'%" + properNounList[1] + "%'")
            queryDone = True
            QueryYesNo(query, 'music.sqlite', queryDone)
        else: #WH- QUESTIONS
            if questiontype == 'who': #probably asking about a song 
                query += "SELECT Artist.name FROM "
                query += ArtistTrack()
                query = AddWhere(query, "Album.name LIKE " + "'%" + properNounList[0] + "%'")
            if questiontype == 'when':
                query += "SELECT Album.releaseDate FROM "
                query += ArtistTrack()
                query = AddWhere(query, "Album.name LIKE " + "'%" + properNounList[0] + "%'")
                queryDone = True
            QueryWH(query, 'music.sqlite', queryDone)
    elif category == 'movies': #MOVIES
       # print("THIS IS MOVIES")
        year = 0
        oscar = False
        oscarType = ""
        nationality = False
        #look at 'best' and check the next word against the list of things 
        #make sure adj italian and german and american and all that are converted to NNPs in list 
        for x in reducedList:
            if x[0] == 'American':
                properNounList.append('USA')
                nationality = True
            elif x[0] == 'Italian':
                properNounList.append('Italy')
                nationality = True
            elif x[0] == 'British':
                properNounList.append('UK')
                nationality = True
            elif x[0] == 'German':
                properNounList.append('Germany')
                nationality = True
            elif x[0] == 'French':
                properNounList.append('France')
                nationality = True
            elif x[0] == 'best':
                oscar = True
                continue
            elif x[0] == 'oscar':
                oscarType = 'generic'
            elif x[1] == 'CD':
                year = int(x[0],10)
            elif oscar: #best was the previous word, so its probably talking about an oscar
                if x[0] == 'actress':
                    oscarType = 'BEST-ACTRESS'
                elif x[0] == 'actor':
                    oscarType = 'BEST-ACTOR'
                elif x[0] == 'movie' or x[0] == 'film':
                    oscarType = 'BEST-PICTURE'
            oscar = False
            
        if questiontype == 'be' or questiontype == 'do': #yes/no questions 
            query += "SELECT COUNT(*) FROM "
            if len(oscarType) > 0: #its some oscar question, lets query both OscarMovie and OscarPerson since we don't have NER tag to tell us if its a person 
                query += OscarMovie() #either leave as is or its a person so its one of joinmoviedirector or joinmovieactor
                if 'act' in sentence:
                    query += JoinMovieActor()
                elif 'direct' in sentence:
                    query += JoinMovieDirector()
                else:
                    query = AddWhere(query,"Movie.name LIKE " + "'%" + properNounList[0] + "%'")
                if oscarType != 'generic':
                    query = AddWhere(query, "Oscar.type = " + "'" + oscarType + "'")
                queryDone = True
            elif 'NNP IN NNP' in posConcat or 'VB IN NNP' in posConcat: #probably an actor in a movie 
                query += Movie()
                query += JoinMovieActor()
                query = AddWhere(query, "Person.name LIKE " + "'%" + properNounList[0] + "%'")
                query = AddWhere(query, "Movie.name LIKE " + "'%" + properNounList[1] + "%'")
                queryDone = True
            else: #look for keywords 
                for x in reducedList:
                    if x[0] == 'director':
                        query += Movie() 
                        query += JoinMovieDirector()
                        query = AddWhere(query, "Director.name LIKE " + "'%" + properNounList[0] + "%'")
                        queryDone = True
            if year > 0: #add a where clause for time -either movie or oscar 
                if len(oscarType) > 0:
                    query = AddWhere(query, "Oscar.year = " + str(year))
                else:
                    query = AddWhere(query, "Movie.year = " + str(year))
            if nationality:
                query = AddWhere(query, "Person.pob LIKE " + "'%" + properNounList[len(properNounList)-1] + "%'")
            QueryYesNo(query, 'oscar-movie_imdb.sqlite', queryDone)
        else: #WH- QUESTIONS
            if questiontype == 'when': #we only have movie year and oscar year so its one of those 
                if len(oscarType) > 0: #we'll be getting oscar year 
                    query += "SELECT Oscar.year FROM "
                    if 'act' in sentence: #person oscar 
                        query += OscarMovie()
                        query += JoinMovieActor()
                    else: #movie oscar
                        query += OscarMovie()
                    queryDone = True
                else: #get movie year from whatever its from 
                    query += "SELECT Movie.year FROM "
                    query += Movie()
                    queryDone = True 
            elif questiontype == 'who':
                query += "SELECT Person.name FROM "
                if len(oscarType) > 0: #its a person oscar question 
                    query += OscarMovie() #join either director or actor 
                    if 'act' in sentence: 
                        query += JoinMovieActor()
                    else:
                        query += JoinMovieDirector()
                    queryDone = True
                elif 'direct' in sentence:
                    query += Movie()
                    query += JoinMovieDirector()
                    query = AddWhere(query, "Movie.name LIKE " + "'%" + properNounList[0] + "%'")
                    queryDone = True
            elif questiontype == 'which':
                if 'act' in sentence: 
                    query += "SELECT Person.name FROM " 
                    if len(oscarType) > 0: #person oscar
                        query += OscarMovie() #join either director or actor 
                        if 'act' in sentence: 
                            query += JoinMovieActor()
                        else:
                            query += JoinMovieDirector()
                    else: 
                        query += Movie()
                    queryDone = True
                else:
                    query += "SELECT Movie.name FROM "
                    if len(oscarType) > 0: #movie oscar
                        query += OscarMovie() 
                    else:
                        query += Movie()
                    queryDone = True
            if year > 0: #add a where clause for time -either movie or oscar 
                if len(oscarType) > 0:
                    query = AddWhere(query, "Oscar.year = " + str(year))
                else:
                    query = AddWhere(query, "Movie.year = " + str(year))
            if nationality:
                query = AddWhere(query, "Person.pob LIKE " + "'%" + properNounList[len(properNounList)-1] + "%'")
            if len(oscarType) > 0: #if it was an oscar question, add the where clause 
                #print("oscar type: ")
                #print(oscarType)
                if oscarType != 'generic':
                    query = AddWhere(query, "Oscar.type = " + "'" + oscarType + "'")
            QueryWH(query, 'oscar-movie_imdb.sqlite', queryDone)
            
    #print("<CATEGORY " + category)
    #print("geog: " + str(totals[0]))
    #print("music: " + str(totals[1]))
    #print("movies: " + str(totals[2]))
	
    # Parse raw string.
    parsedList = list(parser.raw_parse(sentence))
    parsetree = Tree.fromstring(str(parsedList[0]))
    #print(parsedList[0])
    grammar = []
    grammar = grammarList(grammar, parsetree)
    #print(grammar)
    
    
        

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
    
    #print("<PARSETREE>")
    #print(parsetree)
    #parsetree.pretty_print()
	
    #print("\n")
