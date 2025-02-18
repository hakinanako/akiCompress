class mtf:

    @staticmethod
    def encode(data: bytes) -> bytes:
        """Move-to-Front encoding for byte sequences"""
        symbols = list(range(256))
        result = bytearray()

        for byte in data:
            index = symbols.index(byte)
            result.append(index)
            symbols.pop(index)
            symbols.insert(0, byte)

        return bytes(result)

    @staticmethod
    def decode(data: bytes) -> bytes:
        """Move-to-Front decoding for byte sequences"""
        symbols = list(range(256))
        result = bytearray()

        for index in data:
            byte = symbols[index]
            result.append(byte)
            symbols.pop(index)
            symbols.insert(0, byte)

        return bytes(result)