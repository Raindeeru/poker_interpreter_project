from interpreter.tokenizer import lexer

while True:
    data = input("Enter command: ")
    if data == "exit":
        break

    lexer.input(data)

    for tok in lexer:
        print(tok)

    
