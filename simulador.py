from camada_fisica.modulacoes import nrz_polar, manchester, bipolar
from camada_enlace.Enquadramento import enquadrador, camada_enlace
from camada_enlace.Deteccao import detector, bit_paridade, CRC
from camada_fisica.modulador import Modulador, CamadaFisica
from camada_enlace.correcao import hamming

class Simulador:
    def texto_para_bits(self, texto: str):
        # Converte uma string de texto em uma lista de bits.
        bits = []
        for chr in texto:
            ascii_bin = format(ord(chr), '08b')  # 8 bits por caractere
            bits.extend(int(b) for b in ascii_bin)
        return bits
    
    def aplicar_enquadramento(self, tipo_enquadrador: str, texto: str, tamanho_max_quadros: int, tipo_edc: str) -> list[list[int]]:
        # 1. Seleciona enquadrador
        if tipo_enquadrador == "contagem_caracteres":
            enquadrador_inst = camada_enlace.CamadaEnlace(enquadrador.ContagemCaracteres())
        elif tipo_enquadrador == "flag_insercao_bytes":
            enquadrador_inst = camada_enlace.CamadaEnlace(enquadrador.InsercaoBytes())
        else:
            enquadrador_inst = camada_enlace.CamadaEnlace(enquadrador.InsercaoBits())

        bits = self.texto_para_bits(texto)
        quadros = []

        # 2. Se Hamming, ignora o tamanho do quadro e divide em blocos de 7
        if tipo_edc == "hamming":
            bloco_tamanho = 7
        else:
            bloco_tamanho = tamanho_max_quadros

        for i in range(0, len(bits), bloco_tamanho):
            bloco = bits[i:i + bloco_tamanho]
            
            # ⚠️ Hamming exige exatamente 7 bits
            if tipo_edc == "hamming" and len(bloco) < 7:
                # Padding com 0s (opcional)
                bloco += [0] * (7 - len(bloco))

            bloco_com_edc = self.aplicar_edc(tipo_edc, bloco)
            quadro = enquadrador_inst.enquadrar(bloco_com_edc)
            quadros.append(quadro)

        return quadros

    

    def aplicar_edc(self, tipo_edc: str, bloco: list[int]) -> list[int]:
        """
        Aplica a detecção ou correção de erros nos quadros de acordo com o tipo especificado.
        """
        if tipo_edc == "paridade_par":
            edc_inst = detector.CamadaEnlace(bit_paridade.BitParidade())
        elif tipo_edc == "crc32":
            edc_inst = detector.CamadaEnlace(CRC.CRC())
        else:
            edc_inst = detector.CamadaEnlace(hamming.Hamming())

        return edc_inst.transmitir(bloco)
    
    def modular_digital(self, tipo_modulacao: str, quadros: list[list[int]]) -> list[int]:
        """        
        Aplica a modulação digital nos quadros de acordo com o tipo especificado.
        """
        sinais_digitais = []
        for quadro in quadros:
            sinais_digitais.extend(quadro)
        
        if tipo_modulacao == "nrz_polar":
            mod_dig_inst = CamadaFisica(nrz_polar.NRZPolar())
        elif tipo_modulacao == "manchester":
            mod_dig_inst = CamadaFisica(manchester.Manchester())
        else:
            mod_dig_inst = CamadaFisica(bipolar.Bipolar())
        
        sinais_modulados = mod_dig_inst.transmitir(sinais_digitais)
        return sinais_modulados
    
    def demodular_portadora(self, tipo: str, sinais):
        # ex.: solicitação ao Modulador ASK, FSK ou QAM8
        # retorna np.ndarray ou lista de bits
        # implemente a lógica inversa da `modular_por_portadora`
        pass

    def demodular_digital(self, tipo: str, sinais: list[int]) -> list[int]:
        """
        Demodula os sinais digitais de acordo com o tipo especificado.
        """
        if tipo == "nrz_polar":
            mod_dig_inst = CamadaFisica(nrz_polar.NRZPolar())
        elif tipo == "manchester":
            mod_dig_inst = CamadaFisica(manchester.Manchester())
        else:
            mod_dig_inst = CamadaFisica(bipolar.Bipolar())
        
        bitstream = mod_dig_inst.receber(sinais)
        
        return bitstream

    def extrair_quadros_do_bitstream(self, tipo_enq: str, bitstream: list[int]) -> list[list[int]]:
        if tipo_enq == "contagem_caracteres":
            i = 0
            quadros = []
            while i + 8 <= len(bitstream):
                tamanho = int("".join(map(str, bitstream[i:i+8])), 2)
                fim = i + 8 + tamanho
                if fim > len(bitstream): break
                quadros.append(bitstream[i:fim])
                i = fim
            return quadros

        elif tipo_enq in ["flag_insercao_bytes", "flag_insercao_bits"]:
            FLAG = [0,1,1,1,1,1,1,0]
            quadros = []
            i = 0
            while i < len(bitstream):
                try:
                    start = bitstream.index(FLAG, i) # procura o início do quadro (o método index retorna o índice da primeira ocorrência)
                    end = bitstream.index(FLAG, start + 8) # procura o fim do quadro (a partir do índice do início + 8 para evitar pegar a mesma FLAG)
                    quadros.append(bitstream[start:end+8])
                    i = end + 8
                except ValueError:
                    break
            return quadros

    def remover_edc_e_desenquadrar(self, tipo_enq: str, tipo_erro: str, bitstream: list[int]) -> list[list[int]]:
        """
        Remove EDC e desenquadra o bitstream de acordo com o tipo especificado.
        """
        if tipo_enq == "contagem_caracteres":
            enquadrador_inst = camada_enlace.CamadaEnlace(enquadrador.ContagemCaracteres())
        elif tipo_enq == "flag_insercao_bytes":
            enquadrador_inst = camada_enlace.CamadaEnlace(enquadrador.InsercaoBytes())
        else:
            enquadrador_inst = camada_enlace.CamadaEnlace(enquadrador.InsercaoBits())

        if tipo_erro == "paridade_par":
            edc_inst = detector.CamadaEnlace(bit_paridade.BitParidade())
        elif tipo_erro == "crc32":
            edc_inst = detector.CamadaEnlace(CRC.CRC())
        else:
            edc_inst = detector.CamadaEnlace(hamming.Hamming())

        # Desenquadra e remove EDC
        quadros_desenquadrados = []
        quadros_crus = self.extrair_quadros_do_bitstream(tipo_enq, bitstream)

        for quadro in quadros_crus:
            desenquadrado = enquadrador_inst.desenquadrar(quadro)
            if edc_inst.verificar(desenquadrado):
                dados = edc_inst.extrair_dados(desenquadrado)
                quadros_desenquadrados.append(dados)

        
        return quadros_desenquadrados

    def bits_para_texto(self, quadros: list[list[int]]) -> str:
        texto = ""
        bistream = []
        for quadro in quadros:
            bistream.extend(quadro)
        for i in range(0, len(bistream), 8):
            byte = bistream[i:i+8]
            if len(byte) < 8: break
            texto += chr(int("".join(str(b) for b in byte), 2))

        return texto