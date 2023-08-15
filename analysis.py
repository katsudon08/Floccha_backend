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

print("-----tokenize-----")

tokens = tokenize(textBlock)

for token in tokens:
    print(token, token.pos_)

def nesting(tokens):
    if tokens[0].pos == SPACE:
        raise ValueError

    midRepTokens = []

    nestKey = None
    prev_spaceNum = 0
    current_spaceNum = 0

    for key, token in enumerate(tokens):
        print(token.text)
        if token.pos == SPACE:
            prev_spaceNum = current_spaceNum
            current_spaceNum = len(token.text)
            print("スペース:", current_spaceNum)
            continue
        # ネストが同じとき
        elif current_spaceNum == prev_spaceNum and current_spaceNum != 0:
            midRepTokens[nestKey].append(token.text)
            midRepTokens.append(None)
            continue
        # ネストが一つ深くなった時
        if current_spaceNum > prev_spaceNum:
            nestKey = key - 1
            midRepTokens.append([token.text])
            continue
        # ネストが終わった時
        elif current_spaceNum < prev_spaceNum:
            nestKey = None
        midRepTokens.append(token.text)

    # midRepTokens = list(filter(None, midRepTokens))
    return midRepTokens

print("-----nesting-----")

nestedTokens = nesting(tokens)

print("ネスト後")
for token in nestedTokens:
    print(token)