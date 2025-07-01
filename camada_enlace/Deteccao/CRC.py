# Codigo feito por Henrique Givisiez dos Santos de matricula 211027563
from detector import Detector

class CRC(Detector):
    """
    Implementacao do protocolo de deteccao de erros usando CRC-32 (IEEE 802).
    Essa classe herda de 'Detector' e implementa metodos para transmissao e verificacao
    com base no polinomio gerador padrao do CRC-32.
    """

    # Polinômio CRC-32 padrao (em binario): 0x104C11DB7
    POLINOMIO = 0x104C11DB7
    GRAU = 32

    def _lista_para_inteiro(self, bits: list[int]) -> int:
        """Converte uma lista de bits para um numero inteiro."""
        resultado = 0
        for bit in bits:
            resultado = (resultado << 1) | bit
        return resultado

    def _inteiro_para_lista(self, numero: int, tamanho: int) -> list[int]:
        """Converte um numero inteiro para uma lista de bits de tamanho fixo."""
        return [(numero >> i) & 1 for i in reversed(range(tamanho))]

    def transmitir(self, mensagem: list[int]) -> list[int]:
        """
        Gera o codigo CRC para a mensagem e retorna a mensagem original com os bits de CRC anexados.

        Args:
        mensagem (list[int]): Lista de bits da mensagem original.

        Returns:
        list[int]: Mensagem original seguida do codigo CRC (32 bits).
        """
        # Converte a lista de bits para inteiro
        dados = self._lista_para_inteiro(mensagem)

        # Desloca os bits a esquerda para reservar espaço para o CRC (grau do polinômio)
        dados <<= self.GRAU

        # Calcula o CRC usando divisao polinomial
        for i in reversed(range(len(mensagem))):
            if (dados >> (i + self.GRAU)) & 1:
                dados ^= self.POLINOMIO << i

        # O CRC esta nos bits inferiores apos o XOR
        crc = dados & ((1 << self.GRAU) - 1)

        # Concatena os bits originais com o CRC
        return mensagem + self._inteiro_para_lista(crc, self.GRAU)

    def verificar(self, mensagem: list[int]) -> bool:
        """
        Verifica se o codigo CRC da mensagem esta correto.

        Args:
        mensagem (list[int]): Lista de bits contendo a mensagem original + CRC (ultimos 32 bits).

        Returns:
        bool: True se o CRC for valido (sem erro), False se houver erro.
        """
        # Converte a lista de bits para inteiro
        dados = self._lista_para_inteiro(mensagem)

        # Executa a divisao polinomial para verificar o CRC
        for i in reversed(range(len(mensagem) - self.GRAU)):
            if (dados >> (i + self.GRAU)) & 1:
                dados ^= self.POLINOMIO << i

        # Se o resultado for 0, o CRC eh valido
        return (dados & ((1 << self.GRAU) - 1)) == 0
