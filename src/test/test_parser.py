from interpreter.parser import shift_reduce
from interpreter.tokenizer import lexer

while True:
    data = input("Enter command: ")
    if data == "exit":
        break

    lexer.input(data)
    tokens = list(lexer)
    for tok in tokens:
        print(tok)
    stack = shift_reduce(tokens)


    print(stack)

#use 10h to change suit of qs to 10