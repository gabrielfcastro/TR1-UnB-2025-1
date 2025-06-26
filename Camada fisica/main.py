# Codigo feito por Henrique Givisiez dos Santos de matricula 211027563
from modulacoes.manchester import Manchester
from modulador import CamadaFisica
from modulacoes.nrz_polar import NRZPolar
from modulacoes.bipolar import Bipolar

if __name__ == "__main__":
    bits = [1, 0, 1, 1, 0, 0, 1]

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
