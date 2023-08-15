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
    reTokensText = ""

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
                reTokensText += reToken
            else:
                reTokensText += f" {reToken}"
            print(reTokensText)

    reTokens = nlp(reTokensText)
    return reTokens

tokens = tokenize(textBlock)

for token in tokens:
    print(token)



def nestBlocking(text):
    prev_spaceNum = 0
    current_spaceNum = 0

    if text[0].pos == SPACE:
        raise ValueError