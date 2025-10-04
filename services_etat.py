from typing import List, Self, Optional,  TYPE_CHECKING
import icontract


if TYPE_CHECKING:
    from commande import Commande
from base import Base
from zone import Zone



class Services_etat:
    @icontract.require(lambda id, nom: id is not None and nom is not None and len(nom) > 0, "Le nom des services doit être valide")
    def __init__(self:Self, id: int, nom: str, region: str = "Région de FRANCE"):
        self.id = id
        self.nom = nom
        self.region = region
        self.liste_zones: List[Zone] = []  
        self.liste_commandes: List['Commande'] = []
        print(f"[Services État][Création] Services État {id}: {nom} ({region}) initialisés")

    @icontract.require(lambda self, zone: zone is not None, "La zone doit être spécifiée")
    def add_zone(self:Self, zone: Zone) -> None:
        self.liste_zones.append(zone)
        print(f"[Services État][Info] Zone {zone.nom} ajoutée aux services {self.nom}")

    @icontract.require(lambda self, zone_id: zone_id > 0, "L'ID de la zone doit être positif")
    @icontract.ensure(lambda result: result is None or isinstance(result, Zone), "Le résultat doit être une Zone ou None")
    def get_zone(self:Self,zone_id:int)-> Optional[Zone]:
        for objet in self.liste_zones:
            if objet.id == zone_id:
                return objet
        return None  

    @icontract.require(lambda self, commande: commande is not None ,"La commande ne doit pas être None ")
    def add_commande(self:Self, commande: 'Commande' )  -> None:
        if commande not in self.liste_commandes:
            self.liste_commandes.append(commande)
            commande.services_etat = self
            print(f"[Services État][Succes] commande {commande.id_commande} ajoutée au système")
        else:
            print(f"[Services État][Warning] commande {commande.id_commande} déjà enregistrée")


    @icontract.require(lambda self: len(self.liste_commandes) > 0  , "Le service doit avoir des commandes ")      
    def affecter_commandes(self:Self) -> None:
        
        print("[Services État][Alert]  Début de l'affectation  des commandes...")
        livraison_id_base = self.id*10000   # ID unique pour les livraisons
        

        liste_bases: List[Base] =[command.base for command in self.liste_commandes if command.base is not None]
        liste_bases = list(set(liste_bases))  # Éliminer les doublons
        if len(liste_bases)==0:
            print("[Services État] [Error] Aucune base disponible pour l'affectation des commandes")
            return    
        for base in liste_bases:
            print(f"[Services État][Info] Base disponible: {base.nom} avec {len(base.liste_operateurs)} opérateurs")
            liste_commandes_base = [cmd for cmd in self.liste_commandes if cmd.base == base]
            if len(liste_commandes_base)>0:
                print(f"[Services État][Info] Base {base.nom} a {len(liste_commandes_base)} commandes à affecter")
                base.affecter_commandes(liste_commandes_base, livraison_id_base)

    

    @icontract.ensure(lambda self, result: self.nom in result, "La représentation doit contenir le nom des services")
    def __str__(self:Self) -> str:
        return (f"Services État {self.id}:{self.nom} ({self.region})")
