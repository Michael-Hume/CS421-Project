import nltk
from nltk.tree import *
import os
from nltk.parse import stanford
nltk.download('tagsets')
from nltk.parse import CoreNLPParser
from collections import Counter

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

for sentence in testSentence:
    print("*   *   *   *   *   *   *   *   *   *   *   *   ")
    print("Sentence: " + sentence + "\n")
	
	#splits a sentence into tokens (punctuation, words, $ symbols, numbers, floats) eg $3.55 becomes $, 3.55
    tokens = nltk.word_tokenize(sentence)

	#prints the tokens (str() returns a printable representation of an object)
    print("Sentence Tokens: " + str(tokens))

	#tag a sequence of words 
    tagged = nltk.pos_tag(tokens)

	#print tags
    print("\nTagged:")
    for word in tagged:
        print("\t" + str(word))
	
    entities = nltk.chunk.ne_chunk(tagged)
    print("Entities:")
    print(entities)

    # Lexical Parser
    parser = CoreNLPParser(url='http://localhost:9000')
    # Parse raw string.
    parsedList = list(parser.raw_parse(sentence))
    print(parsedList[0])
    # Prints a parse tree from an already parsed sentence
    parsetree = Tree.fromstring(str(parsedList[0]))
    #print parsetree
    parsetree.pretty_print()
	
	
    # NER Tagger
    ner_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')
    ner_tags = list(ner_tagger.tag((sentence.split())))
    #print(ner_tags) #prints all word/category tuples
    #print(ner_tags[0]) #prints word/category tuple 
    #print(ner_tags[0][1]) #prints category
    ner_list = []
    for ner_word in ner_tags:
	    ner_list.append(ner_word[1])
    print(ner_list)	
    counter = Counter(ner_list)
    #prints most common word
    categories = counter.most_common(2)
    print(categories) 
	#we don't care about the 'O' category 
    if categories[0][0] == 'O': 
	    print("Category: " + categories[1][0])
    else:
	    print("Category: " + categories[0][0])

	
    # nltk.help.upenn_tagset("PRP$")
    # nltk.help.upenn_tagset("NN")
    # nltk.help.upenn_tagset("VBZ")
    # nltk.help.upenn_tagset("NNP")

	