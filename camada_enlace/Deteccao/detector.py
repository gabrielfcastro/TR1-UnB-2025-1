# Codigo feito por Henrique Givisiez dos Santos de matricula 211027563
from abc import ABC, abstractmethod

class Detector(ABC):
    @abstractmethod
    def transmitir(self, mensagem: list[int]) -> list[int]:
        pass

    @abstractmethod
    def verificar(self, mensagem: list[int]) -> bool:
        pass

class CamadaEnlace:
    def __init__(self, detector: Detector):
        self.detector = detector

    def transmitir(self, mensagem: list[int]) -> list[int]:
        return self.detector.transmitir(mensagem)

    def verificar(self, mensagem: list[int]) -> bool:
        return self.detector.verificar(mensagem)
