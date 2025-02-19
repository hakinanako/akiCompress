import time
import random
import string
import matplotlib.pyplot as plt

from tiny_compress import tiny_compress


class Benchmark:
    def __init__(self, compressor):
        self.compressor = compressor
        # Initialize lists to store benchmark results for plotting
        self.data_sizes = []
        self.compression_times = []
        self.decompression_times = []
        self.compression_speeds = []
        self.decompression_speeds = []

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

        return compression_time, compressed_size

    def benchmark_decompress(self, data: bytes):
        """
        Benchmark the decompression time and return decompression time.
        """
        start_time = time.time()
        decompressed_data = self.compressor.decompress(data)
        end_time = time.time()

        decompression_time = end_time - start_time
        return decompression_time

    def stress_test(self, data_size: int):
        """
        Perform a stress test by generating random data of the given size
        and benchmarking compression and decompression.
        """
        # Generate random data
        data = self.generate_random_data(data_size)

        # Benchmark compression and decompression
        compression_time, compressed_size = self.benchmark_compress(data)
        compressed_data = self.compressor.compress(data)
        decompression_time = self.benchmark_decompress(compressed_data)

        return compression_time, decompression_time, data_size

    def run_benchmarks(self, data_sizes):
        """
        Run benchmarks for all data sizes and store the results for plotting.
        """
        for size in data_sizes:
            compression_time, decompression_time, original_size = self.stress_test(size)
            # Append the results
            self.data_sizes.append(original_size)
            self.compression_times.append(compression_time)
            self.decompression_times.append(decompression_time)

            # Calculate compression and decompression speeds (MB/s)
            compression_speed = (original_size / (1024 * 1024)) / compression_time if compression_time != 0 else 0
            decompression_speed = (original_size / (1024 * 1024)) / decompression_time if decompression_time != 0 else 0

            self.compression_speeds.append(compression_speed)
            self.decompression_speeds.append(decompression_speed)

        # Plot the benchmark results
        self.plot_benchmarks()

    def plot_benchmarks(self):
        """
        Plot the benchmark results using matplotlib.
        """
        # Plot compression time vs. data size
        plt.figure(figsize=(10, 6))
        plt.plot(self.data_sizes, self.compression_times, label="Compression Time", color='blue', marker='o')
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Data Size (bytes)')
        plt.ylabel('Compression Time (seconds)')
        plt.title('Compression Time vs Data Size')
        plt.grid(True)
        plt.legend()
        plt.show()

        # Plot decompression time vs. data size
        plt.figure(figsize=(10, 6))
        plt.plot(self.data_sizes, self.decompression_times, label="Decompression Time", color='red', marker='o')
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Data Size (bytes)')
        plt.ylabel('Decompression Time (seconds)')
        plt.title('Decompression Time vs Data Size')
        plt.grid(True)
        plt.legend()
        plt.show()

        # Plot compression speed vs. data size
        plt.figure(figsize=(10, 6))
        plt.plot(self.data_sizes, self.compression_speeds, label="Compression Speed", color='green', marker='o')
        plt.xscale('log')
        plt.xlabel('Data Size (bytes)')
        plt.ylabel('Compression Speed (MB/s)')
        plt.title('Compression Speed vs Data Size')
        plt.grid(True)
        plt.legend()
        plt.show()

        # Plot decompression speed vs. data size
        plt.figure(figsize=(10, 6))
        plt.plot(self.data_sizes, self.decompression_speeds, label="Decompression Speed", color='orange', marker='o')
        plt.xscale('log')
        plt.xlabel('Data Size (bytes)')
        plt.ylabel('Decompression Speed (MB/s)')
        plt.title('Decompression Speed vs Data Size')
        plt.grid(True)
        plt.legend()
        plt.show()


if __name__ == "__main__":
    # Create the compressor instance
    compressor = tiny_compress()

    # Create the benchmark instance
    benchmark = Benchmark(compressor)

    # Data sizes, powers of 2 up to 128MB
    data_sizes = [2 ** i for i in range(1, 22)]

    # Run benchmarks and generate plots
    benchmark.run_benchmarks(data_sizes)
