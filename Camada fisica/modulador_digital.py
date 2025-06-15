# Codigo feito por Henrique Givisiez dos Santos de matricula 211027563
# Bibliotecas para auxiliar a implementacao de POO 
# Para mais informacoes, consultar: (https://docs-python-org.translate.goog/3/library/abc.html?_x_tr_sl=en&_x_tr_tl=pt&_x_tr_hl=pt&_x_tr_pto=tc)
from abc import ABC, abstractmethod

class ModuladorDigital(ABC):
    """
    Classe pai base para as modulações digitais.

    O decorator '@abstractmethod' forca as classes filhas a implementarem os metodos.
    """

    @abstractmethod
    def modular(self, bits: list[int]) -> list[int]:
        """Modula uma sequência de bits em sinais."""
        pass

    @abstractmethod
    def demodular(self, sinais: list[int]) -> list[int]:
        """Demodula uma sequência de sinais em bits."""
        pass


class CamadaFisica:
    """Gerencia a codificação e decodificação da camada física."""

    def __init__(self, modulador: ModuladorDigital):
        # Recebe uma instância de ModuladorDigital para realizar as operações
        self.modulador = modulador

    def transmitir(self, dados: list[int]) -> list[int]:
        # Modula os dados (bits) utilizando o modulador digital fornecido
        return self.modulador.modular(dados)

    def receber(self, sinais: list[int]) -> list[int]:
        # Demodula os sinais recebidos utilizando o modulador digital fornecido
        return self.modulador.demodular(sinais)
