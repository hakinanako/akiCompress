import os
import sys
from zlib import decompress

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from rich.console import Console
from console_reader import read_input_to_bytes
from tiny_compress import tiny_compress

import typer

app = typer.Typer()  # 创建一个 Typer 应用实例

# def launch_with_rich():
#     console = Console()
#
#     ascii_art = [
#         "                                              ,----,",
#         "   ,---,              ,-.                   .'   .`|",
#         "  '  .' \\         ,--/ /|    ,--,        .'   .'   ;   ,--,    ,-.----.",
#         " /  ;    '.     ,--. :/ |  ,--.'|      ,---, '    .' ,--.'|    \\    /  \\",
#         ":  :       \\    :  : ' /   |  |,       |   :     ./  |  |,     |   :    |",
#         ":  |   /\\   \\   |  '  /    `--'_       ;   | .'  /   `--'_     |   | .\\ :",
#         "|  :  ' ;.   :  '  |  :    ,' ,'|      `---' /  ;    ,' ,'|    .   : |: |",
#         "|  |  ;/  \\   \\ |  |   \\   '  | |        /  ;  /     '  | |    |   |  \\ :",
#         "'  :  | \\  \\ ,' '  : |. \\  |  | :       ;  /  /--,   |  | :    |   : .  |",
#         "|  |  '  '--'   |  | ' \\ \\ '  : |__    /  /  / .`|   '  : |__  :     |`-'",
#         "|  :  :         '  : |--'  |  | '.'| ./__;       :   |  | '.'| :   : :",
#         "|  | ,'         ;  |,'     ;  :    ; |   :     .'    ;  :    ; |   | :",
#         "`--''           '--'       |  ,   /  ;   |  .'       |  ,   /  `---'.|",
#         "                            ---`-'   `---'            ---`-'     `---`",
#         "©2025 akinanao. All rights reserved."
#     ]
#
#     colors = ["bold red", "bold yellow", "bold green", "bold cyan", "bold blue", "bold magenta"]
#
#     for i, line in enumerate(ascii_art):
#         console.print(line, style=colors[i % len(colors)])

@app.command()
def compress():
    """
    压缩输入的字符串。
    """
    console = Console()
    input_str = read_input_to_bytes("输入压缩字符串:")

    # Create an instance of tiny_compress
    compressor = tiny_compress()

    # Call the compress method
    compressed_data, index = compressor.compress(input_str)

    console.print(f"\n压缩结果: {compressed_data}", style="bold cyan")
    console.print(f"\n索引: {index}", style="bold cyan")

@app.command()
def decompress():
    pass

def main():
    app()

if __name__ == "__main__":
    main()