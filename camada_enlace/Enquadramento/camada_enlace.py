from .enquadrador import Enquadrador

class CamadaEnlace:
    """
    Representa a camada de enlace com foco em enquadramento de dados.

    Esta classe fornece métodos para:
    - aplicar enquadramento a um bloco de bits;
    - remover o enquadramento (desenquadrar) de um quadro de bits.

    O comportamento é definido por uma instância de `Enquadrador`.
    """

    def __init__(self, enquadrador: Enquadrador):
        """
        Inicializa a camada de enlace com uma estratégia de enquadramento.

        Parâmetros:
        - enquadrador: instância concreta de uma subclasse de `Enquadrador`
        """
        self.enquadrador = enquadrador

    def enquadrar(self, bits: list[int]) -> list[int]:
        """
        Aplica a técnica de enquadramento definida no enquadrador.

        Parâmetros:
        - bits: lista de bits representando os dados

        Retorna:
        - lista de bits enquadrados (quadro completo)
        """
        return self.enquadrador.enquadrar(bits)

    def desenquadrar(self, quadro: list[int]) -> list[int]:
        """
        Remove o enquadramento de um quadro de bits.

        Parâmetros:
        - quadro: lista de bits representando o quadro enquadrado

        Retorna:
        - lista de bits originais sem o cabeçalho/marcadores de enquadramento
        """
        return self.enquadrador.desenquadrar(quadro)