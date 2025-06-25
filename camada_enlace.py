from enlace.enquadrador import Enquadrador

class CamadaEnlace:
    def __init__(self, enquadrador: Enquadrador):
        self.enquadrador = enquadrador

    def transmitir(self, bits: list[int]) -> list[int]:
        return self.enquadrador.enquadrar(bits)

    def receber(self, quadro: list[int]) -> list[int]:
        return self.enquadrador.desenquadrar(quadro)
