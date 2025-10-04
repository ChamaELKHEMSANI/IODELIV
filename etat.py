from enum import Enum

class Etat(Enum):
    A_FAIRE = "À faire"
    EN_COURS = "En cours"
    TERMINEE = "Terminée"
    
    def est_a_faire(self) -> bool:
        return self == Etat.A_FAIRE
    
    def est_en_cours(self) -> bool:
        return self == Etat.EN_COURS
    
    def est_terminee(self) -> bool:
        return self == Etat.TERMINEE
    
    def demarrer(self) -> "Etat":
        if not self.est_a_faire():
            raise ValueError("Seul un état 'à faire' peut être démarré")
        return Etat.EN_COURS
    
    def terminer(self) -> "Etat":
        if not self.est_en_cours():
            raise ValueError("Seul un état 'en cours' peut être terminé")
        return Etat.TERMINEE