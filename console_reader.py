def read_input_to_bytes(prompt: str = "Enter text: ", delimiter: str = "\n") -> bytes:
    """
    Read user input from the console and convert it to a byte stream.
    """
    user_input = input(prompt + delimiter)
    return user_input.encode('utf-8')

def read_input_lines_to_bytes(prompt: str = "Enter text (type 'END' on a new line to finish):", delimiter: str = "\n") -> bytes:
    """
    Read multiple lines of user input from the console and convert them to a byte stream.
    """
    print(prompt)
    lines = []
    while True:
        line = input()
        if line == 'END':
            break
        lines.append(line)
    return delimiter.join(lines).encode('utf-8')