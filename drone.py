import time
from typing import Self, Optional, Tuple, TYPE_CHECKING
import pint
import icontract

from base import Base
if TYPE_CHECKING:
    from commande import Commande
    from operateur import Operateur
    from livraison import Livraison
from tools import ureg


class Drone:
    @icontract.require(lambda id_drone, charge_utile, autonomie: id_drone > 0 and charge_utile > 0 * ureg.kg and autonomie > 0 * ureg.km,"Le drone doit avoir un ID positif et des capacités positives")
    @icontract.ensure(lambda self: self.charge_utile > 0 * ureg.kg, "La charge utile doit rester positive")
    @icontract.ensure(lambda self: self.autonomie > 0 * ureg.km, "L'autonomie doit rester positive")
    def __init__(self:Self, id_drone: int, charge_utile: pint.Quantity, autonomie: pint.Quantity):
        self.id_drone = id_drone
        self.charge_utile = charge_utile
        self.autonomie = autonomie
        self.operateur: Optional['Operateur'] = None 
        self.base: Optional[Base] = None
        self.en_mission: bool = False
        self.commande_actuelle: Optional['Commande'] = None
        self.position_actuelle: Optional[Tuple[float, float]] = None
        self.nombre_missions: int = 0
        self.poids_total_livre: pint.Quantity = 0 * ureg.kg
        self.livraison_actuelle: Optional['Livraison'] = None
        print(f"[Drone][Création] Drone {id_drone} initialisé (Charge: {charge_utile}, Autonomie: {autonomie})")


    @icontract.require(lambda self: self.en_mission, "Le drone doit être en mission pour terminer")
    @icontract.ensure(lambda self: not self.en_mission, "Le drone ne doit plus être en mission")
    @icontract.ensure(lambda self: self.commande_actuelle is None, "Aucune commande ne doit être en cours")
    def terminer_commande(self:Self) -> None:
        if not self.en_mission or not self.commande_actuelle:
            print(f"[Drone][Opération] Drone {self.id_drone} n'est pas en mission")
            return
        try:
            self.nombre_missions += 1
            poids_commande = self.commande_actuelle.poids_pillule.magnitude * ureg.kg
            self.poids_total_livre += poids_commande
            self.position_actuelle = self.commande_actuelle.arrivee.position
            self.commande_actuelle.marquer_livree()
            self.en_mission = False
            self.commande_actuelle = None
            print(f"[Drone][Opération] Drone {self.id_drone} a terminé sa mission (Total: {self.nombre_missions} missions, {self.poids_total_livre})", "Drone")
        except Exception as e:
            print(f"[Drone][Exception] Erreur lors de la terminaison de mission: {e}")
            self.en_mission = False
            self.commande_actuelle = None

    @icontract.require(lambda self, destination: destination is not None, "La destination doit être spécifiée")
    @icontract.require(lambda self: self.en_mission, "Le drone doit être en mission pour voler")
    @icontract.ensure(lambda result: result is True or result is False, "Le résultat doit être un booléen")
    def simuler_vol(self:Self, destination: Tuple[float, float]) -> bool:
        if not self.en_mission:
            print("[Drone][Warning] Drone non en mission")
            return False
        print(f"[Drone][Opération] Drone {self.id_drone} vole vers {destination}")
        self.position_actuelle = destination
        return True
    

    @icontract.require(lambda self, commande: commande is not None, "La commande doit être spécifiée")
    @icontract.require(lambda self: not self.en_mission, "Le drone ne doit pas être déjà en mission")
    @icontract.ensure(lambda self: self.en_mission, "Le drone doit être en mission après démarrage")
    @icontract.ensure(lambda self: self.commande_actuelle is not None, "Une commande doit être en cours")
    def demarrer_mission(self:Self, commande: 'Commande') -> bool:
        try:
            if self.en_mission:
                print(f"[Drone][Warning] Drone {self.id_drone} est déjà en mission")
                return False
            self.en_mission = True
            self.commande_actuelle = commande
            commande.demarrer()
            print(f"[Drone][Opération] Drone {self.id_drone} démarre la mission pour commande {commande.id_commande}")
            return True
        except Exception as e:
            print(f"[Drone][Excéption] Erreur démarrage mission drone {self.id_drone}: {e}")
            return False


    

    @icontract.require(lambda self, commande: commande is not None, "La commande doit être spécifiée")
    @icontract.require(lambda self, operateur: operateur is not None, "L'opérateur doit être spécifié")
    @icontract.require(lambda self, numero_mission: numero_mission > 0, "Le numéro de mission doit être positif")
    @icontract.require(lambda self, numero_livraison: numero_livraison > 0, "Le numéro de livraison doit être positif")
    @icontract.ensure(lambda self: not self.en_mission or self.commande_actuelle is None, "Le drone ne doit pas être en mission après exécution")
    def executer_mission_sequencee(self:Self, commande: 'Commande', operateur: 'Operateur', numero_mission: int, numero_livraison: int) -> None:
        print(f"[Drone][Opération]  Mission {numero_mission} Livraison {numero_livraison}: Drone {self.id_drone} -> {commande.arrivee.nom}")
        try:
            if self.en_mission:
                print(f"[Drone][Warning]  Drone {self.id_drone} déjà en mission")
                return
            self.operateur = operateur  
            # Démarrer la mission
            success = self.demarrer_mission(commande)
            if not success:
                print(f"[Drone][Warning]  Échec démarrage mission: {numero_mission},livraison:{numero_livraison}")
                return
            # Vol vers la destination
            print(f"[Drone][Opération]  Décollage drone {self.id_drone} pour {commande.arrivee.nom}")
            time.sleep(1)  # Simulation du vol
            # Livraison
            if self.simuler_vol(commande.arrivee.position):
                print(f"[Drone][Opération]  Drone {self.id_drone} arrivé à {commande.arrivee.nom}")
                self.terminer_commande()
                print(f"[Drone][Opération]  Mission: {numero_mission} ,livraison: {numero_livraison} réussie")
            else:
                print(f"[Drone][Opération]  Échec livraison: mission {numero_mission} ,livraison: {numero_livraison}")
                self.en_mission = False
                self.commande_actuelle = None
        except Exception as e:
            print(f"[Drone][Exception]  Erreur mission: {numero_mission} , livraison: {numero_livraison}: {e}")
            self.en_mission = False
            self.commande_actuelle = None    

    @icontract.ensure(lambda self, result: "Drone" in result and str(self.id_drone) in result, "La représentation doit contenir l'ID du drone")
    def __str__(self:Self) -> str:
        statut = "En mission" if self.en_mission else "Disponible"
        return f"Drone {self.id_drone} ({statut}, Charge: {self.charge_utile}, Autonomie: {self.autonomie})"
    