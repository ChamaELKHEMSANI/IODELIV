from typing import Optional,Self
import pint 
import icontract
from datetime import datetime

from livraison import Livraison
from base import Base
from services_etat import Services_etat
from etat import Etat 
from zone import Zone
from tools import ureg


class Commande:
    
    @icontract.require(lambda id_commande,  poids_pillule, arrivee:  id_commande > 0 and poids_pillule > 0 * ureg.kg  and arrivee is not None,"La commande doit avoir un ID positif, un poids positif et des zones valides")
    @icontract.ensure(lambda self: self.poids_pillule > 0 * ureg.kg, "Le poids doit rester positif")
    @icontract.ensure(lambda self: self.priorite > 0, "La priorité doit être positive")
    def __init__(self:Self, id_commande: int, services_etat: Services_etat, base: Base, poids_pillule: pint.Quantity, arrivee: Zone):
        self.id_commande = id_commande
        self.base = base 
        self.services_etat: Optional[Services_etat] = services_etat
        self.date =  datetime.now().strftime("%d-%m-%Y %H:%M")
        self.poids_pillule = poids_pillule
        self.depart = base.zone
        self.arrivee = arrivee 
        self.livraison: Optional[Livraison] = None 
        self.etat: Etat = Etat.A_FAIRE
        self.priorite: int = arrivee.get_priorite()
        
        print(f"[Commande][Création] Commande {id_commande} créée - {poids_pillule} vers {arrivee.nom} (Priorité: {self.priorite})", "Commande")

    @icontract.require(lambda self: self.etat.est_a_faire(), "La commande doit être à faire pour démarrer")
    @icontract.ensure(lambda self: self.etat.est_en_cours(), "La commande doit être en cours après démarrage")
    def demarrer(self:Self) -> None:
        self.etat = self.etat.demarrer()
        print(f"[Commande][Opération] Commande {self.id_commande} démarrée - Priorité: {self.priorite}")

    @icontract.require(lambda self: self.etat.est_en_cours(), "La commande doit être en cours pour être livrée")
    @icontract.ensure(lambda self: self.etat.est_terminee(), "La commande doit être terminée après livraison")
    def marquer_livree(self:Self) -> None:
        self.etat = self.etat.terminer()
        print(f"[Commande][Opération] Commande {self.id_commande} livrée avec succès à {self.arrivee.nom}")

    @icontract.ensure(lambda self, result: result in ["Terminée", "En cours", "À faire"], "Le statut doit être valide")
    def get_statut(self:Self) -> str:
        if self.etat.est_terminee():
            return "Terminée"
        elif self.etat.est_en_cours():
            return "En cours"
        else:
            return "À faire"

    @icontract.ensure(lambda self, result: "Commande" in result and str(self.id_commande) in result, "La représentation doit contenir l'ID de commande")
    def __str__(self:Self) -> str:
        return f"Commande {self.id_commande} ({self.get_statut()}) - {self.poids_pillule} vers {self.arrivee.nom}"