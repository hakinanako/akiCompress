class RLE:
    MAX_COUNT = 255

    @staticmethod
    def rle_encode(data: bytes) -> bytes:
        encoded = []
        count = 1

        for i in range(1, len(data)):
            if data[i] == data[i - 1]:
                count += 1
            else:
                while count > RLE.MAX_COUNT:
                    encoded.append(RLE.MAX_COUNT)
                    encoded.append(data[i - 1])
                    count -= RLE.MAX_COUNT
                encoded.append(count)
                encoded.append(data[i - 1])
                count = 1

        while count > RLE.MAX_COUNT:
            encoded.append(RLE.MAX_COUNT)
            encoded.append(data[-1])
            count -= RLE.MAX_COUNT
        encoded.append(count)
        encoded.append(data[-1])

        return bytes(encoded)

    @staticmethod
    def rle_decode(data: bytes) -> bytes:
        decoded = bytearray()

        for i in range(0, len(data), 2):
            count = data[i]
            byte = data[i + 1]

            decoded.extend([byte] * count)

        return bytes(decoded)