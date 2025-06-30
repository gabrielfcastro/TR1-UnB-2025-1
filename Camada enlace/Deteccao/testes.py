# Codigo feito por Henrique Givisiez dos Santos de matricula 211027563
from bit_paridade import BitParidade
from CRC import CRC
from detector import CamadaEnlace

if __name__ == "__main__":
    bits = [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0]

    # Teste do Bit de Paridade Par
    print("\n############ Detecção: Bit de Paridade Par ############")
    detector_paridade = CamadaEnlace(BitParidade())
    mensagem_tx = detector_paridade.transmitir(bits.copy())
    print("Mensagem transmitida com paridade:", mensagem_tx)
    resultado = detector_paridade.verificar(mensagem_tx)
    print("Paridade válida?", resultado)

    # Teste erro: inverter um bit qualquer
    mensagem_tx[5] ^= 1
    resultado = detector_paridade.verificar(mensagem_tx)
    print("Teste erro: Paridade valida?", resultado)

    # Teste do CRC-32
    print("\n############ Detecção: CRC-32 ############")
    detector_crc = CamadaEnlace(CRC())
    mensagem_tx = detector_crc.transmitir(bits.copy())
    print("Mensagem transmitida com CRC:", mensagem_tx)
    resultado = detector_crc.verificar(mensagem_tx)
    print("CRC válido?", resultado)

    # Teste erro: inverter um bit qualquer
    mensagem_tx[5] ^= 1
    resultado = detector_crc.verificar(mensagem_tx)
    print("Teste erro: Paridade valida?", resultado)
