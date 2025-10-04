from typing import List,Self,  TYPE_CHECKING
import icontract

if TYPE_CHECKING:
    from drone import Drone
    from base import Base
    from livraison import Livraison


class Operateur:
    @icontract.require(lambda id, nom: nom is not None and id > 0, "L'opérateur doit avoir un nom et un ID positif")
    def __init__(self:Self, id: int, nom: str, base: 'Base') -> None:
        self.nom = nom
        self.id = id
        self.base = base
        self.liste_drones: list['Drone'] = []
        self.liste_livraisons: List[Livraison] = []
        print(f"[Opérateur] [Création] Opérateur {nom} (ID: {id}) créé")

    @icontract.require(lambda self, drone: drone is not None, "Le drone doit être spécifié")
    @icontract.ensure(lambda self, drone: drone in self.liste_drones, "Le drone doit être ajouté à la liste")
    def add_drone(self:Self, drone: 'Drone') -> None:
        if not self.base.is_capacite_full():
            if drone not in self.liste_drones:
                self.liste_drones.append(drone)
                drone.operateur = self
                print(f"[Opérateur][Succes] drone {drone.id_drone} ajoutée au système")
            else:
                print(f"[Opérateur][Warning] drone {drone.id_drone} déjà enregistrée")
        else:
            print(f"[Opérateur][Erreur] Capacité maximale atteinte pour la base {self.base.nom}. Impossible d'ajouter le drone {drone.id_drone}.")

    @icontract.require(lambda self, livraison: livraison is not None, "La livraison doit être spécifiée")
    @icontract.ensure(lambda self, livraison: livraison in self.liste_livraisons, "La livraison doit être ajouté à la liste")
    def add_livraison(self:Self, livraison: 'Livraison') -> None:
        if livraison not in self.liste_livraisons:
            self.liste_livraisons.append(livraison)
            livraison.operateur_affecte = self
            print(f"[Opérateur][Succes] livraison {livraison.id_livraison} ajoutée à l'Opérateur")
        else:
            print(f"[Opérateur][Warning] livraison {livraison.id_livraison} déjà enregistrée")

    @icontract.require(lambda self: len(self.liste_livraisons) > 0, "L'opérateur doit avoir des livraisons à exécuter")
    @icontract.ensure(lambda self: all(livraison.etat.est_en_cours() or livraison.etat.est_terminee() for livraison in self.liste_livraisons), "Toutes les livraisons doivent être en cours ou terminées après exécution")
    def executer_livraisons(self:Self) -> None:
        drones_reset = 0
        for drone in self.liste_drones:
            if drone.en_mission:
                drone.en_mission = False
                drone.commande_actuelle = None
                drones_reset += 1
        if drones_reset > 0:
            print(f"[Opérateur][Info] Opérateur {self.nom} , {drones_reset} drones réinitialisés")
        for livraison in self.liste_livraisons:
            nb_commandes = len(livraison.liste_commandes)
            drone_id = livraison.drones_reserves.id_drone if livraison.drones_reserves else "N/A"
            print(f"[Opérateur][Info]  Livraison {livraison.id_livraison}: {nb_commandes} commandes avec Drone {drone_id}")
            print(f"[Opérateur][Opération]  Opérateur {self.nom} exécute la livraison {livraison.id_livraison}")
            livraison.executer_livraison(livraison.id_livraison)
            print(f"[Opérateur][Succes]  Livraison {livraison.id_livraison} terminée avec succès")

    @icontract.require(lambda self: self.nom is not None, "L'opérateur doit avoir un nom")
    @icontract.ensure(lambda self, result: self.nom in result, "La représentation doit contenir le nom de l'opérateur")
    def __str__(self:Self) -> str:
        return f"Opérateur {self.nom} (ID: {self.id}, Drones: {len(self.liste_drones)})"