import typer
import os

from compressor.Compressor import Compression

app = typer.Typer()

@app.command()
def compress(input_file: str, output_file: str):
    if not os.path.exists(input_file):
        raise typer.BadParameter(f"Input file {input_file} does not exist.")

    typer.echo(f"Compressing file: {input_file}")
    Compression.compress_file(input_file, output_file)
    typer.echo(f"Compressed file saved to: {output_file}")


@app.command()
def decompress(input_file: str, output_file: str):

    if not os.path.exists(input_file):
        raise typer.BadParameter(f"Input file {input_file} does not exist.")

    typer.echo(f"Decompressing file: {input_file}")
    Compression.decompress_file(input_file, output_file)
    typer.echo(f"Decompressed file saved to: {output_file}")


if __name__ == "__main__":
    app()
