from camada_enlace.Enquadramento import enquadrador, camada_enlace

class Simulador:
    def texto_para_bits(self, texto: str):
        # Converte uma string de texto em uma lista de bits.
        bits = []
        for chr in texto:
            ascii_bin = format(ord(chr), '08b')  # 8 bits por caractere
            bits.extend(int(b) for b in ascii_bin)
        return bits
    
    def aplicar_enquadramento(self, tipo_enquadrador: str, texto: str) -> list[int]:
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
        quadros = enquadrador_inst.enquadrar(bits=bits)
        return quadros

