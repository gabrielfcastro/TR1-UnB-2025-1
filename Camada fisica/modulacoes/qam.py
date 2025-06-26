# Codigo feito por Gabriel Francisco de Oliveira Castro de matricula 202066571
from modulador import Modulador
import numpy as np

class QAM(Modulador):
    """
    QAM significa Modulação em Amplitude em Quadratura (combina modulação em amplitude com
    modulação em fase)
    - 8QAM: Modulação Digital que transmite 3 bits por símbolo (2**3 = 8 simbolos diferentes)
    """
    def modular(self, bits: list[int]) -> np.ndarray:
        """
        Converte uma sequência de bits (multiplos de 3) em um sinal 8QAM. 
        - Cada conjunto de 3 bits representam um símbolo com fase e amplitude diferentes.
        """
        if len(bits) % 3 != 0:
            raise ValueError("A quantidade de bits deve ser múltipla de 3.")
        ################################################################
        # Vamos mudar isso aqui, p/ quando formos integrar tudo junto.
        # Vai receber via terminal ?
        # --- Geração da Onda Portadora (template) ---
        # Cria um vetor de tempo para a duração de um bit
        # Cria a onda portadora
        amostras_por_bit = 200
        freq_portadora = 5.0
        tempo = np.linspace(0, 1, amostras_por_bit, endpoint = False)
        ################################################################
        sinal_modulado = []
        mapa_8qam = {
            0: (1.0, 0),
            1: (1.0, np.pi/2),
            2: (1.0, np.pi),
            3: (1.0, 3*np.pi/2),
            4: (0.5, np.pi/4),
            5: (0.5, 3*np.pi/4),
            6: (0.5, 5*np.pi/4),
            7: (0.5, 7*np.pi/4),
        }
        for i in range(0, len(bits),3):
            grupo = bits[i:i+3]
            b0, b1, b2 = grupo
            simbolo = (b0 << 2) | (b1 <<1) | b2 # Converto meu grupo de 3 bits em um número de 0 a 7, sendo b0 o mais significativo
            amplitude, fase = mapa_8qam[simbolo]
            onda = amplitude * np.cos(2 * np.pi * freq_portadora * tempo + fase)
            sinal_modulado.extend(onda)

        return np.array(sinal_modulado)
    
    def demodular(self, sinais: np.ndarray) -> list[int]:
        """
        Recupero meu trem de bits a partir de um sinal 8QAM, usando a correlação com todos os
        símbolos da constelação.
        """
        ################################################################
        # --- Geração da Onda Portadora para correlação ---
        # Vamos mudar isso aqui, p/ quando formos integrar tudo junto.
        # Vai receber via terminal ?
        amostras_por_simbolo = 200
        freq_portadora = 5.0
        tempo = np.linspace(0, 1, amostras_por_simbolo, endpoint=False)
        ################################################################
        bits_recuperados = []
        mapa_8qam = {
            0: (1.0, 0),
            1: (1.0, np.pi/2),
            2: (1.0, np.pi),
            3: (1.0, 3*np.pi/2),
            4: (0.5, np.pi/4),
            5: (0.5, 3*np.pi/4),
            6: (0.5, 5*np.pi/4),
            7: (0.5, 7*np.pi/4),
        }
        referencias = {}
        # Para cada símbolo da constelação gera a onde de referência com determinada amplitude e fase
        for simb, (amp, fase) in mapa_8qam.items(): 
            referencia = amp * np.cos(2 * np.pi * freq_portadora * tempo + fase)
            referencias[simb] = referencia
        for i in range(0, len(sinais), amostras_por_simbolo):
            trecho = sinais[i:i + amostras_por_simbolo]
            if len(trecho) < amostras_por_simbolo:
                break  # ignora pedaços incompletos
            melhor_correlacao = -np.inf # Usamos um valor inicial tão baixo que qualquer correlação é maior
            simbolo_detectado = 0
            for simb, ref in referencias.items(): # Comparo o trecho recebido com a onda de referência
                correlacao = np.dot(trecho, ref)
                if correlacao > melhor_correlacao:
                    melhor_correlacao = correlacao
                    simbolo_detectado = simb
            b0 = (simbolo_detectado >> 2) & 1
            b1 = (simbolo_detectado >> 1) & 1
            b2 = simbolo_detectado & 1
            bits_recuperados.extend([b0, b1, b2])

        return bits_recuperados


