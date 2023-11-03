

from models.database import Database

"""
Nessa classe vou pesquisar, adicionar e salvar em um arquivo uma lista de farms por aldeia.
para usar essa função sem precisar comprar club dourado

"""
class Farm:
    def __init__(self, travian):
        self.travian = travian
        self.database = Database(self.travian)

    def write(self):
        pass