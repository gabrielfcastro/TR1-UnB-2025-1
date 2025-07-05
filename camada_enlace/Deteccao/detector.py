from abc import ABC, abstractmethod

class Detector(ABC):
    """
    Interface abstrata para detectores e corretores de erro (EDC).
    Todas as classes concretas devem implementar os seguintes métodos:
    - transmitir: aplica o EDC à mensagem
    - verificar: valida a integridade da mensagem recebida
    - extrair_dados: remove os bits de controle e retorna somente os dados
    """
    
    @abstractmethod
    def transmitir(self, mensagem: list[int]) -> list[int]:
        """
        Aplica o algoritmo de EDC e retorna a mensagem codificada.
        """
        pass

    @abstractmethod
    def verificar(self, mensagem: list[int]) -> bool:
        """
        Verifica se a mensagem recebida está íntegra (sem erro detectável).
        """
        pass

    @abstractmethod
    def extrair_dados(self, bits: list[int]) -> list[int]:
        """
        Remove os bits de EDC e retorna apenas os dados originais.
        """
        pass


class CamadaEnlace:
    """
    Esta classe encapsula um detector de EDC e fornece uma interface única
    para usá-lo na transmissão e recepção de quadros.

    Utiliza o padrão de projeto *Strategy*, permitindo usar diferentes algoritmos
    de EDC (paridade, CRC, Hamming) de forma intercambiável.
    """
    
    def __init__(self, detector: Detector):
        """
        Inicializa a camada de enlace com um detector de erros.
        """
        self.detector = detector

    def transmitir(self, mensagem: list[int]) -> list[int]:
        """
        Aplica o EDC à mensagem (fase de transmissão).
        """
        return self.detector.transmitir(mensagem)

    def verificar(self, mensagem: list[int]) -> bool:
        """
        Verifica se a mensagem recebida passou no teste de integridade.
        """
        return self.detector.verificar(mensagem)

    def extrair_dados(self, bits: list[int]) -> list[int]:
        """
        Remove os bits de EDC e retorna somente os dados da mensagem.
        """
        return self.detector.extrair_dados(bits)
