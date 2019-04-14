import nltk
from nltk.tree import *
import os
from nltk.parse import stanford
nltk.download('tagsets')
from nltk.parse import CoreNLPParser

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
    print("\n")

	
    entities = nltk.chunk.ne_chunk(tagged)
    print("Entities:")
    print(entities)

	#from the stanford parser
    testEntities = "(ROOT (SQ (VBZ Is) (NP (DT the) (NNP Pacific)) (NP (NP (JJR deeper)) (PP (IN than) (NP (DT the) (NNP Atlantic)))) (. ?)))"
	#[Tree('ROOT', [Tree('SBARQ', [Tree('WHNP', [Tree('WP', ['What'])]), Tree('SQ', [Tree('VBZ', ['is']), Tree('NP', [Tree('NP', [Tree('DT', ['the']), Tree('NN', ['airspeed'])]), Tree('PP', [Tree('IN', ['of']), Tree('NP', [Tree('DT', ['an']), Tree('JJ', ['unladen'])])]), Tree('S', [Tree('VP', [Tree('VB', ['swallow'])])])])]), Tree('.', ['?'])])])]


    # Prints a parse tree from an already parsed sentence
    parsetree = Tree.fromstring(str(testEntities))
    #print parsetree
    parsetree.pretty_print()

    print("\n\n")
	
    
    grammar = ('''
    NP: {<DT>?<JJ>*<NN>} # NP
    ''')

	#this bit does the same thing as above basically but actually parses the sentence with the stanford parser 
    # Lexical Parser
    parser = CoreNLPParser(url='http://localhost:9000')
    # Parse raw string.
    parsedList = list(parser.raw_parse(sentence))
    print(parsedList[0])
    # Prints a parse tree from an already parsed sentence
    parsetree = Tree.fromstring(str(parsedList[0]))
    #print parsetree
    parsetree.pretty_print()

	
    # nltk.help.upenn_tagset("PRP$")
    # nltk.help.upenn_tagset("NN")
    # nltk.help.upenn_tagset("VBZ")
    # nltk.help.upenn_tagset("NNP")

	