from modulador import Modulador
import numpy as np

class QAM8(Modulador):
    """
    Implementação otimizada de modulação e demodulação 8-QAM.
    
    Características:
    - Modulação: Mapeia grupos de 3 bits em símbolos 8-QAM (Amplitude + Fase).
    - Demodulação: Coerente I/Q com decisão por distância euclidiana mínima.
    - Pré-computação de portadoras e constelação para eficiência.
    
    Parâmetros:
    - freq_portadora: Frequência da portadora (Hz).
    - amostras_por_simbolo: Número de amostras por símbolo (deve ser >= 8).
    """
    def __init__(self, freq_portadora: float, amostras_por_simbolo: int):
        if amostras_por_simbolo < 8:
            raise ValueError("amostras_por_simbolo deve ser >= 8 para evitar aliasing.")
        
        self.freq_portadora = freq_portadora
        self.amostras_por_simbolo = amostras_por_simbolo
        
        self._constelacao = {
            0b000: (1.0, np.pi / 4),        # Símbolo 0
            0b001: (1.0, 3 * np.pi / 4),    # Símbolo 1
            0b010: (1.0, 5 * np.pi / 4),    # Símbolo 2
            0b011: (1.0, 7 * np.pi / 4),    # Símbolo 3
            0b100: (0.5, np.pi / 4),        # Símbolo 4
            0b101: (0.5, 3 * np.pi / 4),    # Símbolo 5
            0b110: (0.5, 5 * np.pi / 4),    # Símbolo 6
            0b111: (0.5, 7 * np.pi / 4),    # Símbolo 7
        }
        
        self._iq_ideal = {
            simbolo: (amp * np.cos(fase), amp * np.sin(fase))
            for simbolo, (amp, fase) in self._constelacao.items()
        }
        
        self._tempo = np.linspace(0, 1, amostras_por_simbolo, endpoint=False)
        self._portadora_i = np.cos(2 * np.pi * freq_portadora * self._tempo)
        self._portadora_q = -np.sin(2 * np.pi * freq_portadora * self._tempo)
    

    def modular(self, bits: list[int]) -> np.ndarray:
        """
        Modula uma lista de bits (múltiplos de 3) em um sinal 8-QAM.
        
        Parâmetros:
        - bits: Lista de bits (0 ou 1). Ex: [1, 0, 1, 0, 0, 0].
        
        Retorna:
        - Sinal modulado em formato numpy.array.
        
        Lança:
        - ValueError se o número de bits não for múltiplo de 3.
        """
        if len(bits) % 3 != 0:
            raise ValueError("A quantidade de bits deve ser múltipla de 3 (8-QAM usa 3 bits/símbolo).")
        
        sinal_modulado = np.array([])
        for i in range(0, len(bits), 3):
            simbolo = (bits[i] << 2) | (bits[i+1] << 1) | bits[i+2]
            amp, fase = self._constelacao[simbolo]
            simbolo_modulado = amp * np.cos(2 * np.pi * self.freq_portadora * self._tempo + fase)
            sinal_modulado = np.append(sinal_modulado, simbolo_modulado)
        
        return sinal_modulado
    
    def demodular(self, sinal: np.ndarray) -> list[int]:
        """Demodula o sinal 8-QAM para bits."""
        if len(sinal) % self.amostras_por_simbolo != 0:
            raise ValueError("O comprimento do sinal deve ser múltiplo de amostras_por_simbolo.")

        bits_recuperados = []
        for i in range(0, len(sinal), self.amostras_por_simbolo):
            trecho = sinal[i:i + self.amostras_por_simbolo]            
            i_rx = (2 / self.amostras_por_simbolo) * np.sum(trecho * self._portadora_i)
            q_rx = (2 / self.amostras_por_simbolo) * np.sum(trecho * self._portadora_q)
            simbolo_detectado = min(
                self._iq_ideal.keys(),
                key=lambda s: (i_rx - self._iq_ideal[s][0])**2 + (q_rx - self._iq_ideal[s][1])**2
            )
            bits_recuperados.extend([
                (simbolo_detectado >> 2) & 1,
                (simbolo_detectado >> 1) & 1,
                simbolo_detectado & 1
            ])
        
        return bits_recuperados
