import interpreter.core as core


while True:
    data = input("Enter command: ")
    if data == "exit":
        break

    out = core.interpret_command(data, None)
    print(out)
