from typing import Self
import icontract

class Zone:
    @icontract.require(lambda id,nom, nombre_personnes, position: id is not None and nom is not None and nombre_personnes >= 0 and position is not None and len(position) == 2, "La zone doit avoir un nom, un nombre de personnes positif et une position valide")
    @icontract.ensure(lambda self: self.nombre_personnes >= 0, "Le nombre de personnes ne peut pas être négatif")
    def __init__(self:Self, id: int, nom: str, nombre_personnes: int, position: tuple[float, float]):
        self.id = id
        self.nom = nom
        self.nombre_personnes = nombre_personnes
        self.position = position  # (latitude, longitude)


    @icontract.ensure(lambda self, result: result >0, "La priorité doit être >0")
    def get_priorite(self:Self) -> int:
        return self.nombre_personnes 



    
    @icontract.ensure(lambda self, result: self.nom in result, "La représentation doit contenir le nom de la zone")
    def __str__(self:Self) -> str:
        return f"Zone {self.id} : {self.nom} ({self.nombre_personnes} personnes, priorité: {self.get_priorite()})"
    