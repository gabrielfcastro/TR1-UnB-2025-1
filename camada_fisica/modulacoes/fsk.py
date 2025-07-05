# Codigo feito por Gabriel Francisco de Oliveira Castro de matricula 202066571
from camada_fisica.modulador import Modulador
import numpy as np

class FSK(Modulador):
    """
    Modulação por Chaveamento de Freqûencia. Consiste em fazer uma seleção de frequências
    entre dois sinais baseado no meu sinal modulante. Por exemplo, enquanto o sinal modudante
    estiver em 1 uso a frequência da minha portadora 1, caso esteja em 0 uso o a frequeência da
    minha portadora 2, ou seja:
    |m(t) = 1 --> fp1
    |m(t) = 0 --> fp2
    
    - A frequência da minha portadora varia de acordo com a amplitude do sinal mensagem
    """

    def __init__(self, freq_p_bit0: float, freq_p_bit1: float, amostras_por_bit: int, amplitude: float = 1.0):
        """
            Inicializo o modulador FSK:
            - freq_p_bit0 (frequência da portadora 1) : Frequência do meu bit 0.
            - freq_p_bit1 (frequência da portadora 2) : Frequência do meu bit 1.
            - amostras_por_bit                        : Número de amostras p/ representar cada bit.
        """
        self.freq_p_bit0 = freq_p_bit0
        self.freq_p_bit1 = freq_p_bit1
        self.amostras_por_bit = amostras_por_bit

        self.tempo = np.linspace(0, 1, amostras_por_bit, endpoint=False)
        self.portadora_0 = amplitude * np.cos(2 * np.pi * freq_p_bit0 * self.tempo)
        self.portadora_1 = amplitude * np.cos(2 * np.pi * freq_p_bit1 * self.tempo)

    def modular(self, bits: list[int]) -> np.ndarray:
        sinal_modulado = []
        for bit in bits:
            if bit == 1:
                sinal_modulado.extend(self.portadora_1)
            else:
                sinal_modulado.extend(self.portadora_0)

        return np.array(sinal_modulado)
    
    def demodular(self, sinal: np.ndarray) -> list[int]:
        """
        Converte um sinal FSK de volta para uma sequência de bits. Para isso< Compara cada trecho do sinal com 
        duas ondas de referência (para bit 0 e 1) e escolhe o bit correspondente à referência mais parecida.
        """
        bits_recuperados = []
        for i in range(0, len(sinal), self.amostras_por_bit):
            trecho = sinal[i:i + self.amostras_por_bit]
            correlacao_0 = np.sum(trecho * self.portadora_0)
            correlacao_1 = np.sum(trecho * self.portadora_1)
            if correlacao_1 > correlacao_0:
                bits_recuperados.append(1)
            else:
                bits_recuperados.append(0)

        return bits_recuperados