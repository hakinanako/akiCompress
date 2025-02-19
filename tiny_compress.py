from mtf import mtf
from rle import rle
from bwt import bwt  # Assuming rle is another module you have
from huffman import huffman

class tiny_compress:
    def __init__(self):
        self.logger = self.setup_logger()

    def setup_logger(self):
        import logging
        logger = logging.getLogger('tiny_compress')
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def log_bytes(self, data: bytes, description: str, original_size: int = None):
        self.logger.info(f"{description}: {data[:50]}{'...' if len(data) > 50 else ''} ({len(data)} bytes)")

    def compress(self, data: bytes) -> bytes:
        self.logger.info("\nCOMPRESSION PROCESS")
        self.logger.info("=" * 80)

        original_size = len(data)
        self.log_bytes(data, "Input Data")

        bwt_encoded = bwt.encode(data)
        self.log_bytes(bwt_encoded, "After BWT")

        mtf_encoded = mtf.encode(bwt_encoded)
        self.log_bytes(mtf_encoded, "After MTF", original_size)

        rel_encoded = rle.encode(mtf_encoded)
        self.log_bytes(rel_encoded, "After RLE", original_size)

        huffman_coded = huffman.encode(rel_encoded)
        self.log_bytes(huffman_coded, "After Huffman", original_size)


        compressed_size = len(huffman_coded)
        compression_ratio = compressed_size / original_size
        self.logger.info(f"Compression ratio: {compression_ratio:.2f}")
        print(f"Compression ratio: {compression_ratio:.2f}")  # Output to console

        return huffman_coded

    def decompress(self, data: bytes) -> bytes:
        self.logger.info("\nDECOMPRESSION PROCESS")
        self.logger.info("=" * 80)

        self.log_bytes(data, "Input Compressed Data")

        huffman_decoded = huffman.decode(data)
        self.log_bytes(huffman_decoded, "After Huffman Decode")

        rel_decoded = rle.decode(huffman_decoded)
        self.log_bytes(rel_decoded, "After RLE Decode")

        mtf_decoded = mtf.decode(rel_decoded)
        self.log_bytes(mtf_decoded, "After MTF Decode")

        bwt_decoded = bwt.decode(mtf_decoded)
        self.log_bytes(bwt_decoded, "After BWT Decode")

        return bwt_decoded

    def compress_file(self, input_file: str, output_file: str):
        self.logger.info(f"\nCompressing file: {input_file}")
        self.logger.info("=" * 80)

        with open(input_file, 'rb') as file:
            data = file.read()

        compressed_data = self.compress(data)

        with open(output_file, 'wb') as file:
            file.write(compressed_data)

        self.logger.info(f"File compressed successfully and saved as: {output_file}")

        # 文件解压缩

    def decompress_file(self, input_file: str, output_file: str):
        self.logger.info(f"\nDecompressing file: {input_file}")
        self.logger.info("=" * 80)

        with open(input_file, 'rb') as file:
            compressed_data = file.read()

        decompressed_data = self.decompress(compressed_data)

        with open(output_file, 'wb') as file:
            file.write(decompressed_data)

        self.logger.info(f"File decompressed successfully and saved as: {output_file}")

    def _test_single_case(self, data: bytes):
        self.logger.info("\nCOMPRESSION TEST")
        self.logger.info("=" * 80)

        compressed = self.compress(data)
        decompressed = self.decompress(compressed)

        self.logger.info("\nCOMPRESSION RESULTS")
        self.logger.info("=" * 80)
        self.logger.info(f"Original size: {len(data)} bytes")
        self.logger.info(f"Compressed size: {len(compressed)} bytes")

        assert data == decompressed
        self.logger.info("Test passed! Original and decompressed data match.")

    def test(self):
        self.logger.info("Starting Compression Tests")
        self.logger.info("=" * 80)

        data = b"""
from mtf import mtf"""

        self._test_single_case(data)

        self.logger.info("All tests passed!")

if __name__ == '__main__':
    # 测试串的压缩和解压缩
    compressor = tiny_compress()
    # compressor.test()
#     测试文件的压缩和解压缩
#     compressor.test_file("test.txt")
    compressor.compress_file('test.txt', 'test_compressed.bin')
    compressor.decompress_file('test_compressed.bin', 'test_decompressed.txt')
    assert open('test.txt', 'rb').read() == open('test_decompressed.txt', 'rb').read()
    print("Test passed! Original and decompressed file match.")