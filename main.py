# Codigo feito por Henrique Givisiez dos Santos de matricula 211027563

from modulador_digital import CamadaFisica
from modulacoes.nrzPolar import NRZPolar
from modulacoes.manchester import Manchester
from modulacoes.bipolar import Bipolar

from enlace.enquadrador import ContagemCaracteres, InsercaoBytes, InsercaoBits
from enlace.camada_enlace import CamadaEnlace

if __name__ == "__main__":
    bits = [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0]
  #  bits = [1, 0, 1, 1, 0, 0, 1, 1, 1, 1 ,1 ,1 ,1 ,1 , 1, 0]
    # Teste da camada fisica com a modulacao NRZ Polar

    print("############ Teste NRZ Polar ############")
    nrz_polar = CamadaFisica(NRZPolar())

    sinais = nrz_polar.transmitir(bits)
    print("Sinais modulados:", sinais)

    bits_recebidos = nrz_polar.receber(sinais)
    print("Bits recebidos:", bits_recebidos)

    # Teste da camada fisica com a modulacao Manchester

    print("############ Teste Manchester ############")
    manchester = CamadaFisica(Manchester())

    sinais = manchester.transmitir(bits)
    print("Sinais modulados:", sinais)

    bits_recebidos = manchester.receber(sinais)
    print("Bits recebidos:", bits_recebidos)

    # Teste da camada fisica com a modulacao Bipolar

    print("############ Teste Bipolar ############")
    bipolar = CamadaFisica(Bipolar())

    sinais = bipolar.transmitir(bits)

    print("Sinais modulados:", sinais)

    bits_recebidos = bipolar.receber(sinais)
    print("Bits recebidos:", bits_recebidos)

    # Teste da camada de enlace - Contagem de Caracteres
    print("\n############ Enlace: Contagem de Caracteres ############")
    enlace_contagem = CamadaEnlace(ContagemCaracteres())
    quadro = enlace_contagem.transmitir(bits)
    print("Bits enquadrados:", quadro)
    dados = enlace_contagem.receber(quadro)
    print("Bits desenquadrados:", dados)

    # Teste da camada de enlace - Insercao de Bytes
    print("\n############ Enlace: Insercao de Bytes ############")
    enlace_bytes = CamadaEnlace(InsercaoBytes())
    quadro = enlace_bytes.transmitir(bits)
    print("Bits enquadrados:", quadro)
    dados = enlace_bytes.receber(quadro)
    print("Bits desenquadrados:", dados)

    # Teste da camada de enlace - Insercao de Bits
    print("\n############ Enlace: Insercao de Bits ############")
    enlace_bits = CamadaEnlace(InsercaoBits())
    quadro = enlace_bits.transmitir(bits)
    print("Bits enquadrados:", quadro)
    dados = enlace_bits.receber(quadro)
    print("Bits desenquadrados:", dados)
