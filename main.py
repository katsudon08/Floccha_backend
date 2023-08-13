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
        # ) 単体の時はスペースを入れないようにする
        if token.text != ')':
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

# 改行の数だけ、スペースの数が増えてしまう
tokeninze("""
for i in range(5):
    print(i)
    a = i
""")
del tokens[0]

# 抽象構文木生成、意味解析
class ASTNode:
    def __init__(self, value="VALUE"):
        self.value = value
        self.children = []

    def printNode(self):
        print("value:", self.value)
        print("children:", self.children, "\n")

    def __str__(self):
        return f"value: {self.value}"

print("SPACE調整")

prev_spaceNum = None
current_spaceNum = 0

block = []
# 作り変え
blockAstNodes = []
astNodes = []

astNewTokens = []
newTokens = []

num = 0

for token in tokens:
    # astNodes.append(ASTNode(token.text))
    newTokens.append(token.text)

for key, token in enumerate(tokens):
    print(token.text)
    # 改行とスペースの区別をつける必要がある
    # !スペースの数が同じだったら同じブロックである判定を出す

    prevKey = key - 1
    if token.pos == SPACE:
        # if len(tokens) - 1 == key:
        #         print("削除作業実行")
        #         for astNode in astNodes:
        #             if astNode.value in block:
        #                 print(astNode)
        #                 astNodes.remove(astNode)
        #         for astBlock in block:
        #             blockAstNodes.append(ASTNode(astBlock))
        #         astNodes.append(blockAstNodes)
        #         blockAstNodes = []
        #         block = []
        continue
    elif tokens[prevKey].pos == SPACE and key != 0:
        print("該当文字:", token)
        print("スペース:", len(tokens[prevKey].text) - 2)

        prev_spaceNum = current_spaceNum
        current_spaceNum = len(tokens[prevKey].text) - 2

# !後で関数化を行うこと
        if prev_spaceNum != current_spaceNum:
            if current_spaceNum != 0:
                keyCopy = key - num
                print("keyCopy", keyCopy)
                while tokens[keyCopy].pos != SPACE:
                    block.append(tokens[keyCopy].text)
                    newTokens.pop(num)
                    print(block)
                    keyCopy += 1
                num = key - (keyCopy - key)
                print(block)
            else:
                pass
                # print("削除作業実行")
                # for astNode in astNodes:
                #     if astNode.value in block:
                #         astNodes.remove(astNode)
                # for astBlock in block:
                #     blockAstNodes.append(ASTNode(astBlock))
                # astNodes.append(blockAstNodes)
                # blockAstNodes = []
                # block = []
        elif prev_spaceNum == current_spaceNum and current_spaceNum != 0:
            keyCopy = key - num
            print("keyCopy", keyCopy)
            while tokens[keyCopy].pos != SPACE:
                block.append(tokens[keyCopy].text)
                newTokens.pop(num)
                print(block)
                keyCopy += 1
            num = key - (keyCopy - key)
            print(block)

    print("prev:", prev_spaceNum, "current:", current_spaceNum)


print("デバッグ開始")

# for astNode in astNodes:
#     if type(astNode) == list:
#         for i in astNode:
#             print(i.value)
#             i.printNode()
#     else:
#         astNode.printNode()

for newToken in newTokens:
    if type(newToken) == list:
        for i in newToken:
            print(i)
    else:
        print(newToken)

# print(astNodes)

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

# nodeとedgeの要素を含む
class MidRepNode:
    def __init__(self, id, x, y, label):
        self.id = id
        self.position = {'x': x, 'y': y}
        self.data = {"label": label}
        self.edgeId = "edge-" + id
        self.source = None
        self.target = None

    def printMidRep(self):
        print("id:", self.id)
        print("position:", self.position)
        print("data:", self.data)
        print("edge-id:", self.edgeId)
        print("source:", self.source)
        print("target:", self.target, "\n")

def makeLabel(key):
    keyCopy = key + 1
    label = ""
    while astNodes[keyCopy].value != ":":
        label += astNodes[keyCopy].value + " "
        keyCopy += 1
    return label

midReps = []
variables = []
contents = []

startMidRep = MidRepNode("start", 0, 0, "開始")
endMidRep = MidRepNode("end", 0, None, "終了")

midReps.append(startMidRep)
startMidRep.printMidRep()
endMidRep.printMidRep()

# 字句から直接中間表現を作成しちゃおう
for key, astNode in enumerate(astNodes):
    match astNode.value:
        case '=':
            variable = astNodes[key - 1].value
            content = astNodes[key + 1].value
            variableMidRep = MidRepNode("variable-" + variable, 0, None, "変数 " + variable + " に " + content + " を代入")
            variables.append(variable)
            contents.append(content)
            midReps.append(variableMidRep)

            variableMidRep.printMidRep()
        case "for":
            label = makeLabel(key)
            #* 前の要素の高さに+100した高さにする必要がある
            if astNodes[0]:
                forStartMidRep = MidRepNode("for_start", 0, 100, label)
            else:
                forStartMidRep = MidRepNode("for_start", 0, None, label)
            forEndMidRep = MidRepNode("for_end", 0, None, "")

            # 中の表現をstartとendの間につなぐ必要がある
            forStartMidRep.source = forStartMidRep.id
            forStartMidRep.target = forEndMidRep.id

            forEndMidRep.source = forEndMidRep.id
            forEndMidRep.target = forStartMidRep.id

            midReps.append(forStartMidRep)
            midReps.append(forEndMidRep)
            forStartMidRep.printMidRep()
            forEndMidRep.printMidRep()

        case "while":
            label = makeLabel(key)
            # EdgeVERにする
            loopMidRep = MidRepNode("while", 0, None, label)

            midReps.append(loopMidRep)
            loopMidRep.printMidRep()

        case "if":
            label = makeLabel(key)
            # EdgeVERにする
            branchMidRep = MidRepNode("if", 0, None, label)

            midReps.append(branchMidRep)
            branchMidRep.printMidRep()

midReps.append(endMidRep)

for key, midRep in enumerate(midReps):
    if midRep.position['y'] == None:
        midRep.position['y'] = key * 100

print("AFTER")

for midRep in midReps:
    midRep.printMidRep()

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