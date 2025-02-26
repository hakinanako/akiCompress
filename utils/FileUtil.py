class FileUtile:

    @staticmethod
    def read_file(file_path: str) -> bytes:
        with open(file_path, 'rb') as file:
            return file.read()

    @staticmethod
    def write_file(file_path: str, data: bytes):
        with open(file_path, 'wb') as file:
            file.write(data)
