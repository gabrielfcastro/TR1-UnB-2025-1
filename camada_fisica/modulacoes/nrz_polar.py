# Codigo feito por Henrique Givisiez dos Santos de matricula 211027563
from ..modulador import Modulador

class NRZPolar(Modulador):
    """
    Em telecomunicacoes , um codigo de linha sem retorno a zero (NRZ) eh um codigo binário no qual os bits 1 sao 
    representados por uma condicao significativa , geralmente uma tensao positiva, enquanto os bits 0 sao representados 
    por alguma outra condicao significativa, geralmente uma tensao negativa, sem nenhuma outra condicao neutra ou de repouso.

    Na variante NRZ Polar o bit 1 eh representado por um nivel fisico (geralmente uma voltagem positiva), enquanto o bit 0 eh representado 
    por uma voltagem negativa. 

    Fonte: https://en-m-wikipedia-org.translate.goog/wiki/Non-return-to-zero?_x_tr_sl=en&_x_tr_tl=pt&_x_tr_hl=pt&_x_tr_pto=tc
    
    Implementacao da modulacao NRZ-Polar:
    - Bit 1: nivel positivo
    - Bit 0: nivel negativo
    """
    def modular(self, bits: list[int]) -> list[int]:
        """
        A modulacao parte do transmissor que irá  convertes os dados (bits) em um sinal do meio para o receptor poder receber

        Args:
            bits (list[int]): Dados(bits) que irao ser convertidos em uma funcao continua (voltagem V)
        Returns:
            list[int]: +V para bit 1 e -V para bit 0
        """
        return [1 if bit == 1 else -1 for bit in bits]

    def demodular(self, sinais: list[int]) -> list[int]:
        """
        A demodulacao parte do receptor que irá receber as variacoes de voltagem e interpretar em bits (1 para +V e 0 para -V)

        Args:
            bits (list[int]): Sinais (variacoes da amplitude) da voltagem

        Returns:
            list[int]: Sequencia de bits (1 para +V e 0 para -V)
        """
        return [1 if s > 0 else 0 for s in sinais]
