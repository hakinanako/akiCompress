
from mtf import mtf
from rle import rle
from bwt import bwt#  Assuming rle is another module you have

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
        self.log_bytes(bwt_encoded, "After BWT", original_size)

        mtf_encoded = mtf.encode(bwt_encoded)
        self.log_bytes(mtf_encoded, "After MTF", original_size)

        rel_encoded = rle.encode(mtf_encoded)
        self.log_bytes(rel_encoded, "After RLE", original_size)

        return rel_encoded

    def decompress(self, data: bytes) -> bytes:
        self.logger.info("\nDECOMPRESSION PROCESS")
        self.logger.info("=" * 80)

        self.log_bytes(data, "Input Compressed Data")

        rel_decoded = rle.decode(data)
        self.log_bytes(rel_decoded, "After RLE Decode")

        mtf_decoded = mtf.decode(rel_decoded)
        self.log_bytes(mtf_decoded, "After MTF Decode")

        bwt_decoded = bwt.decode(mtf_decoded)
        self.log_bytes(bwt_decoded, "After BWT Decode")

        return bwt_decoded


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

        data = b"banana"*100+b"apple"+b"banana"*100
        self._test_single_case(data)

        self.logger.info("All tests passed!")

if __name__ == '__main__':
    # 测试串的压缩和解压缩
    compressor = tiny_compress()
    compressor.test()
