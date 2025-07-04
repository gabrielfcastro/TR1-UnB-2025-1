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
    
    def aplicar_enquadramento(self, tipo_enquadrador: str, texto: str, tamanho_max_quadros: int) -> list[int]:
        """
        Aplica o enquadramento nos texto de acordo com o tipo especificado.
        """
        if tipo_enquadrador == "contagem_caracteres":
            enquadrador_inst = camada_enlace.CamadaEnlace(enquadrador.ContagemCaracteres())
        elif tipo_enquadrador == "flag_insercao_bytes":
            enquadrador_inst = camada_enlace.CamadaEnlace(enquadrador.InsercaoBytes())
        else:
            enquadrador_inst = camada_enlace.CamadaEnlace(enquadrador.InsercaoBits())
            
        bits = self.texto_para_bits(texto)
        quadros = []
        for i in range(0, len(bits), tamanho_max_quadros):
            bits_por_quadro = bits[i:i + tamanho_max_quadros]
            quadro_atual = enquadrador_inst.enquadrar(bits=bits_por_quadro)
            quadros.append(quadro_atual)
        return quadros

    def aplicar_edc(self, tipo_edc: str, quadros: list[list[int]]) -> list[int]:
        """
        Aplica a detecção ou correção de erros nos quadros de acordo com o tipo especificado.
        """
        if tipo_edc == "paridade_par":
            edc_inst = detector.CamadaEnlace(bit_paridade.BitParidade())
        elif tipo_edc == "crc32":
            edc_inst = detector.CamadaEnlace(CRC.CRC())
        else:
            edc_inst = detector.CamadaEnlace(hamming.Hamming())

        quadros_com_edc = []
        # Aplica EDC em cada quadro
        for quadro in quadros:
            quadro_atual = edc_inst.transmitir(quadro)
            quadros_com_edc.append(quadro_atual)
        
        return quadros_com_edc
    
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
        for quadro in enquadrador_inst.desenquadrar(bitstream):
            quadro_sem_edc = edc_inst.verificar(quadro)
            if quadro_sem_edc is not None:
                quadros_desenquadrados.append(quadro_sem_edc)

        return quadros_desenquadrados

    def bits_para_texto(self, quadros: list[list[int]]) -> str:
        texto = ""
        for quadro in quadros:
            for i in range(0, len(quadro), 8):
                byte = quadro[i:i+8]
                if len(byte) < 8: break
                texto += chr(int("".join(str(b) for b in byte), 2))
        return texto