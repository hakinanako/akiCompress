import time
import os

from compressor.Compressor import Compression

class Benchmark:

    @staticmethod
    def time_compress(data: bytes) -> float:

        start_time = time.time()
        Compression.compress(data)
        end_time = time.time()
        return end_time - start_time

    @staticmethod
    def time_decompress(data: bytes) -> float:

        start_time = time.time()
        Compression.decompress(data)
        end_time = time.time()
        return end_time - start_time

    @staticmethod
    def file_size(file_path: str) -> int:

        return os.path.getsize(file_path)

    @staticmethod
    def benchmark_compress(data: bytes) -> dict:

        original_size = len(data)
        compression_time = Benchmark.time_compress(data)
        compressed_data = Compression.compress(data)
        compressed_size = len(compressed_data)

        return {
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_time': compression_time
        }

    @staticmethod
    def benchmark_decompress(data: bytes) -> dict:

        decompression_time = Benchmark.time_decompress(data)
        decompressed_data = Compression.decompress(data)
        decompressed_size = len(decompressed_data)

        return {
            'decompressed_size': decompressed_size,
            'decompression_time': decompression_time
        }

    @staticmethod
    def benchmark_file_compression(input_file: str, output_file: str) -> dict:

        with open(input_file, 'rb') as file:
            data = file.read()

        benchmark_results = Benchmark.benchmark_compress(data)

        Compression.compress_file(input_file, output_file)

        original_size = Benchmark.file_size(input_file)
        compressed_size = Benchmark.file_size(output_file)

        benchmark_results.update({
            'original_file_size': original_size,
            'compressed_file_size': compressed_size
        })

        return benchmark_results

    @staticmethod
    def benchmark_file_decompression(input_file: str, output_file: str) -> dict:

        with open(input_file, 'rb') as file:
            data = file.read()

        benchmark_results = Benchmark.benchmark_decompress(data)

        Compression.decompress_file(input_file, output_file)

        decompressed_size = Benchmark.file_size(output_file)

        benchmark_results.update({
            'decompressed_file_size': decompressed_size
        })

        return benchmark_results

if __name__ == '__main__':

    benchmark_results = Benchmark.benchmark_file_compression('data/lorem_ipsum.txt', 'data/compressed.txt')
    print(benchmark_results)
    benchmark_results = Benchmark.benchmark_file_decompression('data/compressed.txt', 'data/decompressed.txt')
    print(benchmark_results)
