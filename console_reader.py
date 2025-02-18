class console_reader:
    @staticmethod
    def read_input_to_bytes() -> bytes:
        """
        Read user input from the console and convert it to a byte stream.
        """
        user_input = input("Enter text: ")
        return user_input.encode('utf-8')

    @staticmethod
    def read_input_lines_to_bytes() -> bytes:
        """
        Read multiple lines of user input from the console and convert them to a byte stream.
        """
        print("Enter text (type 'END' on a new line to finish):")
        lines = []
        while True:
            line = input()
            if line == 'END':
                break
            lines.append(line)
        return '\n'.join(lines).encode('utf-8')