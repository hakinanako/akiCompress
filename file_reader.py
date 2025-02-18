import os


class file_reader:


    """读取转为字节流"""
    @staticmethod
    def read_file_to_bytes(file_path: str) -> bytes:

        with open(file_path, "rb") as f:
            return f.read()

    """写入字节流"""
    @staticmethod
    def write_bytes_to_file(data: bytes, file_path: str):
        with open(file_path, "wb") as f:
            f.write(data)

    """获取文件大小"""
    @staticmethod
    def get_file_size(file_path: str) -> int:
        return os.path.getsize(file_path)

    """分块读入文件"""
    @staticmethod
    def read_file_in_chunks(file_path: str, chunk_size: int = 1024) -> bytes:
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    """分块写入文件"""
    @staticmethod
    def write_chunks_to_file(chunks, file_path: str):
        with open(file_path, "wb") as f:
            for chunk in chunks:
                f.write(chunk)

    """文件/目录是否存在"""
    @staticmethod
    def file_exists(file_path: str) -> bool:
        return os.path.exists(file_path)

