# Bibliotecas para auxiliar a implementacao de POO 
# Para mais informacoes, consultar: (https://docs-python-org.translate.goog/3/library/abc.html?_x_tr_sl=en&_x_tr_tl=pt&_x_tr_hl=pt&_x_tr_pto=tc)
from abc import ABC, abstractmethod
import numpy as np

class Modulador(ABC):
    """
    Classe pai base para as modulações digitais e por portadora.

    O decorator '@abstractmethod' forca as classes filhas a implementarem os metodos.
    """

    @abstractmethod
    def modular(self, bits: list[int]) -> list[int] | np.ndarray:
        pass

    @abstractmethod
    def demodular(self, sinais: list[int] | np.ndarray) -> list[int]:
        pass


class CamadaFisica:
    """Gerencia a codificação e decodificação da camada física."""

    def __init__(self, modulador: Modulador):
        self.modulador = modulador

    def transmitir(self, dados: list[int]) -> list[int] | np.ndarray:
        return self.modulador.modular(dados)

    def receber(self, sinais: list[int] | np.ndarray) -> list[int]:
        return self.modulador.demodular(sinais)
