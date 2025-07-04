# Codigo feito por Henrique Givisiez dos Santos de matricula 211027563
from abc import ABC, abstractmethod

class Detector(ABC):
    @abstractmethod
    def transmitir(self, mensagem: list[int]) -> list[int]:
        pass

    @abstractmethod
    def verificar(self, mensagem: list[int]) -> bool:
        pass

    @abstractmethod
    def extrair_dados(self, bits: list[int]) -> list[int]:
        pass

class CamadaEnlace:
    def __init__(self, detector: Detector):
        self.detector = detector

    def transmitir(self, mensagem: list[int]) -> list[int]:
        return self.detector.transmitir(mensagem)

    def verificar(self, mensagem: list[int]) -> bool:
        return self.detector.verificar(mensagem)

    def extrair_dados(self, bits: list[int]) -> list[int]:
        """
        Extrai os dados da mensagem, removendo o bit de paridade ou EDC.
        Args:
        bits (list[int]): Lista de bits com o bit de paridade ou EDC no final.

        Returns:
        list[int]: Lista de bits sem o bit de paridade ou EDC.
        """
        return self.detector.extrair_dados(bits)