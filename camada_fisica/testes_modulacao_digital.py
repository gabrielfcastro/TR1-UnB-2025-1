# Codigo feito por Henrique Givisiez dos Santos de matricula 211027563
from camada_fisica.modulacoes.manchester import Manchester
from  camada_fisica.modulacoes.nrz_polar import NRZPolar
from  camada_fisica.modulacoes.bipolar import Bipolar
from  camada_fisica.modulador import CamadaFisica
import matplotlib.pyplot as plt


def plot_trem_de_bits(bits):
    plt.figure()  # cria nova janela
    tempo = []
    valores = []
    for i, bit in enumerate(bits):
        tempo.extend([i, i + 1])
        valores.extend([bit, bit])
    plt.step(tempo, valores, where='post')
    plt.ylim(-0.5, 1.5)
    plt.title("Trem de Bits Original")
    plt.xlabel("Tempo")
    plt.ylabel("Bit")
    plt.grid(True)
    plt.show(block=False)

def plot_sinal_modulado(sinais, titulo):
    plt.figure()  # cria nova janela
    tempo = list(range(len(sinais)))
    plt.step(tempo, sinais, where='post')
    plt.title(titulo)
    plt.xlabel("Tempo")
    plt.ylabel("Sinal")
    plt.grid(True)
    plt.show(block=False)

if __name__ == "__main__":
    bits = [1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1]

    print("############ Teste NRZ Polar ############")
    nrz_polar = CamadaFisica(NRZPolar())
    sinais = nrz_polar.transmitir(bits)
    print("Sinais modulados:", sinais)
    bits_recebidos = nrz_polar.receber(sinais)
    print("Bits recebidos:", bits_recebidos)
    plot_trem_de_bits(bits)
    plot_sinal_modulado(sinais, "Sinal Modulado NRZ Polar")

    print("############ Teste Manchester ############")
    manchester = CamadaFisica(Manchester())
    sinais = manchester.transmitir(bits)
    print("Sinais modulados:", sinais)
    bits_recebidos = manchester.receber(sinais)
    print("Bits recebidos:", bits_recebidos)
    plot_sinal_modulado(sinais, "Sinal Modulado Manchester")

    print("############ Teste Bipolar ############")
    bipolar = CamadaFisica(Bipolar())
    sinais = bipolar.transmitir(bits)
    print("Sinais modulados:", sinais)
    bits_recebidos = bipolar.receber(sinais)
    print("Bits recebidos:", bits_recebidos)
    plot_sinal_modulado(sinais, "Sinal Modulado Bipolar")

    # Manter janelas abertas
    plt.pause(0.1)  # permite renderizar
    input("Pressione ENTER para fechar os gráficos...")