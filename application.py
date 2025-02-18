import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from tiny_compress import tiny_compress
import typer



def main():
    print("Hello World")
    tiny_compress.banana()

# 文件压缩


if __name__ == "__main__":
    tiny_compress.banana()
    typer.run(main)