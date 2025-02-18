
import logging
from datetime import datetime
import sys



from mtf import mtf
from rle import rle
from sais_bwt import sais_bwt

sys.setrecursionlimit(1500)

class tiny_compress:
    def __init__(self):
        # Set up logging
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            handlers=[
                logging.FileHandler(f'compression_log_{timestamp}.txt'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def banana():
        test_cases = [
            b"banana"
        ]
        for test in test_cases:
            compressed, index = tiny_compress().compress(test)
            decompressed = tiny_compress().decompress(compressed, index)
            assert decompressed == test, f"Test failed for input: {test}"

        print("Test passed!")

    def log_bytes(self, data: bytes, prefix: str = "", original_size: int = None):
        """Helper method to log byte data in both raw and hex formats"""
        self.logger.info(f"{prefix} (length: {len(data)})")
        self.logger.info(f"Raw: {data}")
        self.logger.info(f"Hex: {[hex(b) for b in data]}")
        if original_size is not None:
            percentage, ratio = self.calc_compression_ratio(original_size, len(data))
            self.logger.info(f"Compression Percentage: {percentage:.2f}% of original size")
            self.logger.info(f"Compression Ratio: {ratio:.2f}:1")
        self.logger.info("-" * 80)

    @staticmethod
    def calc_compression_ratio(original_size: int, compressed_size: int) -> tuple[float, float]:
        """
        Calculate compression ratio
        Returns: (percentage, ratio)
        percentage: compressed size as percentage of original
        ratio: original size / compressed size
        """
        percentage = (compressed_size / original_size) * 100
        ratio = original_size / compressed_size if compressed_size > 0 else float('inf')
        return percentage, ratio

    def compress(self, data: bytes) -> tuple[bytes, int]:
        self.logger.info("\nCOMPRESSION PROCESS")
        self.logger.info("=" * 80)

        original_size = len(data)
        self.log_bytes(data, "Input Data")

        bwt_encoded, index = sais_bwt.encode(data)
        self.log_bytes(bwt_encoded, "After BWT", original_size)

        mtf_encoded = mtf.encode(bwt_encoded)
        self.log_bytes(mtf_encoded, "After MTF", original_size)

        rel_encoded = rle.encode(mtf_encoded)
        self.log_bytes(rel_encoded, "After RLE", original_size)

        return rel_encoded, index

    def decompress(self, data: bytes, index: int) -> bytes:
        self.logger.info("\nDECOMPRESSION PROCESS")
        self.logger.info("=" * 80)

        self.log_bytes(data, "Input Compressed Data")

        rel_decoded = rle.decode(data)
        self.log_bytes(rel_decoded, "After RLE Decode")

        mtf_decoded = mtf.decode(rel_decoded)
        self.log_bytes(mtf_decoded, "After MTF Decode")

        bwt_decoded = sais_bwt.decode(mtf_decoded, index)
        self.log_bytes(bwt_decoded, "After BWT Decode")

        return bwt_decoded

    def _test_single_case(self, data: bytes):
        self.logger.info("\nCOMPRESSION TEST")
        self.logger.info("=" * 80)

        compressed, index = self.compress(data)
        decompressed = self.decompress(compressed, index)

        percentage, ratio = self.calc_compression_ratio(len(data), len(compressed))

        self.logger.info("\nCOMPRESSION RESULTS")
        self.logger.info("=" * 80)
        self.logger.info(f"Original size: {len(data)} bytes")
        self.logger.info(f"Compressed size: {len(compressed)} bytes")
        self.logger.info(f"Compression Percentage: {percentage:.2f}% of original size")
        self.logger.info(f"Compression Ratio: {ratio:.2f}:1")

        assert data == decompressed
        self.logger.info("Test passed! Original and decompressed data match.")

    # 测试
    def test(self):
        self.logger.info("Starting Compression Tests")
        self.logger.info("=" * 80)

        # Test case 1
        data = b"banana"
        self._test_single_case(data)

        # Test case 2
        data = b"abracadabra"
        self._test_single_case(data)

        self.logger.info("All tests passed!")
