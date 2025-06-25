# Codigo feito por Gabriel Francisco de Oliveira Castro de matricula 202066571
from modulador import ModuladorPorPortadora
import numpy as np

class FSK(ModuladorPorPortadora):
    """
    Modulação por Chaveamento de Freqûencia. Consiste em fazer uma seleção de frequências
    entre dois sinais baseado no meu sinal modulante. Por exemplo, enquanto o sinal modudante
    estiver em 1 uso a frequência da minha portadora 1, caso esteja em 0 uso o a frequeência da
    minha portadora 2, ou seja:
    |m(t) = 1 --> fp1
    |m(t) = 0 --> fp2
    
    - A frequência da minha portadora varia de acordo com a amplitude do sinal mensagem
    """
    def modular(self, bits: list[int]) -> np.ndarray:
        ################################################################
        # Vamos mudar isso aqui, p/ quando formos integrar tudo junto.
        # Vai receber via terminal ?
        # --- Parâmetros da Simulação ---
        amostras_por_bit = 200
        freq_p_bit0 = 5.0
        freq_p_bit1 = 10.0
        amplitude = 1.0
        tempo = np.linspace(0, 1, amostras_por_bit, endpoint=False)
        portadora_0 = amplitude * np.cos(2 * np.pi * freq_p_bit0 * tempo)
        portadora_1 = amplitude * np.cos(2 * np.pi * freq_p_bit1 * tempo)
        ################################################################
        sinal_modulado = []
        for bit in bits:
            if bit == 1:
                sinal_modulado.extend(portadora_1)
            else:
                sinal_modulado.extend(portadora_0)

        return np.array(sinal_modulado)
    
    def demodular(self, sinal: np.ndarray) -> list[int]:
        """
        Converte um sinal FSK de volta para uma sequência de bits. Para isso< Compara cada trecho do sinal com 
        duas ondas de referência (para bit 0 e 1) e escolhe o bit correspondente à referência mais parecida.
        """
        ################################################################
        # Vamos mudar isso aqui, p/ quando formos integrar tudo junto.
        # Vai receber via terminal ?
        # --- Parâmetros da Simulação ---
        amostras_por_bit = 200
        freq_p_bit0 = 5.0
        freq_p_bit1 = 10.0
        tempo = np.linspace(0, 1, amostras_por_bit, endpoint=False)
        ref_0 = np.cos(2 * np.pi * freq_p_bit0 * tempo)
        ref_1 = np.cos(2 * np.pi * freq_p_bit1 * tempo)
        ################################################################
        bits_recuperados = []
        for i in range(0, len(sinal), amostras_por_bit):
            trecho = sinal[i:i + amostras_por_bit]
            correlacao_0 = np.sum(trecho * ref_0)
            correlacao_1 = np.sum(trecho * ref_1)
            if correlacao_1 > correlacao_0:
                bits_recuperados.append(1)
            else:
                bits_recuperados.append(0)

        return bits_recuperados