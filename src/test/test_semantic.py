from interpreter.tokenizer import lexer
from interpreter.parser import parser
from interpreter.semantic_analyzer import valid_semantics
print('Check Parser Debug file')

while True:
    data = input("Enter command: ")
    if data == "exit":
        break

    lexer.input(data)

    for tok in lexer:
        print(tok)
    out = parser.parse(data)
    x = valid_semantics(out)
    print(x)
    print(out)

    #use 5h to change suit of 9c use 