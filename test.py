from nltk.parse import CoreNLPParser

# Lexical Parser
parser = CoreNLPParser(url='http://localhost:9000')

# Parse tokenized text.
print(list(parser.parse('What is the airspeed of an unladen swallow ?'.split())))

# Parse raw string.
#print(list(parser.raw_parse('What is the airspeed of an unladen swallow ?')))
testList = list(parser.raw_parse('What is the airspeed of an unladen swallow ?'))
print(testList[0])


# Neural Dependency Parser
from nltk.parse.corenlp import CoreNLPDependencyParser
dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
parses = dep_parser.parse('What is the airspeed of an unladen swallow ?'.split())
print([[(governor, dep, dependent) for governor, dep, dependent in parse.triples()] for parse in parses])


# Tokenizer
parser = CoreNLPParser(url='http://localhost:9000')
print(list(parser.tokenize('What is the airspeed of an unladen swallow?')))


# POS Tagger
pos_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='pos')
print(list(pos_tagger.tag('What is the airspeed of an unladen swallow ?'.split())))

# NER Tagger
ner_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')
print(list(ner_tagger.tag(('Rami Eid is studying at Stony Brook University in NY'.split()))))