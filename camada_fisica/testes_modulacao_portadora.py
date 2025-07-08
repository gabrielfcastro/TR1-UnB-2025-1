from camada_fisica.modulacoes.qam import QAM8
import matplotlib.pyplot as plt
from camada_fisica.modulacoes.ask import ASK
from camada_fisica.modulacoes.fsk import FSK
import numpy as np

def testar_ask(bits, freq, amostras):
    mod = ASK(freq, amostras)
    sinal = mod.modular(bits)
    bits_rec = mod.demodular(sinal)
    tempo = np.linspace(0, len(bits), len(sinal))
    
    fig, axs = plt.subplots(4, 1, figsize=(10, 8))
    axs[0].plot(tempo, np.repeat(bits, amostras), 'r')
    axs[0].set_title('1. Dados Originais')
    axs[1].plot(tempo, np.cos(2 * np.pi * freq * tempo), 'g')
    axs[1].set_title(f'2. Portadora ({freq} Hz)')
    axs[2].plot(tempo, sinal, 'b')
    axs[2].set_title('3. Sinal Modulado ASK')
    axs[3].plot(tempo, np.repeat(bits_rec, amostras), 'm')
    axs[3].set_title('4. Sinal Demodulado')
    [ax.grid() for ax in axs]
    plt.tight_layout()
    plt.show()

def testar_fsk(bits, freq0, freq1, amostras):
    mod = FSK(freq0, freq1, amostras)
    sinal = mod.modular(bits)
    bits_rec = mod.demodular(sinal)
    tempo = np.linspace(0, len(bits), len(sinal))
    
    fig, axs = plt.subplots(5, 1, figsize=(10, 10))
    axs[0].plot(tempo, np.repeat(bits, amostras), 'r')
    axs[0].set_title('1. Dados Originais')
    axs[1].plot(tempo, np.cos(2 * np.pi * freq0 * tempo), 'b')
    axs[1].set_title(f'2. Portadora Bit 0 ({freq0} Hz)')
    axs[2].plot(tempo, np.cos(2 * np.pi * freq1 * tempo), 'g')
    axs[2].set_title(f'3. Portadora Bit 1 ({freq1} Hz)')
    axs[3].plot(tempo, sinal, 'm')
    axs[3].set_title('4. Sinal Modulado FSK')
    axs[4].plot(tempo, np.repeat(bits_rec, amostras), 'c')
    axs[4].set_title('5. Sinal Demodulado')
    [ax.grid() for ax in axs]
    plt.tight_layout()
    plt.show()

def testar_qam(bits, freq, amostras):
    mod = QAM8(freq, amostras)
    sinal = mod.modular(bits)
    bits_rec = mod.demodular(sinal)
    
    # Calcula pontos recebidos
    pontos_rx = []
    for i in range(0, len(sinal), amostras):
        trecho = sinal[i:i+amostras]
        i_rx = (2/amostras) * np.sum(trecho * mod._portadora_i)
        q_rx = (2/amostras) * np.sum(trecho * mod._portadora_q)
        pontos_rx.append([i_rx, q_rx])
    pontos_rx = np.array(pontos_rx)
    
    fig = plt.figure(figsize=(12, 8))
    
    # Sinal modulado
    ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2)
    ax1.plot(sinal, 'b')
    ax1.set_title('1. Sinal 8-QAM Modulado')
    ax1.grid()
    
    # Constelação com pontos ideais e recebidos
    ax2 = plt.subplot2grid((2, 2), (1, 0))
    if hasattr(mod, '_iq_ideal'):
        pontos_ideais = np.array(list(mod._iq_ideal.values()))
        ax2.scatter(pontos_ideais[:,0], pontos_ideais[:,1], c='r', marker='o', label='Ideais')
        ax2.scatter(pontos_rx[:,0], pontos_rx[:,1], c='b', marker='x', label='Recebidos')
        ax2.set_title('2. Constelação (Ideais vs Recebidos)')
        ax2.axis('equal')
        ax2.grid()
        ax2.legend()
    
    # Bits demodulados
    ax3 = plt.subplot2grid((2, 2), (1, 1))
    ax3.stem(bits_rec, linefmt='b-', markerfmt='bo', basefmt=' ')
    ax3.set_title('3. Bits Demodulados')
    ax3.set_ylim(-0.1, 1.1)
    ax3.grid()
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    testar_ask([1,0,1,1,0], 10, 100)
    testar_fsk([1,0,1,1,0], 10, 20, 100)
    testar_qam([1,0,1,0,0,0,1,1,1], 10, 100)