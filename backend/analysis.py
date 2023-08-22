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

def nesting(tokens):
    if tokens[0].pos == SPACE:
        raise ValueError

    midRepTokens = []

    nestKey = None
    prev_spaceNum = 0
    current_spaceNum = 0

    for key, token in enumerate(tokens):
        print(token.text)
        print(prev_spaceNum, current_spaceNum)
        if token.pos == SPACE:
            prev_spaceNum = current_spaceNum
            current_spaceNum = len(token.text)
            print("スペース:", current_spaceNum)
            midRepTokens.append(None)
            continue
        # ネストが同じとき
        elif current_spaceNum == prev_spaceNum and current_spaceNum != 0:
            midRepTokens[nestKey].append(token.text)
            midRepTokens.append(None)
            continue
        # ネストが一つ深くなった時
        if current_spaceNum > prev_spaceNum:
            if tokens[key - 1].pos == SPACE:
                midRepTokens.append([token.text])
                nestKey = key
            else:
                midRepTokens[nestKey].append(token.text)
            continue
        # ネストが終わった時
        elif current_spaceNum < prev_spaceNum:
            nestKey = None
        midRepTokens.append(token.text)

    midRepTokens = list(filter(None, midRepTokens))
    return midRepTokens

class MidRep:
    def __init__(self, id, x, y, label):
        self.id = id
        self.position = {'x': x, 'y': y}
        self.data = {"label": label}
        self.edgeId = "edge-" + id
        self.source = None
        self.target = None

    def __str__(self):
        r = ""
        r += "id: " + self.id + "\n"
        r += "pos: " + str(self.position) + "\n"
        r += "data: " + str(self.data) + "\n"
        r += "edge-id: " + self.edgeId + "\n"
        r += "src: " + str(self.source) + "\n"
        r += "trg: " + str(self.target) + "\n"

        return r

def makeLabel(tokens, key):
    key = key + 1
    label = ""
    while tokens[key] != ':':
        label += tokens[key] + ' '
        key += 1
    return label

def makeSentenceMidRep(midReps, tokens):
    variables = []
    contents = []

    for key, token in enumerate(tokens):
        if type(token) == list:
            # リスト時の処理を記述すること
            continue
        else:
            match token:
                case '=':
                    variable = token[key - 1]
                    content = token[key + 1]

                    variableMidRep = MidRep(f"variable-{variable}", 0, None, f"変数 {variable} に {content} を代入")

                    variables.append(variable)
                    contents.append(content)
                    midReps.append(variableMidRep)

                    print(variableMidRep)

                case "for":
                    label = makeLabel(tokens, key)
                    # 前要素の高さに+100した高さにする必要がある
                    forStartMidRep = MidRep("for_start", 0, None, label)
                    forEndMidRep = MidRep("for_end", 0, None, "")

                    keyCopy = key
                    while type(tokens[keyCopy]) != list:
                        keyCopy += 1

                    print(keyCopy)
                    print(tokens[keyCopy])

                    # 中の表現をstartとendの間につなぐ必要がある
                    forStartMidRep.source = forStartMidRep.id
                    forStartMidRep.target = forEndMidRep.id

                    forEndMidRep.source = forEndMidRep.id
                    forEndMidRep.target = forStartMidRep.id

                    midReps.append(forStartMidRep)
                    midReps.append(forEndMidRep)

                    print(forStartMidRep)
                    print(forEndMidRep)

                case "while":
                    label = makeLabel(tokens, key)
                    loopMidRep = MidRep("while", 0, None, label)

                    midReps.append(loopMidRep)

                    print(loopMidRep)

                case "if":
                    label = makeLabel(tokens, key)
                    branchMidRep = MidRep("if", 0, None, label)

                    midReps.append(branchMidRep)

                    print(branchMidRep)

def makeMidRep(midReps, nestedTokens):
    startMidRep = MidRep("start", 0, None, "開始")
    midReps.append(startMidRep)

    makeSentenceMidRep(midReps, nestedTokens)

    endMidRep = MidRep("end", 0, None, "終了")
    midReps.append(endMidRep)

    for key, midRep in enumerate(midReps):
        midRep.position['y'] = key * 100

def execute():
    print("-----tokenize-----")

    tokens = tokenize(textBlock)

    for token in tokens:
        print(token, token.pos_)


    print("-----nesting-----")

    # このトークンは型がstringになっている
    nestedTokens = nesting(tokens)

    print("ネスト後\n")
    for token in nestedTokens:
        print(token)

    midReps = []

    makeMidRep(midReps, nestedTokens)

    print("-----makeMidRep-----")

    for midRep in midReps:
        print(midRep)

    return midReps

if __name__ == "__main__":
    execute()