from abc import ABC, abstractmethod

class Enquadrador(ABC):
    """
    Interface abstrata para todos os enquadradores.
    """

    @abstractmethod
    def enquadrar(self, bits: list[int]) -> list[int]:
        """
        Aplica enquadramento aos bits fornecidos.
        """
        pass

    @abstractmethod
    def desenquadrar(self, quadro: list[int]) -> list[int]:
        """
        Remove o enquadramento de um quadro.
        """
        pass


class ContagemCaracteres(Enquadrador):
    """
    Enquadramento por contagem de caracteres.
    Adiciona um cabeçalho de 8 bits com o tamanho do quadro.
    """

    def enquadrar(self, bits: list[int]) -> list[int]:
        tamanho = len(bits)
        tamanho_bits = list(map(int, f"{tamanho:08b}"))  # converte tamanho para 8 bits
        return tamanho_bits + bits

    def desenquadrar(self, quadro: list[int]) -> list[int]:
        tamanho = int("".join(map(str, quadro[:8])), 2)  # extrai tamanho
        return quadro[8:8 + tamanho]


class InsercaoBytes(Enquadrador):
    """
    Enquadramento com FLAG e inserção de bytes (byte stuffing).
    Usa FLAG = 0x7E (01111110) e ESC = 0x7D (01111101).
    Substitui ocorrências desses bytes por sequências de escape.
    """

    def __init__(self):
        self.FLAG = [0, 1, 1, 1, 1, 1, 1, 0]  # 0x7E

    def byte_to_bits(self, byte: int) -> list[int]:
        return list(map(int, f"{byte:08b}"))

    def bits_to_bytes(self, bits: list[int]) -> list[int]:
        return [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8)]

    def enquadrar(self, bits: list[int]) -> list[int]:
        bytes_ = self.bits_to_bytes(bits)
        stuffed_bytes = []

        for b in bytes_:
            if b == 0x7E:  # FLAG
                stuffed_bytes.extend([0x7D, 0x5E])  # ESC + substituto
            elif b == 0x7D:  # ESC
                stuffed_bytes.extend([0x7D, 0x5D])  # ESC + substituto
            else:
                stuffed_bytes.append(b)

        stuffed_bits = []
        for b in stuffed_bytes:
            stuffed_bits.extend(self.byte_to_bits(b))

        return self.FLAG + stuffed_bits + self.FLAG

    def desenquadrar(self, quadro: list[int]) -> list[int]:
        dados = quadro[8:-8]  # remove FLAGs
        bytes_ = self.bits_to_bytes(dados)
        i = 0
        result = []
        while i < len(bytes_):
            if bytes_[i] == 0x7D:  # ESC
                i += 1
                if i < len(bytes_):
                    if bytes_[i] == 0x5E:
                        result.append(0x7E)
                    elif bytes_[i] == 0x5D:
                        result.append(0x7D)
            else:
                result.append(bytes_[i])
            i += 1

        # Converte lista de bytes de volta para bits
        return sum([self.byte_to_bits(b) for b in result], [])


class InsercaoBits(Enquadrador):
    """
    Enquadramento com FLAG e inserção de bits (bit stuffing).
    Insere um 0 após 5 bits consecutivos com valor 1.
    """

    def __init__(self):
        self.FLAG = [0, 1, 1, 1, 1, 1, 1, 0]  # 0x7E

    def enquadrar(self, bits: list[int]) -> list[int]:
        count = 0
        stuffed = []
        for b in bits:
            stuffed.append(b)
            if b == 1:
                count += 1
                if count == 5:
                    stuffed.append(0)  # bit stuffing
                    count = 0
            else:
                count = 0
        return self.FLAG + stuffed + self.FLAG

    def desenquadrar(self, quadro: list[int]) -> list[int]:
        dados = quadro[8:-8]  # remove FLAGs
        count = 0
        result = []
        i = 0
        while i < len(dados):
            b = dados[i]
            result.append(b)
            if b == 1:
                count += 1
                if count == 5:
                    i += 1  # ignora o bit inserido (0)
                    count = 0
            else:
                count = 0
            i += 1
        return result
