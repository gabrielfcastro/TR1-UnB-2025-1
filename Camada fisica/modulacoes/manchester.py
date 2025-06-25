# Codigo feito por Henrique Givisiez dos Santos de matricula 211027563
from modulador import ModuladorDigital

class Manchester(ModuladorDigital):
    """
    A codificacao Manchester utiliza uma funcao booleana exclusiva OR (XOR) para combinar os sinais de clock eh dados em um unico fluxo de bits. 
    Cada periodo de bit reflete a transicao de um nivel de tensao para outro. 
    A transicao sempre ocorre no ponto medio do periodo de bit, fornecendo uma indicacao clara do estado do bit.

    Fonte: https://www-techtarget-com.translate.goog/searchnetworking/definition/Manchester-encoding?_x_tr_sl=en&_x_tr_tl=pt&_x_tr_hl=pt&_x_tr_pto=tc

    Saidas resultantes:
    - 0: [0, 1] (transicao de baixo para cima)
    - 1: [1, 0] (transicao de cima para baixo)
    """
    def modular(self, bits: list[int]) -> list[int]:
        """
        Modula os bits usando a codificacao Manchester.
        Cada bit eh representado por dois sinais, onde:
        - 0 eh representado por [0, 1]
        - 1 eh representado por [1, 0]
    
        Args:
            bits (list[int]): Lista de bits a serem modulados (0s e 1s).

        Returns:
            list[int]: Lista de sinais modulados, onde cada bit eh representado por dois sinais.
        Examples:
            Entrada: [0, 1, 1, 0]
            Saida: [0, 1, 1, 0, 1, 0, 0, 1]
        """
        sinais = []
        clock = [0, 1] # Sinal de clock para a codificacao Manchester
        # Cada bit eh convertido em dois sinais
        for bit in bits:
            sinais.append(bit ^ clock[0])
            sinais.append(bit ^ clock[1])
        return sinais

    def demodular(self, sinais: list[int]) -> list[int]:
        """
        Demodula os sinais usando a codificacao Manchester.
        Cada par de sinais representa um bit, onde:
        - [0, 1] eh interpretado como 0
        - [1, 0] eh interpretado como 1
    
        Args:
            sinais (list[int]): Lista de sinais a serem demodulados, onde cada bit eh representado por dois sinais.

        Returns:
            list[int]: Lista de bits demodulados (0s e 1s).
        Examples:
            Entrada: [0, 1, 1, 0, 1, 0, 0, 1]
            Saida: [0, 1, 1, 0]
        """
        # Lê dois sinais por bit
        bits = []
        for i in range(0, len(sinais), 2):
            if sinais[i] < sinais[i + 1]:
                bits.append(0)  # Transição de baixo para cima
            else:
                bits.append(1)  # Transição de cima para baixo
        return bits
