from typing import  List, Optional,  TYPE_CHECKING
import icontract

from etat import Etat
from drone import Drone
from operateur import Operateur
from tools import  calculer_distance

if TYPE_CHECKING:
    from commande import Commande

class Livraison:
    @icontract.require(lambda id_livraison: id_livraison > 0, "L'ID de livraison doit être positif")
    def __init__(self, id_livraison: int):
        self.id_livraison = id_livraison
        self.liste_commandes: List['Commande'] = []
        self.etat: Etat = Etat.A_FAIRE
        self.operateur_affecte: Optional[Operateur] = None  
        self.drones_reserves: Optional[Drone] = None   
        print(f"[Livraison] [Création] Livraison {id_livraison} créée", "Livraison")

    @icontract.require(lambda self, commande: commande is not None, "La commande doit être spécifiée")
    @icontract.ensure(lambda self: len(self.liste_commandes) > 0, "La livraison doit contenir au moins une commande après ajout")
    def ajouter_commande(self, commande: 'Commande') -> None:
        self.liste_commandes.append(commande)
        commande.livraison = self
        print(f"[Livraison] [Info] Commande {commande.id_commande} ajoutée à la livraison {self.id_livraison}", "Livraison")
                
    @icontract.ensure(lambda self, result: result in ["Terminée", "En cours", "À faire"], "Le statut doit être valide")
    def get_statut(self) -> str:
        if self.etat.est_terminee():
            return "Terminée"
        elif self.etat.est_en_cours():
            return "En cours"
        else:
            return "À faire"

    @icontract.require(lambda self, numero: numero > 0, "Le numéro de livraison doit être positif")
    @icontract.ensure(lambda self: self.etat.est_terminee() or self.etat.est_a_faire(), "La livraison doit être terminée ou à faire après exécution")
    def executer_livraison(self, numero: int) -> None:
        print(f"[Livraison] [info] Livraison {numero}: {len(self.liste_commandes)} commandes")
        try:
            self.etat = self.etat.demarrer()
            if not self.drones_reserves:
                print(f"[Livraison] [Erreur]  Aucun drone réservé pour la livraison {numero}")
                return
            drone = self.drones_reserves
            operateur = self.operateur_affecte
            if not operateur:
                print(f"[Livraison] [Erreur]  Aucun opérateur affecté pour la livraison {numero}")
                return
            for i, commande in enumerate(self.liste_commandes, 1):
                drone.executer_mission_sequencee(commande, operateur, i, numero)
            self.etat = self.etat.terminer()
            print(f"[Livraison] [Succes]  Livraison {numero} terminée ({len(self.liste_commandes)} commandes)")
        except Exception as e:
            print(f"[Livraison] [Exception]  Erreur livraison {numero}: {e}", )


    @icontract.ensure(lambda self, result: result >= 0, "La distance parcourue doit être non négative")
    @icontract.require(lambda self: self.operateur_affecte is not None and self.drones_reserves is not None, "L'opérateur et le drone doivent être affectés pour calculer la distance parcourue")
    def distance_parcourue(self) -> float:

        distance_totale:float=0
        operateur = self.operateur_affecte
        drone = self.drones_reserves
        if not operateur or not drone:
            return 0.0
        prev_cmd: Optional['Commande'] = None
        for cmd in self.liste_commandes:
            if distance_totale==0:
                distance_totale = calculer_distance(operateur.base.position, cmd.arrivee.position)
            else:
                if prev_cmd:
                    distance_totale += calculer_distance(prev_cmd.arrivee.position, cmd.arrivee.position)
            prev_cmd = cmd
        if prev_cmd:
            distance_totale += calculer_distance(prev_cmd.arrivee.position, operateur.base.position)
        return distance_totale




    @icontract.ensure(lambda self, result: "Livraison" in result and str(self.id_livraison) in result, "La représentation doit contenir l'ID de livraison")
    def __str__(self) -> str:
        return f"Livraison {self.id_livraison} ({self.get_statut()}) - {len(self.liste_commandes)} commandes"
