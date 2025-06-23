# Codigo feito por Gabriel Francisco de Oliveira Castro de matrícula 202066571
# Arquivo feito utilizando como base o arquivo modulador_digital.py feito por Henrique Givisiez dos Santos
from abc import ABC, abstractmethod
import numpy as np

class ModuladorPorPortadora(ABC):
    """
    Classe pai base para as modulações digitais.

    O decorator '@abstractmethod' forca as classes filhas a implementarem os metodos.
    """

    @abstractmethod
    def modular(self, bits: list[int]) -> np.ndarray:
        """Converte uma sequência de bits em um sinal analógico modulado."""
        pass

    @abstractmethod
    def demodular(self, sinais: np.ndarray) -> list[int]:
        """Recupera a sequência de bits original a partir de um sinal analógico."""
        pass

class CamadaFisica:
    """Gerencia a codificação e decodificação da camada física."""

    ## O q seria o modulador ?
    def __init__(self, modulador: ModuladorPorPortadora):
        self.modulador = modulador

    def transmitir(self, dados: list[int]) -> np.ndarray:
        sinal_gerado = self.modulador.modular(dados) 
        return sinal_gerado

    def receber(self, sinais: np.ndarray) -> list[int]:
        bits_recuperados = self.modulador.demodular(sinais)
        return bits_recuperados