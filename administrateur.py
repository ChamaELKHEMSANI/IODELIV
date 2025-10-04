from typing import Self, List, Optional
import icontract


from services_etat import Services_etat
from base import Base
from drone import Drone
from commande import Commande
from livraison import Livraison


class Administrateur:
    @icontract.require(lambda nom, id_administrateur: nom is not None and id_administrateur > 0, "L'administrateur doit avoir un nom et un ID positif")
    def __init__(self: Self, nom: str, id_administrateur: int) -> None:
        self.nom = nom
        self.id_administrateur = id_administrateur
        self.liste_bases: List[Base] = []
        self.liste_services: List[Services_etat] = []



    @icontract.require(lambda self, service: service is not None, "Le service  doit être spécifié")
    @icontract.ensure(lambda self, service: service in self.liste_services, "Le service doit être ajouté à la liste")
    def add_service(self: Self, service: Services_etat) -> None:
        if service not in self.liste_services:
            self.liste_services.append(service)
            print(f"[Administrateur] Service {service.nom} ajouté au système ")
        else:
            print(f"[Administrateur] Service {service.nom} déjà enregistré")

    @icontract.require(lambda self, base: base is not None, "La base doit être spécifiée")
    @icontract.ensure(lambda self, base: base in self.liste_bases, "La base doit être ajoutée à la liste")
    def add_base(self:Self, base: Base) -> None:
        if base not in self.liste_bases:
            self.liste_bases.append(base)
            print(f"[Administrateur] Base {base.nom} ajoutée au système")
        else:
            print(f"[Administrateur] Base {base.nom} déjà enregistrée")




    @icontract.require(lambda self, service_id: service_id > 0, "L'ID du service doit être positif")
    @icontract.ensure(lambda result: result is None or isinstance(result, Services_etat), "Le résultat doit être un Service_etat ou None")
    def get_service(self:Self,service_id:int)-> Optional[Services_etat] :
        for objet in self.liste_services:
            if objet.id == service_id:
                return objet
        return None  
    


    @icontract.require(lambda self, base_id: base_id > 0, "L'ID de la base doit être positif")
    @icontract.ensure(lambda result: result is None or isinstance(result, Base), "Le résultat doit être une Base ou None")
    def get_base(self:Self,base_id:int)-> Optional[Base] :
        for objet in self.liste_bases:
            if objet.id == base_id:
                return objet
        return None  
    



    @icontract.require(lambda self: len(self.liste_services) > 0, "L'administrateur doit avoir des services pour affecter des commandes")
    @icontract.require(lambda self: len(self.liste_bases) > 0, "L'administrateur doit avoir des bases pour affecter des commandes")
    @icontract.ensure(lambda self: True, "L'exécution des livraisons doit se terminer")
    def executer_livraison(self:Self) -> None:
        print("[Administrateur] Démarrage de la Livraison ")
        print("[Administrateur] Vérification de l'état des drones...")
        total_zones = sum(len(service.liste_zones) for service in self.liste_services)    
        total_operateurs  =   sum(len(op.liste_operateurs) for op in self.liste_bases)      
        print("[Administrateur] === STATISTIQUES INITIALES ===")
        print(f"[Administrateur]  Opérateurs: {total_operateurs} | Zone: {total_zones} |  Bases: {len(self.liste_bases)} |  Services: {len(self.liste_services)}")
        for service in self.liste_services:
            if len(service.liste_commandes):
                service.affecter_commandes()
        liste_commandes: List[Commande] = [command for service in self.liste_services for command in service.liste_commandes]
        liste_livraisons: List[Livraison] = [livraison for base in self.liste_bases for operateur in base.liste_operateurs for livraison in operateur.liste_livraisons]
        print(f"[Administrateur]  Commandes: {len(liste_commandes)} |  Livraisons: {len(liste_livraisons)}")
        for base in self.liste_bases:
            if len(base.liste_operateurs):
                base.executer_livraisons()
        print("[Administrateur] Livraisons terminée avec succès")



    @icontract.require(lambda self: len(self.liste_bases) > 0, "L'administrateur doit avoir des bases pour exécuter des livraisons")
    def generer_rapport_final(self:Self) -> None:
        print("[Administrateur] === RAPPORT FINAL  ===")
        liste_livraisons: List[Livraison] = [livraison for base in self.liste_bases for operateur in base.liste_operateurs for livraison in operateur.liste_livraisons]
        liste_commandes: List[Commande] =[command for service in self.liste_services for command in service.liste_commandes]
        liste_drones: List[Drone] = [drone for base in self.liste_bases for operateur in base.liste_operateurs for drone in operateur.liste_drones]
        # Statistiques générales
        commandes_livrees = sum(1 for c in liste_commandes if c.etat.est_terminee())
        total_commandes = len(liste_commandes)
        taux_reussite = (commandes_livrees / total_commandes * 100) if total_commandes > 0 else 0
        
        print("[Administrateur] === STATISTIQUES GÉNÉRALES ===")
        print(f"[Administrateur]  COMMANDES: {commandes_livrees}/{total_commandes} ({taux_reussite:.1f}%)")
        print(f"[Administrateur]  LIVRAISONS: {len([livraison for livraison in liste_livraisons if livraison.etat.est_terminee()])}/{len(liste_livraisons)}")
        print("[Administrateur] === DÉTAILS PAR LIVRAISON ===")
        for livraison in liste_livraisons:
            if livraison.drones_reserves:
                drone_id = livraison.drones_reserves.id_drone
                print(f"[Administrateur]  Livraison {livraison.id_livraison} avec Drone {drone_id}: {len(livraison.liste_commandes)} commandes, Distance parcourue: {livraison.distance_parcourue():.2f} km")
                for commande in livraison.liste_commandes:
                    statut = "Livrée" if commande.etat.est_terminee() else "Échouée"
                    print(f"[Administrateur]    Commande {commande.id_commande}: {statut},destination:{commande.arrivee.nom}, Poids: {commande.poids_pillule}, Priorité: {commande.priorite}")
        print("[Administrateur] === DÉTAILS PAR SERVICE ===")
        for service in self.liste_services:
            cmd_service = [c for c in liste_commandes if c.services_etat == service]
            livrees_service = sum(1 for c in cmd_service if c.etat.est_terminee())
            taux_service = (livrees_service / len(cmd_service) * 100) if cmd_service else 0
            print(f"[Administrateur]  {service.nom}: {livrees_service}/{len(cmd_service)} ({taux_service:.1f}%)")
        print("[Administrateur] PERFORMANCE DES DRONES:")
        for drone in sorted( liste_drones, key=lambda d: d.id_drone, reverse=False):
            statut = "(ok)" if not drone.en_mission else "(no))"
            distance_totale= drone.livraison_actuelle.distance_parcourue() if drone.livraison_actuelle else 0.0
            print(f"[Administrateur]  Drone {drone.id_drone}: {statut} {drone.nombre_missions} missions, poids {drone.poids_total_livre} / {drone.charge_utile}, distance {distance_totale:.2f} / {drone.autonomie}")
        
   

    @icontract.ensure(lambda self, result: self.nom in result, "La représentation doit contenir le nom de l'administrateur")
    def __str__(self:Self) -> str:
        total_bases=len(self.liste_bases)
        total_services=len(self.liste_services)
        total_zones = sum(len(service.liste_zones) for service in self.liste_services)    
        total_operateurs  =   sum(len(op.liste_operateurs) for op in self.liste_bases)      
        return (f"Administrateur {self.nom} (ID: {self.id_administrateur}) - Bases: {total_bases},Service: {total_services}- Zones: {total_zones},Operateurs: {total_operateurs}")
    