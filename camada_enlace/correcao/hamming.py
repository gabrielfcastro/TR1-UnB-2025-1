from ..Deteccao.detector import Detector

class Hamming(Detector):
    """
    Implementacao do protocolo de correcao de erros utilizando o codigo de Hamming
    para um tamanho fixo de 7 bits de dados e 4 bits de paridade (11 bits no total)
    """

    def transmitir(self, mensagem: list[int]) -> list[int]:
        """
        Codifica 7 bits de dados utilizando Hamming e caclula a paridade desse trem de bits.
        """
        if len(mensagem) != 7:
            raise ValueError("A mensagem precisa ter exatamente 7 bits de dados")
        
        # Faço uma copia da minha mensagem 
        dados = mensagem
        # Crio um vetor de 11 posições preenchidos com 0
        codigo = [0] * 11
        
        # Mapeia os 7 bits de dados
        codigo[2] = dados[0]  # Posição 3
        codigo[4] = dados[1]  # Posição 5
        codigo[5] = dados[2]  # Posição 6
        codigo[6] = dados[3]  # Posição 7
        codigo[8] = dados[4]  # Posição 9
        codigo[9] = dados[5]  # Posição 10
        codigo[10] = dados[6] # Posição 11

        # Calcula os bits de paridade
        # Paridade P1 (Posicao 1): cobre bits 3, 5, 7, 9, 11
        p1 = (codigo[2] + codigo[4] + codigo[6] + codigo[8] + codigo[10]) % 2
        # Paridade P2 (Posicao 2): cobre bits 3, 6, 7, 10, 11
        p2 = (codigo[2] + codigo[5] + codigo[6] + codigo[9] + codigo[10]) % 2
        # Paridade P4 (Posicao 4): cobre bits 5, 6, 7
        p4 = (codigo[4] + codigo[5] + codigo[6]) % 2
        # Paridade P8 (Posicao 8): cobre bits 9, 10, 11
        p8 = (codigo[8] + codigo[9] + codigo[10]) % 2

        # Insere os bits de paridade
        codigo[0] = p1  # Posição 1
        codigo[1] = p2  # Posição 2
        codigo[3] = p4  # Posição 4
        codigo[7] = p8  # Posição 8
        
        return codigo
    
    def _calcular_posicao_erro(self, mensagem: list[int]) -> int:
        """
        Método auxilicar responsável por determinar a posição que tem erro
        """
        if len(mensagem) != 11:
            raise ValueError("A mensagem recebida deve ter exatamente 11 bits")
        
        # Isolo os bits de paridade recebido
        p1_recebido = mensagem[0]
        p2_recebido = mensagem[1]
        p4_recebido = mensagem[3]
        p8_recebido = mensagem[7]

        # Recalculo os bits de paridade
        p1_recalculado = (mensagem[2] + mensagem[4] + mensagem[6] + mensagem[8] + mensagem[10]) % 2
        p2_recalculado = (mensagem[2] + mensagem[5] + mensagem[6] + mensagem[9] + mensagem[10]) % 2
        p4_recalculado = (mensagem[4] + mensagem[5] + mensagem[6]) % 2
        p8_recalculado = (mensagem[8] + mensagem[9] + mensagem[10]) % 2

        # Comparo os bits de paridade calculados com o recebido
        # p/ o bit 1
        if p1_recebido != p1_recalculado:
            s1 = 1
        else:
            s1 = 0
        # p/ o bit 2
        if p2_recebido != p2_recalculado:
            s2 = 1
        else:
            s2 = 0
        # p/ o bit 4
        if p4_recebido != p4_recalculado:
            s4 = 1
        else:
            s4 = 0
        # p/ o bit 8
        if p8_recebido != p8_recalculado:
            s8 = 1
        else:
            s8 = 0
        
        # Calculo a posição que tem erro (calculando o binário baseado nos grupos que tem erro)
        posicao_com_erro = s1 * 1 + s2 * 2 + s4 * 4 + s8 * 8
        return posicao_com_erro

    def verificar(self, mensagem: list[int]) -> bool:
        """
        Verifica se a mensagem de 11 bits contém um erro detectável pelo Hamming
        """
        posicao_com_erro = self._calcular_posicao_erro(mensagem)
        # Se for 0 significa que não tem erro
        if posicao_com_erro == 0:
            return True
        else:
            return False
        
    def corrigir(self, mensagem: list[int]) -> list[int]:
        """
        Recebe um código de 11 bits, corrige o erro caso exista e retorna a mensagem corrigida
        """
        posicao_com_erro = self._calcular_posicao_erro(mensagem)

        codigo_corrigido = list(mensagem)

        if posicao_com_erro == 0:
            print("Nenhum erro detectado.")

        else:
            print(f"Erro detectado na posição {posicao_com_erro}, corrigindo...")
            codigo_corrigido[posicao_com_erro - 1]  ^= 1 # Flipo o bit

        # Extrai os 7 bits de dados do código já corrigido
        dados_recuperados = [
            codigo_corrigido[2],
            codigo_corrigido[4],
            codigo_corrigido[5],
            codigo_corrigido[6],
            codigo_corrigido[8],
            codigo_corrigido[9],
            codigo_corrigido[10],
        ]

        return dados_recuperados