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
        if token.text == '%':
            token.pos = SYM
        tokens.append(token)
        print(token.text, token.pos_)

    for i in tokens:
        print(i)

tokeninze("""
for i in range(5):
    print(i)
""")
del tokens[0]

# 抽象構文木生成、意味解析
class ASTNode:
    def __init__(self, value="VALUE"):
        self.value = value
        self.children = []

    def printNode(self):
        print("value:", self.value)
        print("children:",  self.children, "\n")

astNodes = []
for token in tokens:
    if token.pos in [PUNCT, SPACE]:
        continue
    astNodes.append(ASTNode(token.text))

for astNode in astNodes:
    astNode.printNode()

# 予約語一覧
print(keyword.kwlist)

keywordNodes = []
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
call.printNode()

"""# 抽象構文木のノードを表すクラス
class ASTNode:
    def __init__(self, value):
        self.value = value
        self.children = []

# 構文解析器の実装
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def parse(self):
        return self.parse_expression()

    def parse_expression(self):
        left = self.parse_term()
        while self.match('+') or self.match('-'):
            operator = self.previous()
            right = self.parse_term()
            node = ASTNode(operator.lexeme)
            node.children.append(left)
            node.children.append(right)
            left = node
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.match('*') or self.match('/'):
            operator = self.previous()
            right = self.parse_factor()
            node = ASTNode(operator.lexeme)
            node.children.append(left)
            node.children.append(right)
            left = node
        return left

    def parse_factor(self):
        if self.match('number'):
            return ASTNode(self.previous().lexeme)
        elif self.match('('):
            node = self.parse_expression()
            self.consume(')', "Expect ')' after expression.")
            return node
        else:
            raise Exception("Unexpected token: " + self.peek().lexeme)

    def match(self, token_type):
        if self.check(token_type):
            self.advance()
            return True
        return False

    def check(self, token_type):
        return self.peek().type == token_type

    def advance(self):
        if not self.is_at_end():
            self.index += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == 'EOF'

    def peek(self):
        return self.tokens[self.index]

    def previous(self):
        return self.tokens[self.index - 1]

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        raise Exception(message)


class Token:
    def __init__(self, type, lexeme):
        self.type = type
        self.lexeme = lexeme

# トークン列を定義
tokens = [
    Token('number', '3'),
    Token('+', '+'),
    Token('number', '5'),
    Token('*', '*'),
    Token('(', '('),
    Token('number', '2'),
    Token('-', '-'),
    Token('number', '8'),
    Token(')', ')'),
]

# 構文解析器を初期化してASTを生成
parser = Parser(tokens)
ast = parser.parse()"""


# 中間表現の生成



