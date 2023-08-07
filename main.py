import spacy

def codeParser(text):
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(text)
    for token in doc:
        print(token.text, token.pos_)

codeParser("""
for i in range(5):
    print(i)
           """)