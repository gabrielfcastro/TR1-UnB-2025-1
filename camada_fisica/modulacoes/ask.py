# Codigo feito por Gabriel Francisco de Oliveira Castro de matricula 202066571
from camada_fisica.modulador import Modulador
import numpy as np

class ASK(Modulador):
    """
    Modulação por Chaveamento de Amplitude, a amplitude do sinal da portadora para
    criar elementos de sinal
    - Tanto a frequência quanto a fase permanem inalteras enquanto a APENAS amplitude muda.
    Nesse sentido:
    - Bit 1: Representado pela presença da onda portadora (alta amplitude).
    - Bit 0: Representado pela ausencia de onda portadaora (baixa amplitude).
    """
    def __init__(self, freq_portadora: float, amostras_por_bit: int, limiar_de_energia: float = 0.1):
        """
            Inicializo o modulador ASK:
            - freq_portadora    : Frequência da onda portadora em Hz.
            - amostras_por_bit  : Número de amostras p/ representar cada bit.
            - limiar_de_energia : Limiar para a tomada de decisão durante a modulação.
        """
        self.freq_portadora = freq_portadora
        self.amostras_por_bit = amostras_por_bit
        self.limiar_de_energia = limiar_de_energia

        tempo = np.linspace(0, 1, amostras_por_bit, endpoint = False)
        self.portadora = np.cos(2 * np.pi* freq_portadora * tempo)

    def modular(self, bits: list[int]) -> np.ndarray:
        """
        Converte uma sequência de bits em um sinal ASK. Para isso, "multiplica" a portadora
        pelo modulante digital
        """
        sinal_modulado = []
        for bit in bits:
            if bit == 1:
                amplitude = 1.0
            else:
                amplitude = 0
            sinal_modulado.extend(amplitude * self.portadora)        
        
        return np.array(sinal_modulado)
    
    def demodular(self, sinais: np.ndarray) -> list[int]:
        """
        O princípio da demodulação ASK é medir a energia do sinal em cada intervalo (Este método recebe a onda
        ASK e o converte para o sinal original").
        - Criamos um valor de corte para entre 0 e 1, isso leva em consideração o mundo real e o ruído. 
        - Dessa forma, calculamos a energia do trecho (soma dos quadrados das amostras) e compara com o limiar 
        p/ decidir qual o valor do bit. 
        """
        bits_recuperados = []
        for i in range(0, len(sinais),self.amostras_por_bit):
            trecho = sinais[i:i + self.amostras_por_bit]
            energia = np.sum(trecho**2)/self.amostras_por_bit
            if energia > self.limiar_de_energia:
                bits_recuperados.append(1)
            else:
                bits_recuperados.append(0)
                
        return bits_recuperados