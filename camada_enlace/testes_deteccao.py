from camada_enlace.Deteccao.bit_paridade import BitParidade
from camada_enlace.Deteccao.detector import CamadaEnlace
from camada_enlace.Deteccao.CRC import CRC


def testar_detector(nome, detector, bits):
    print(f"\n############ Detecção: {nome} ############")
    
    # Transmissão normal
    print("\n--- Teste com mensagem correta ---")
    mensagem_tx = detector.transmitir(bits.copy())
    print("Mensagem transmitida:", mensagem_tx)
    resultado = detector.verificar(mensagem_tx)
    print("Mensagem ok? ", resultado)

    # Forçar 1 erro
    mensagem_erro = mensagem_tx.copy()
    mensagem_erro[5] ^= 1
    print("\n--- Teste com 1 bit invertido (posição 5) ---")
    print("Mensagem transmitida:", mensagem_erro)
    resultado = detector.verificar(mensagem_erro)
    print("Mensagem ok? ", resultado)

    # Forçar múltiplos erros
    if nome == "CRC-32":
        return
    mensagem_multi_erro = mensagem_tx.copy()
    mensagem_multi_erro[3] ^= 1
    mensagem_multi_erro[10] ^= 1
    print("\n--- Teste com mais de 1 bit invertido (posições 3 e 10) ---")
    print("Mensagem transmitida:", mensagem_multi_erro)
    resultado = detector.verificar(mensagem_multi_erro)
    print("Mensagem ok? ", resultado)

if __name__ == "__main__":
    bits = [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0]

    testar_detector("Bit de Paridade Par", CamadaEnlace(BitParidade()), bits)
    testar_detector("CRC-32", CamadaEnlace(CRC()), bits)
