from datetime import datetime
from pickle import PROTO
from tempfile import tempdir

from compressor.MTF import MTF
from compressor.BWT import BWT
from compressor.Huffman import Huffman
from compressor.RLE import RLE
from utils.LogUtil import LogUtil


class Compression:

    @staticmethod
    def compress(data: bytes) -> bytes:
        LogUtil.log_with_datetime(f'-----------------Compression-----------------')


        LogUtil.log_with_datetime(f'original len({len(data)})')
        temp_time = datetime.now()
        bwt_compressed = BWT.bwt_encode(data)

        mtf_compressed = MTF.mtf_encode(bwt_compressed)
        LogUtil.log_with_datetime(f'mtf encode len({len(mtf_compressed)})')

        rle_compressed = RLE.rle_encode(mtf_compressed)
        LogUtil.log_with_datetime(f'rle encode len({len(rle_compressed)})')

        huffman_compressed = Huffman.huffman_encode(rle_compressed)
        LogUtil.log_with_datetime(f'huffman encode len({len(huffman_compressed)})')

        LogUtil.log_with_datetime(f'compression time:{(datetime.now() - temp_time).total_seconds():.2f} seconds')

        LogUtil.log_with_datetime(f'original_size:{len(data)},compressed_size:{len(huffman_compressed)}')
        LogUtil.log_with_datetime(f'compression ratio:{len(huffman_compressed)/len(data):.3f}')

        LogUtil.log_with_datetime(f'-----------------Compression-----------------')

        return huffman_compressed

    @staticmethod
    def decompress(data: bytes) -> bytes:

        LogUtil.log_with_datetime(f'-----------------Decompression-----------------')

        LogUtil.log_with_datetime(f'original len({len(data)})')

        temp_time = datetime.now()

        huffman_decoded = Huffman.huffman_decode(data)
        LogUtil.log_with_datetime(f'huffman decode len({len(huffman_decoded)})')

        rle_decoded = RLE.rle_decode(huffman_decoded)
        LogUtil.log_with_datetime(f'rle decode len({len(rle_decoded)})')

        mtf_decoded = MTF.mtf_decode(rle_decoded)
        LogUtil.log_with_datetime(f'mtf decode len({len(mtf_decoded)})')

        bwt_decoded = BWT.bwt_decode(mtf_decoded)
        LogUtil.log_with_datetime(f'bwt decode len({len(bwt_decoded)})')

        LogUtil.log_with_datetime(f'decompression time:{(datetime.now() - temp_time).total_seconds():.2f} seconds')
        LogUtil.log_with_datetime(f'-----------------Decompression-----------------')

        return bwt_decoded

    @staticmethod
    def compress_file(input_file: str, output_file: str):
        with open(input_file, 'rb') as file:
            data = file.read()
        compressed_data = Compression.compress(data)
        with open(output_file, 'wb') as file:
            file.write(compressed_data)

    @staticmethod
    def decompress_file(input_file: str, output_file: str):
        with open(input_file, 'rb') as file:
            data = file.read()
        decompressed_data = Compression.decompress(data)
        with open(output_file, 'wb') as file:
            file.write(decompressed_data)
