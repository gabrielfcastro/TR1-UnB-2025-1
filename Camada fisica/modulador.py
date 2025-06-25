# Codigo feito por Henrique Givisiez dos Santos de matricula 211027563
# Bibliotecas para auxiliar a implementacao de POO 
# Para mais informacoes, consultar: (https://docs-python-org.translate.goog/3/library/abc.html?_x_tr_sl=en&_x_tr_tl=pt&_x_tr_hl=pt&_x_tr_pto=tc)
from abc import ABC, abstractmethod
import numpy as np

class ModuladorDigital(ABC):
    """
    Classe pai base para as modulações digitais.

    O decorator '@abstractmethod' forca as classes filhas a implementarem os metodos.
    """

    @abstractmethod
    def modular(self, bits: list[int]) -> list[int]:
        pass

    @abstractmethod
    def demodular(self, sinais: list[int]) -> list[int]:
        pass

class ModuladorPorPortadora(ABC):
    @abstractmethod
    def modular(self, bits: list[int]) -> np.ndarray:
        pass

    @abstractmethod
    def demodular(self, sinais: np.ndarray) -> list[int]:
        pass


class CamadaFisicaDigital:
    """Gerencia a codificação e decodificação da camada física."""

    def __init__(self, modulador: ModuladorDigital):
        self.modulador = modulador

    def transmitir(self, dados: list[int]) -> list[int]:
        return self.modulador.modular(dados)

    def receber(self, sinais: list[int]) -> list[int]:
        return self.modulador.demodular(sinais)
    
class CamadaFisicaPorPortadora:

    def __init__(self, modulador: ModuladorPorPortadora):
        self.modulador = modulador

    def transmitir(self, dados: list[int]) -> np.ndarray: 
        return self.modulador.modular(dados)

    def receber(self, sinais: np.ndarray) -> list[int]:
        return self.modulador.demodular(sinais)
