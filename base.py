from typing import Self, List,Optional, TYPE_CHECKING
import icontract
import pint
if TYPE_CHECKING:
    from drone import Drone
    from commande import Commande
from zone import Zone
from operateur import Operateur
from tools import  calculer_distance,ureg


class Base:
    @icontract.require(lambda id,nom, position,capacite: id is not None and nom is not None and position is not None and len(position) == 2, "La base doit avoir un nom, une position valide ")
    @icontract.ensure(lambda self: self.capacite >= 0, "La capacité ne peut pas être négative")
    def __init__(self:Self, id: int, nom: str, position: tuple[float, float],capacite:int) -> None:
        self.id = id
        self.nom = nom
        self.position = position
        self.capacite = capacite
        self.liste_operateurs: List[Operateur] = []
        self.zone = Zone(0,nom, 0, position)  
        print(f"[Base] [Création] Base {nom} (ID: {id}) créée à la position {position}")


    @icontract.require(lambda self: self.capacite >= 0, "La capacité doit être non négative")
    @icontract.ensure(lambda self, result: isinstance(result, bool), "Le résultat doit être un booléen")
    def is_capacite_full(self) -> bool:
        total_drones = sum(len(operateur.liste_drones) for operateur in self.liste_operateurs)
        return total_drones >= self.capacite
    

    @icontract.require(lambda self, operateur: operateur is not None, "L'opérateur doit être spécifié")
    @icontract.ensure(lambda self, operateur: operateur in self.liste_operateurs, "L'opérateur doit être ajouté à la liste")
    def add_operateur(self: Self, operateur: Operateur) -> None:
        if operateur not in self.liste_operateurs:
            self.liste_operateurs.append(operateur)
            print(f"[Base] [Info] Opérateur {operateur.nom} ajouté au système par {self.nom}")
        else:
            print(f"[Base] [Warning] Opérateur {operateur.nom} déjà enregistré")


    @icontract.require(lambda self, operateur_id: operateur_id > 0, "L'ID de l'opérateur doit être positif")
    @icontract.ensure(lambda result: result is None or isinstance(result, Operateur), "Le résultat doit être un Operateur ou None")
    def get_operateur(self:Self,operateur_id:int)-> Optional[Operateur]:
        for objet in self.liste_operateurs:
            if objet.id == operateur_id:
                return objet
        return None  
    

    @icontract.require(lambda self: len(self.liste_operateurs) > 0, "La base doit avoir des opérateurs pour exécuter des livraisons")
    def executer_livraisons(self) -> None:
        for  operateur in self.liste_operateurs:
            print(f"[Base]  [Opération] base {self.nom} exécute ls livraison ")
            operateur.executer_livraisons()

    @icontract.require(lambda self, drone: drone is not None, "Le drone doit être spécifié")
    @icontract.ensure(lambda self, drone: drone in [d for op in self.liste_operateurs for d in op.liste_drones], "Le drone doit être ajouté à la liste des drones des opérateurs")
    def can_add_commande(self:Self,drone:'Drone',commande: 'Commande') -> bool:
        operateur = drone.operateur
        if not operateur:
            return False
        charge_drone = drone.charge_utile
        autonomie_drone = drone.autonomie
        poids_commande = commande.poids_pillule      

        if drone.livraison_actuelle is None:
            distance = 2 * calculer_distance(operateur.base.position, commande.arrivee.position)*ureg.km
            print(f"[Base] [Info] Vérification drone {drone.id_drone} pour commande {commande.id_commande}: Distance totale {distance} km, Autonomie drone {autonomie_drone} km, Poids total livraison {poids_commande} kg, Charge drone {charge_drone} kg")
            if distance > autonomie_drone  or poids_commande > charge_drone       :
                return False
        else:
            distance_totale:pint.Quantity=0* ureg.km
            poids_total_livraison:pint.Quantity=poids_commande
            prev_cmd: Optional['Commande'] = None
            for cmd in drone.livraison_actuelle.liste_commandes:
                poids_total_livraison = poids_total_livraison+cmd.poids_pillule
                if distance_totale==0:
                    distance_totale = calculer_distance(operateur.base.position, cmd.arrivee.position)*ureg.km
                else:
                    if prev_cmd:
                        distance_totale += calculer_distance(prev_cmd.arrivee.position, cmd.arrivee.position)*ureg.km
                prev_cmd = cmd
            if prev_cmd:
                distance_totale += calculer_distance(prev_cmd.arrivee.position, commande.arrivee.position)*ureg.km
            distance_totale += calculer_distance(commande.arrivee.position, operateur.base.position)*ureg.km
            print(f"[Base] [Info] Vérification drone {drone.id_drone} pour commande {commande.id_commande}: Distance totale {distance_totale:.2f} km, Autonomie drone {autonomie_drone} km, Poids total livraison {poids_total_livraison} kg, Charge drone {charge_drone} kg")
            if distance_totale > autonomie_drone or poids_total_livraison > charge_drone:
                return False
        return True
 

    @icontract.require(lambda self, liste_commandes_base, livraison_id_base: liste_commandes_base is not None and len(liste_commandes_base) > 0, "La liste des commandes ne doit pas être vide")
    @icontract.ensure(lambda self: True, "L'affectation des commandes doit se terminer")  
    def affecter_commandes(self:Self,liste_commandes_base: List['Commande'], livraison_id_base:int) -> None:
        from livraison import Livraison
        print(f"[Base] [Alert]  Début de l'affectation  des commandes pour la base {self.nom}...")
        if len(liste_commandes_base)==0:
            return 
        livraison_id = livraison_id_base + self.id*  100 + 1  
        liste_drones: List[Drone] =[drone  for operateur in self.liste_operateurs for drone in operateur.liste_drones]
        liste_drones.sort(key=lambda d: d.autonomie, reverse=True) 
        for drone in liste_drones:
            drone.en_mission = False
            drone.commande_actuelle = None
        commandes_non_affectees = sorted(liste_commandes_base, key=lambda c: c.priorite, reverse=True)
        for commande in commandes_non_affectees:
            print(f"[Base] [Info] Commande {commande.id_commande} (Priorité: {commande.priorite}, Poids: {commande.poids_pillule}) en attente d'affectation")   
            for drone in liste_drones:
                if self.can_add_commande(drone,commande):
                    print(f"[Base] [Info] Drone {drone.id_drone} peut  prendre la commande {commande.id_commande}")
                    livraison =drone.livraison_actuelle
                    if livraison:
                        livraison.ajouter_commande(commande)
                        print(f"[Base] [Info] Commande {commande.id_commande} ajoutée à la livraison {livraison.id_livraison} du drone {drone.id_drone}")
                        break
                    else:
                        print(f"[Base] [Info] Drone {drone.id_drone} n'a pas de livraison en cours pour la commande {commande.id_commande}")
                        operateur = drone.operateur
                        if operateur:
                            livraison = Livraison(livraison_id)
                            livraison.ajouter_commande(commande)
                            livraison.operateur_affecte = operateur
                            livraison.drones_reserves = drone
                            operateur.add_livraison(livraison)
                            drone.en_mission = True
                            drone.livraison_actuelle =livraison
                            livraison_id += 1
                            print(f"[Base] [Info] Commande {commande.id_commande} -> {operateur.nom} (Drone {drone.id_drone})")
                            break
                else:
                    print(f"[Base] [Info] Drone {drone.id_drone} ne peut pas prendre la commande {commande.id_commande} (Charge: {drone.charge_utile}, Autonomie: {drone.autonomie})")
        print(f"[Base] [Alert]  Fin de l'affectation des commandes pour la base {self.nom}.")


    @icontract.ensure(lambda self, result: self.nom in result, "La représentation doit contenir le nom de la base")
    def __str__(self:Self) -> str:
        return f"Base {self.id} : {self.nom} (Position: {self.position}, Operateurs: {len(self.liste_operateurs)})"