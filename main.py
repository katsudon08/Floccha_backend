import spacy
from spacy.symbols import SYM, PUNCT, SPACE
import keyword
import re

tokens = []


# トークン化
def tokeninze(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    firstTokens = ""
    print("BEFORE-----")
    for token in doc:
        print(token.text, token.pos_)
        reTokenText = re.sub("\(", lambda x: f" {x.group()} ", token.text)
        reTokenText = re.sub("\)", lambda x: f"{x.group()} ", reTokenText)
        reTokenText = re.sub("\%|\/", lambda x: f" {x.group()} ", reTokenText)
        firstTokens += f" {reTokenText}"
        print(firstTokens)

    secondTokens = nlp(firstTokens)
    print("AFTER------")
    for token in secondTokens:
        if token.text == "%":
            token.pos = SYM
        tokens.append(token)
        print(token.text, token.pos_)

    for i in tokens:
        print(i)


tokeninze(
    """
for i in range(5):
    print(i)
"""
)
del tokens[0]


# 抽象構文木生成、意味解析
class ASTNode:
    def __init__(self, value="VALUE"):
        self.value = value
        self.children = []

    def printNode(self):
        print("value:", self.value)
        print("children:", self.children, "\n")


astNodes = []
for token in tokens:
    if token.pos == SPACE:
        continue
    astNodes.append(ASTNode(token.text))

for astNode in astNodes:
    astNode.printNode()

# 予約語一覧
print(keyword.kwlist)


# 中間表現
class MidRep:
    def __init__(self, id, x, y, label):
        self.id = id
        self.position = {"x": x, "y": y}
        self.data = {"label": label}

    def printMidRep(self):
        print(self.id)
        print(self.position)
        print(self.data)

class MidRepEdge(MidRep):
    def __init__(self, id, x, y, label, targetId):
        super().__init__(id, x, y, label)
        self.source = id
        self.target = targetId

    def printMidRepEdge(self):
        super().printMidRep()
        print(self.source)
        print(self.targetf)

def makeLabel(key):
    keyCopy = key + 1
    label = ""
    while astNodes[keyCopy].value != ":":
        label += astNodes[keyCopy].value + " "
        keyCopy += 1
    return label

# 字句から直接中間表現を作成しちゃおう
for key, astNode in enumerate(astNodes):
    match astNode.value:
        case "for":
            label = makeLabel(key)
            startMidRep = MidRep("for_start", 0, 100, label)
            endMidRep = MidRep("for_end", 0, 200, " ")
            # 中の表現をstartとendの間につなぐ必要がある
            startMidRep.printMidRep()
            endMidRep.printMidRep()
        case "while":
            label = makeLabel(key)
            # EdgeVERにする
            loopMidRep = MidRep("while", 0, 100, label)
            loopMidRep.printMidRep()
        case "if":
            label = makeLabel(key)
            # EdgeVERにする
            branchMidRep = MidRep("if", 0, 100, label)
            branchMidRep.printMidRep()

# 一旦様子見
"""keywordNodes = []
unkeywordNodes = []
kwNum = 0

for key, astNode in enumerate(astNodes):
    if astNode.value in keyword.kwlist:
        match astNode.value:
            case "for":
                kwNum = key
                # 変数
                while astNodes[kwNum + 1].value != "in":
                    kwNum += 1
                    astNode.children.append(astNodes[kwNum].value)
                # イテラブルシーケンス

                # rangeの場合
                call = ASTNode("call")
                kwNum += 1
                astNode.children.append(astNodes[kwNum].value)
                kwNum += 1
                astNodes[kwNum].children.append(astNodes[kwNum].value)
                astNodes[kwNum].children.append(call.value)
                kwNum += 1
                call.children.append(astNodes[kwNum].value)
                call.children.append(astNodes[kwNum + 1].value)


                # それ以外の場合
                print([i.children for i in astNodes])
                # enumerateが原因でバグ発生？
                for key, astNode in enumerate(astNodes):
                    print(astNode.children)
                    if astNode.children == []:
                        astNodes.pop(key)
            # case "in":

for astNode in astNodes:
    astNode.printNode()
call.printNode()"""

# 中間表現の生成
