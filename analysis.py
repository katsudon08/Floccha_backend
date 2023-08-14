import spacy
from spacy.symbols import SPACE
import re

textBlock = [
    "for i in range(5):",
    "    print(i)",
    "    a = i"
]

def tokenize(textBlock):
    nlp = spacy.load("en_core_web_sm")
    reTokens = ""

    for text in textBlock:
        doc = nlp(text)
        for key, token in enumerate(doc):
            print(token, token.pos_)
            reToken = re.sub("\(", lambda x: f" {x.group()} ", token.text)
            # ) 単体の時はスペースを入れないようにする
            if token.text != ')':
                reToken = re.sub("\)", lambda x: f"{x.group()} ", reToken)
            reToken = re.sub("\%|\/", lambda x: f" {x.group()} ", reToken)
            if key == 0:
                reTokens += reToken
            else:
                reTokens += f" {reToken}"
            print(reTokens)

    return reTokens

text = tokenize(textBlock)

print(text)