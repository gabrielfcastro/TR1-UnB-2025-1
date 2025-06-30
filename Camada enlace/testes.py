from enquadrador import ContagemCaracteres, InsercaoBytes, InsercaoBits
from camada_enlace import CamadaEnlace

if __name__ == "__main__":
  bits = [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0]

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
