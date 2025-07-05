from .detector import Detector

class BitParidade(Detector):
    """
    Implementacao do protocolo de deteccao de erro utilizando Bit de Paridade Par.
    Esta classe implementa os metodos para transmissao e verificacao com base no numero
    de bits '1' em uma mensagem.
    """

    def transmitir(self, mensagem: list[int]) -> list[int]:
        """
        Metodo responsavel por transmitir uma mensagem, adicionando o bit de paridade par.

        Args:
        mensagem (list[int]): Lista de bits (0 ou 1) representando a mensagem original.

        Returns:
        list[int]: Lista de bits com o bit de paridade adicionado ao final.
        """
        # Conta quantos bits '1' existem na mensagem
        conta_uns = mensagem.count(1)

        # Calcula o bit de paridade: se eh quantidade par de '1's, paridade eh 0;
        # caso contrario, adiciona 1 para tornar par.
        paridade = 0 if conta_uns % 2 == 0 else 1

        # Adiciona o bit de paridade ao final da mensagem
        mensagem.append(paridade)

        # Retorna a mensagem com o bit de paridade
        return mensagem

    def verificar(self, mensagem: list[int]) -> bool:
        """
        Metodo responsavel por verificar se a paridade da mensagem esta correta.

        Args:
        mensagem (list[int]): Lista de bits com o bit de paridade ja incluido.

        Returns:
        bool: True se a paridade estiver correta (numero total de '1's eh par),
              False caso contrario.
        """
        # Conta o número total de bits '1' (incluindo o bit de paridade)
        total_uns = mensagem.count(1)

        # Retorna True se a quantidade for par (paridade válida), False se for ímpar
        return total_uns % 2 == 0


    def extrair_dados(self, bits: list[int]) -> list[int]:
        """
        Extrai os dados da mensagem, removendo o bit de paridade.
        Args:
        bits (list[int]): Lista de bits com o bit de paridade no final.

        Returns:
        list[int]: Lista de bits sem o bit de paridade.
        """
        return bits[:-1]  # remove último bit (paridade)