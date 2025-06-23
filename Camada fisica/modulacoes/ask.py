# Codigo feito por Gabriel Francisco de Oliveira Castro de matricula 202066571
from modulador_por_portadora import ModuladorPorPortadora
import numpy as np

class ASK(ModuladorPorPortadora):
    """
    Modulação por Chaveamento de Amplitude, a amplitude do sinal da portadora para
    criar elementos de sinal
    - Tanto a frequência quanto a fase permanem inalteras enquanto a APENAS amplitude muda

    - Bit 1: Representado pela presença da onda portadora (alta amplitude).
    - Bit 0: Representado pela ausencia de onda portadaora (baixa amplitude).
    """
    def modular(self, bits: list[int]) -> np.ndarray:
        """
        Converte uma sequência de bits em um sinal ASK. Para isso, "multiplica" a portadora
        pelo modulante digital
        """
        amostras_por_bit = 200
        freq_portadora = 5.0

        # --- Geração da Onda Portadora (template) ---
        # Cria um vetor de tempo para a duração de um bit
        tempo = np.linspace(0, 1, amostras_por_bit, endpoint = False)
        # Cria a onda portadora
        portadora = np.cos(2 * np.pi* freq_portadora * tempo)

        sinal_modulado = []
        # Para cada bit na sequência de entrada...
        for bit in bits:
            # Se o bit for 1, a amplitude é 1, se for 0 a amplitude é 0
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
        """
        amostras_por_bit = 200
        """
        Valor de corte para decidir entre 0 e 1, isso leva em consideração o mundo real e o ruído. De acordo com 
        o tanto de ruído que teremos em nosso sinal. Como estamos tratando aqui de um caso ideal (0 + 0) vai dar
        sempre zero.
        """
        limiar_de_energia = 0.1 

        bits_recuperados = []
        # Processa o sinal em "fatias", esta corresponde a um bit
        for i in range(0, len(sinais),amostras_por_bit):
            trecho = sinais[i:i + amostras_por_bit]
            # Calcula a energia do trecho (soma dos quadrados das amostras)
            energia = np.sum(trecho**2)/amostras_por_bit
            # Compara a energia com o limiar para decidir o bit
            if energia > limiar_de_energia:
                bits_recuperados.append(1)
            else:
                bits_recuperados.append(0)
                
        return bits_recuperados