import nltk
from nltk.tree import *
nltk.download('tagsets')

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
    tokens = nltk.word_tokenize(sentence)

    print("Sentence Tokens: " + str(tokens))

    tagged = nltk.pos_tag(tokens)

    print("\nTagged:")
    for word in tagged:
        print("\t" + str(word))
    print("\n")

    entities = nltk.chunk.ne_chunk(tagged)
    print("Entities:")
    print(entities)

    testEntities = "(ROOT (SQ (VBZ Is) (NP (DT the) (NNP Pacific)) (NP (NP (JJR deeper)) (PP (IN than) (NP (DT the) (NNP Atlantic)))) (. ?)))"

    # Prints a parse tree from an already parsed sentence
    parsetree = Tree.fromstring(str(testEntities))
    #print parsetree
    parsetree.pretty_print()

    print("\n\n")

    grammar = ('''
    NP: {<DT>?<JJ>*<NN>} # NP
    ''')



    # nltk.help.upenn_tagset("PRP$")
    # nltk.help.upenn_tagset("NN")
    # nltk.help.upenn_tagset("VBZ")
    # nltk.help.upenn_tagset("NNP")

