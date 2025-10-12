from interpreter.tokenizer import lexer
from interpreter.parser import parser

print('Check Parser Debug file')

while True:
    data = input("Enter command: ")
    if data == "exit":
        break

    lexer.input(data)

    for tok in lexer:
        print(tok)
    out = parser.parse(data)
    print(out)
