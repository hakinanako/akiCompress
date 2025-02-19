import time
import random
import string

from tiny_compress import tiny_compress


class Benchmark:
    def __init__(self, compressor):
        self.compressor = compressor

    def generate_random_data(self, size: int) -> bytes:
        """
        Generate random data of a specified size.
        """
        # Generate random bytes
        data = bytes(random.choices(string.ascii_letters.encode(), k=size))
        return data

    def benchmark_compress(self, data: bytes):
        """
        Benchmark the compression time and return compression time and size.
        """
        start_time = time.time()
        compressed_data = self.compressor.compress(data)
        end_time = time.time()

        compression_time = end_time - start_time
        compressed_size = len(compressed_data)
        original_size = len(data)
        compression_ratio = compressed_size / original_size

        print(f"Compression Time: {compression_time:.4f} seconds")
        print(f"Compressed Size: {compressed_size} bytes")
        print(f"Compression Ratio: {compression_ratio:.2f}")

        return compression_time, compressed_size

    def benchmark_decompress(self, data: bytes):
        """
        Benchmark the decompression time and return decompression time.
        """
        start_time = time.time()
        decompressed_data = self.compressor.decompress(data)
        end_time = time.time()

        decompression_time = end_time - start_time
        decompressed_size = len(decompressed_data)

        print(f"Decompression Time: {decompression_time:.4f} seconds")
        print(f"Decompressed Size: {decompressed_size} bytes")

        return decompression_time

    def stress_test(self, data_size: int):
        """
        Perform a stress test by generating random data of the given size
        and benchmarking compression and decompression.
        """
        print(f"\nStress Testing with Data Size: {data_size} bytes")

        # Generate random data
        data = self.generate_random_data(data_size)

        # Benchmark compression and decompression
        compression_time, compressed_size = self.benchmark_compress(data)
        compressed_data = self.compressor.compress(data)
        decompression_time = self.benchmark_decompress(compressed_data)

        return compression_time, decompression_time

    def run_benchmarks(self, data_sizes):
        """
        Run benchmarks for all data sizes and calculate the average compression and decompression speeds.
        """
        total_compression_time = 0
        total_decompression_time = 0
        total_compressed_size = 0
        total_original_size = 0
        count = len(data_sizes)

        for size in data_sizes:
            compression_time, decompression_time = self.stress_test(size)
            total_compression_time += compression_time
            total_decompression_time += decompression_time
            total_compressed_size += size  # Just accumulating the original data sizes
            total_original_size += size  # for calculating average speed

        avg_compression_time = total_compression_time / count
        avg_decompression_time = total_decompression_time / count

        # Calculate average compression and decompression speeds (in MB per second)
        avg_compression_speed = (total_original_size / (
                    1024 * 1024)) / avg_compression_time if avg_compression_time != 0 else 0
        avg_decompression_speed = (total_compressed_size / (
                    1024 * 1024)) / avg_decompression_time if avg_decompression_time != 0 else 0

        print(f"\nAverage Compression Time: {avg_compression_time:.4f} seconds")
        print(f"Average Decompression Time: {avg_decompression_time:.4f} seconds")
        print(f"Average Compression Speed: {avg_compression_speed:.2f} MB/s")
        print(f"Average Decompression Speed: {avg_decompression_speed:.2f} MB/s")


if __name__ == "__main__":
    # Create the compressor instance
    compressor = tiny_compress()

    # Create the benchmark instance
    benchmark = Benchmark(compressor)

    # Data sizes, powers of 2 up to 128MB
    data_sizes = [2 ** i for i in range(0, 28)]

    # Run benchmarks and calculate average compression and decompression speeds
    benchmark.run_benchmarks(data_sizes)
