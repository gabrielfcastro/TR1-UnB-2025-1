#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulador

Este módulo implementa a lógica de simulação das camadas de enlace e física
para transmissão e recepção de dados. Ele inclui:
- Conversão entre texto e bits
- Enquadramento e desenquadramento
- Detecção e correção de erros (EDC)
- Modulação e demodulação digital
- Interfaces com os módulos ASK, FSK, QAM, NRZ, Manchester, Bipolar
"""

# Importações das camadas física e de enlace
from camada_fisica.modulacoes import nrz_polar, manchester, bipolar
from camada_enlace.Enquadramento import enquadrador, camada_enlace
from camada_enlace.Deteccao import detector, bit_paridade, CRC
from camada_fisica.modulador import Modulador, CamadaFisica
from camada_enlace.correcao import hamming

class Simulador:
    def texto_para_bits(self, texto: str):
        """
        Converte um texto em uma lista de bits (8 bits por caractere ASCII).
        """
        bits = []
        for chr in texto:
            ascii_bin = format(ord(chr), '08b')  # codifica cada caractere em 8 bits
            bits.extend(int(b) for b in ascii_bin)
        return bits

    def aplicar_enquadramento(self, tipo_enquadrador: str, texto: str, tamanho_max_quadros: int, tipo_edc: str) -> list[list[int]]:
        """
        Aplica enquadramento e EDC (detecção/correção de erros) aos bits da mensagem.
        Divide a mensagem em blocos e aplica o enquadramento selecionado.

        - tipo_enquadrador: tipo de enquadramento (contagem_caracteres, flag_insercao_bytes, flag_insercao_bits)
        - tipo_edc: paridade_par, crc32, hamming
        """
        # 1. Instancia o enquadrador apropriado
        if tipo_enquadrador == "contagem_caracteres":
            enquadrador_inst = camada_enlace.CamadaEnlace(enquadrador.ContagemCaracteres())
        elif tipo_enquadrador == "flag_insercao_bytes":
            enquadrador_inst = camada_enlace.CamadaEnlace(enquadrador.InsercaoBytes())
        else:
            enquadrador_inst = camada_enlace.CamadaEnlace(enquadrador.InsercaoBits())

        bits = self.texto_para_bits(texto)
        quadros = []

        # 2. Divide a mensagem em blocos
        bloco_tamanho = 7 if tipo_edc == "hamming" else tamanho_max_quadros

        for i in range(0, len(bits), bloco_tamanho):
            bloco = bits[i:i + bloco_tamanho]

            # Preenchimento se o bloco estiver incompleto (apenas para Hamming)
            if tipo_edc == "hamming" and len(bloco) < 7:
                bloco += [0] * (7 - len(bloco))

            # 3. Aplica EDC e enquadramento
            bloco_com_edc = self.aplicar_edc(tipo_edc, bloco)
            quadro = enquadrador_inst.enquadrar(bloco_com_edc)
            quadros.append(quadro)

        return quadros

    def aplicar_edc(self, tipo_edc: str, bloco: list[int]) -> list[int]:
        """
        Aplica o método de detecção ou correção de erros sobre um bloco de bits.
        """
        if tipo_edc == "paridade_par":
            edc_inst = detector.CamadaEnlace(bit_paridade.BitParidade())
        elif tipo_edc == "crc_32":
            edc_inst = detector.CamadaEnlace(CRC.CRC())
        else:
            edc_inst = detector.CamadaEnlace(hamming.Hamming())

        return edc_inst.transmitir(bloco)

    def modular_digital(self, tipo_modulacao: str, quadros: list[list[int]]) -> list[int]:
        """
        Aplica a modulação digital (baseband) sobre os bits dos quadros.
        - tipo_modulacao: "nrz_polar", "manchester", "bipolar"
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

    def demodular_digital(self, tipo: str, sinais: list[int]) -> list[int]:
        """
        Realiza a demodulação digital (converte sinal → bits).
        """
        if tipo == "nrz_polar":
            mod_dig_inst = CamadaFisica(nrz_polar.NRZPolar())
        elif tipo == "manchester":
            mod_dig_inst = CamadaFisica(manchester.Manchester())
        else:
            mod_dig_inst = CamadaFisica(bipolar.Bipolar())

        bitstream = mod_dig_inst.receber(sinais)
        return bitstream

    def encontrar_sublista(self, lista: list[int], sublista: list[int], inicio: int = 0) -> int:
        """
        Retorna o índice da primeira ocorrência de sublista em lista a partir de 'inicio'.
        Retorna -1 se não for encontrada.
        """
        for i in range(inicio, len(lista) - len(sublista) + 1):
            if lista[i:i + len(sublista)] == sublista:
                return i
        return -1

    def extrair_quadros_do_bitstream(self, tipo_enq: str, bitstream: list[int]) -> list[list[int]]:
        """
        Extrai os quadros do bitstream, baseado no protocolo de enquadramento.
        """
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
                start = self.encontrar_sublista(bitstream, FLAG, i)
                if start == -1:
                    break

                end = self.encontrar_sublista(bitstream, FLAG, start + len(FLAG))
                if end == -1:
                    break

                # Conteúdo entre as flags
                quadro = bitstream[start:end+8]
                quadros.append(quadro)

                # Próxima busca começa após a segunda flag
                i = end + len(FLAG)
            return quadros

    def remover_edc_e_desenquadrar(self, tipo_enq: str, tipo_erro: str, bitstream: list[int]) -> list[list[int]]:
        """
        Remove o enquadramento e o EDC dos quadros recebidos.
        """
        # print(bitstream)

        if tipo_enq == "contagem_caracteres":
            enquadrador_inst = camada_enlace.CamadaEnlace(enquadrador.ContagemCaracteres())
        elif tipo_enq == "flag_insercao_bytes":
            enquadrador_inst = camada_enlace.CamadaEnlace(enquadrador.InsercaoBytes())
        else:
            enquadrador_inst = camada_enlace.CamadaEnlace(enquadrador.InsercaoBits())

        if tipo_erro == "paridade_par":
            edc_inst = detector.CamadaEnlace(bit_paridade.BitParidade())
        elif tipo_erro == "crc_32":
            edc_inst = detector.CamadaEnlace(CRC.CRC())
        else:
            edc_inst = detector.CamadaEnlace(hamming.Hamming())

        quadros_desenquadrados = []
        quadros_crus = self.extrair_quadros_do_bitstream(tipo_enq, bitstream)

        print(quadros_crus)
        for quadro in quadros_crus:
            desenquadrado = enquadrador_inst.desenquadrar(quadro)
            if edc_inst.verificar(desenquadrado):
                dados = edc_inst.extrair_dados(desenquadrado)
                quadros_desenquadrados.append(dados)

        return quadros_desenquadrados

    def bits_para_texto(self, quadros: list[list[int]]) -> str:
        """
        Converte quadros de bits de volta para uma string de texto.
        """
        texto = ""
        bistream = []
        for quadro in quadros:
            bistream.extend(quadro)

        for i in range(0, len(bistream), 8):
            byte = bistream[i:i+8]
            if len(byte) < 8: break
            texto += chr(int("".join(str(b) for b in byte), 2))

        return texto
