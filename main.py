import spacy

nlp = spacy.load("en_core_web_sm")

doc = nlp("int num( int n ) { return n; }")
for token in doc:
    print(token.text, token.pos_, token.dep_)

print(doc)