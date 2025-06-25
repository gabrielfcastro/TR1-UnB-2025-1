# Codigo feito por Gabriel Francisco de Oliveira Castro de matricula 202066571
from modulador import ModuladorPorPortadora
import numpy as np

class ASK(ModuladorPorPortadora):
    """
    Modulação por Chaveamento de Amplitude, a amplitude do sinal da portadora para
    criar elementos de sinal
    - Tanto a frequência quanto a fase permanem inalteras enquanto a APENAS amplitude muda.
    Nesse sentido:
    - Bit 1: Representado pela presença da onda portadora (alta amplitude).
    - Bit 0: Representado pela ausencia de onda portadaora (baixa amplitude).
    """
    def modular(self, bits: list[int]) -> np.ndarray:
        """
        Converte uma sequência de bits em um sinal ASK. Para isso, "multiplica" a portadora
        pelo modulante digital
        """
        ################################################################
        # Vamos mudar isso aqui, p/ quando formos integrar tudo junto.
        # Vai receber via terminal ?
        # --- Geração da Onda Portadora (template) ---
        # Cria um vetor de tempo para a duração de um bit
        # Cria a onda portadora
        amostras_por_bit = 200
        freq_portadora = 5.0
        tempo = np.linspace(0, 1, amostras_por_bit, endpoint = False)
        portadora = np.cos(2 * np.pi* freq_portadora * tempo)
        ################################################################
        sinal_modulado = []
        for bit in bits:
            if bit == 1:
                amplitude = 1.0
                sinal_modulado.extend(amplitude * portadora)
            else:
                amplitude = 0
                sinal_modulado.extend(amplitude * portadora)        
        
        return np.array(sinal_modulado)
    
    def demodular(self, sinais: np.ndarray) -> list[int]:
        """
        O princípio da demodulação ASK é medir a energia do sinal em cada intervalo (Este método recebe a onda
        ASK e o converte para o sinal original").
        - Criamos um valor de corte para entre 0 e 1, isso leva em consideração o mundo real e o ruído. 
        - Dessa forma, calculamos a energia do trecho (soma dos quadrados das amostras) e compara com o limiar 
        p/ decidir qual o valor do bit. 
        """
        ################################################################
        # Vamos mudar isso aqui, p/ quando formos integrar tudo junto.
        # Vai receber via terminal ?
        amostras_por_bit = 200
        limiar_de_energia = 0.1 
        ################################################################
        bits_recuperados = []
        for i in range(0, len(sinais),amostras_por_bit):
            trecho = sinais[i:i + amostras_por_bit]
            energia = np.sum(trecho**2)/amostras_por_bit
            if energia > limiar_de_energia:
                bits_recuperados.append(1)
            else:
                bits_recuperados.append(0)
                
        return bits_recuperados