
import logging
import os
from datetime import datetime
import sys



from mtf import mtf
from bwt import bwt
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
        # 用原生bwt实现
        # bwt_encoded, index = bwt.encode(data)
        rel_encoded = rle.encode(bwt_encoded)
        # self.log_bytes(rel_encoded, "After RLE", original_size)

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

        # bwt_decoded = bwt.decode(mtf_decoded, index)

        return bwt_decoded

    def file_compress(self, file_path: str):
        # 读取文件 转换成字节流，进行压缩
        with open(file_path, 'rb') as f:
            data = f.read()
        compressed, index = self.compress(data)

        # 保存压缩后的文件和索引 其中索引用文件头的方式保存，文件头还有原始文件的长度
        compressed_file_path = file_path + '.compressed'
        with open(compressed_file_path, 'wb') as f:
            # 写入原始文件长度和索引
            f.write(len(data).to_bytes(4, 'big'))
            f.write(index.to_bytes(4, 'big'))
            # 写入压缩数据
            f.write(compressed)

    def file_decompress(self, compressed_file_path: str):
        # 读取压缩文件
        with open(compressed_file_path, 'rb') as f:
            # 读取原始文件长度和索引
            original_size = int.from_bytes(f.read(4), 'big')
            index = int.from_bytes(f.read(4), 'big')
            # 读取压缩数据
            compressed_data = f.read()

        # 解压缩数据
        decompressed_data = self.decompress(compressed_data, index)

        # 保存解压缩后的文件
        decompressed_file_path = compressed_file_path.replace('.compressed', '.decompressed')
        with open(decompressed_file_path, 'wb') as f:
            f.write(decompressed_data)


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

    @staticmethod
    def test_file_compression():
        compressor = tiny_compress()

        # Create a sample file to compress
        sample_file_path = 'compression_log_20250218_183239.txt'
        # with open(sample_file_path, 'wb') as f:
        #     f.write(b'This is a test file for compression and decompression.')

        # Compress the file
        compressor.file_compress(sample_file_path)
        compressed_file_path = sample_file_path + '.compressed'

        # Check if the compressed file exists
        assert os.path.exists(compressed_file_path), "Compressed file was not created."

        # Decompress the file
        compressor.file_decompress(compressed_file_path)
        decompressed_file_path = compressed_file_path.replace('.compressed', '.decompressed')

        # Check if the decompressed file exists
        assert os.path.exists(decompressed_file_path), "Decompressed file was not created."

        # Verify the content of the decompressed file
        with open(decompressed_file_path, 'rb') as f:
            decompressed_data = f.read()
        with open(sample_file_path, 'rb') as f:
            original_data = f.read()

        assert decompressed_data == original_data, "Decompressed data does not match the original data."

        print("File compression and decompression test passed!")

    # 测试
    def test(self):
        self.logger.info("Starting Compression Tests")
        self.logger.info("=" * 80)

        # Test case 2
        # data = b"banana"
        # self._test_single_case(data)

        data = b"banana"
        self._test_single_case(data)

        self.logger.info("All tests passed!")
# 测试
if __name__ == '__main__':
    # tiny_compress().test()
    tiny_compress().test_file_compression()
