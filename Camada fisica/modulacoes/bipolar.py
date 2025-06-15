# Codigo feito por Henrique Givisiez dos Santos de matricula 211027563
from modulador_digital import ModuladorDigital

class Bipolar(ModuladorDigital):
    """
    O esquema de codificacao bipolar define tres niveis de tensao: positivo, negativo e zero.
    Na codificacao bipolar, o nivel zero representa o bit 0, e o bit 1 eh representado por uma alternancia entre tensoes positivas e negativas.
    Suponha que o primeiro bit 1 seja representado por uma amplitude positiva. O segundo bit 1 será representado por uma tensao negativa; 
    o terceiro bit 1 volta a ser positivo, e assim por diante, alternando mesmo quando os bits 1 nao sao sucessivos.

    Fonte: https://www.tutorialspoint.com/what-is-bipolar-encoding?utm_source=chatgpt.com
    Saidas resultantes:
    - 0: 0V (nivel nulo)
    - 1: +1V ou -1V (alternando a cada bit 1 sucessivo)
    """
    def modular(self, bits: list[int]) -> list[int]:
        """
        Modula uma sequencia de bits usando codificacao bipolar.

        Args:
            bits (list[int]): lista de bits (0s e 1s) a serem modulados.

        Returns:
            list[int]: lista de niveis de tensao para transmissao:
                0 -> 0V
                1 -> alterna +1 e -1 a cada 1 sucessivo

        Examples:
            Entrada: [1, 0, 1, 1, 0, 1]
            Saida:   [+1, 0, -1, +1, 0, -1]
        """
        sinais = []
        ultimo = -1  # Comeca em -1 para que o primeiro 1 gere +1
        for bit in bits:
            if bit == 0:
                sinais.append(0)
            else:
                ultimo *= -1  # alterna entre +1 e -1
                sinais.append(ultimo)
        return sinais

    def demodular(self, sinais: list[int]) -> list[int]:
        """
        Demodula uma sequencia de sinais de volta para bits usando codificao bipolar.

        Args:
            sinais (list[int]): lista de niveis de tensao recebidos.

        Returns:
            list[int]: lista de bits reconstruidos:
                       - 0V → 0
                       - +V ou -V → 1 (nao se verifica violacao aqui)
                       
        Examples:
            Entrada: [+1, 0, -1, +1, 0, -1]
            Saida:   [1, 0, 1, 1, 0, 1]
        """
        return [0 if s == 0 else 1 for s in sinais]
