from .enquadrador import Enquadrador

class CamadaEnlace:
    def __init__(self, enquadrador: Enquadrador):
        self.enquadrador = enquadrador

    def enquadrar(self, bits: list[int]) -> list[int]:
        return self.enquadrador.enquadrar(bits)

    def desenquadrar(self, quadro: list[int]) -> list[int]:
        return self.enquadrador.desenquadrar(quadro)
