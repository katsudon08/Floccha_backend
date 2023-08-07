import spacy
import keyword
import re

def tokeninze(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    firstTokens = ""
    for token in doc:
        reTokenText = re.sub("\(", lambda x: f" {x.group()} ", token.text)
        reTokenText = re.sub("\)", lambda x: f"{x.group()} ", reTokenText)
        firstTokens += f" {reTokenText}"
        print(firstTokens)

tokeninze("""
for i in range(5):
    print(i)
""")

