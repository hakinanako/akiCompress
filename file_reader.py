import os

class file_reader:

    @staticmethod
    def read_file_to_bytes(file_path: str) -> bytes:

        with open(file_path, "rb") as f:
            return f.read()

    @staticmethod
    def write_bytes_to_file(data: bytes, file_path: str):
        with open(file_path, "wb") as f:
            f.write(data)

    @staticmethod
    def get_file_size(file_path: str) -> int:
        return os.path.getsize(file_path)

    @staticmethod
    def read_file_in_chunks(file_path: str, chunk_size: int = 1024) -> bytes:
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    @staticmethod
    def write_chunks_to_file(chunks, file_path: str):
        with open(file_path, "wb") as f:
            for chunk in chunks:
                f.write(chunk)

    @staticmethod
    def file_exists(file_path: str) -> bool:
        return os.path.exists(file_path)

