from tools import ureg
from services_etat import Services_etat
from zone import Zone
from base import Base
from operateur import Operateur
from drone import Drone
from commande import Commande
from administrateur import Administrateur


def main() -> None:
    """Fonction principale"""
    try:
        print("DÉMARRAGE ", "main")
        print("Étape 1: Chargement configuration") 


        administrateur = Administrateur("Admin Principal", 1)
        if not administrateur:
            raise ValueError("Échec de la création de l'administrateur")
        # Création des services d'état et leurs zones
        ## Service SDIS-38
        service_sdis_38 = Services_etat(1, "SDIS-38", "Isère")
        zone_grenoble = Zone(1, "Grenoble Centre", 1000, (45.1885, 5.7245))
        zone_villard = Zone(2, "Villard-de-Lans", 4000, (45.0700, 5.5500))
        zone_alpe_huez = Zone(3, "Alpe-d'Huez", 1800, (45.0925, 6.0694))
        zone_deux_alpes = Zone(4, "Les Deux-Alpes", 5200, (45.0114, 6.1250))
        zone_chamrousse = Zone(5, "Chamrousse", 800, (45.1100, 5.8800))

        service_sdis_38.add_zone(zone_grenoble)
        service_sdis_38.add_zone(zone_villard)
        service_sdis_38.add_zone(zone_alpe_huez)
        service_sdis_38.add_zone(zone_deux_alpes)
        service_sdis_38.add_zone(zone_chamrousse)

        ## Service SDIS-73
        service_sdis_73 = Services_etat(2, "SDIS-73", "Savoie")
        zone_chambery = Zone(6, "Chambéry", 2000, (45.5646, 5.9178))
        zone_courchevel = Zone(7, "Courchevel", 2500, (45.4150, 6.6350))
        zone_val_thorens = Zone(8, "Val Thorens", 3500, (45.2972, 6.5833))

        service_sdis_73.add_zone(zone_chambery)
        service_sdis_73.add_zone(zone_courchevel)
        service_sdis_73.add_zone(zone_val_thorens)

        # Ajout des services à l'administrateur
        administrateur.add_service(service_sdis_38)
        administrateur.add_service(service_sdis_73)

        # Création des bases principales
        ## Base Alpes Nord
        base_alpes_nord = Base(1, "Base Alpes Nord", (45.1885, 5.7245),10)

        ## Base Savoie Sud
        base_savoie_sud = Base(2, "Base Savoie Sud", (45.5646, 5.9178),8)

        # Ajout des bases à l'administrateur
        administrateur.add_base(base_alpes_nord)
        administrateur.add_base(base_savoie_sud)

        # Création des opérateurs et drones
        ## Opérateur Alpes Drone Express
        operateur_alpes = Operateur(1, "Alpes Drone Express", base_alpes_nord)
        drone_alpes_1 = Drone(1, 6.0 * ureg.kg, 80.0 * ureg.km)
        drone_alpes_2 = Drone(2, 4.0 * ureg.kg, 90.0 * ureg.km)
        drone_alpes_3 = Drone(3, 7.0 * ureg.kg, 70.0 * ureg.km)

        operateur_alpes.add_drone(drone_alpes_1)
        operateur_alpes.add_drone(drone_alpes_2)
        operateur_alpes.add_drone(drone_alpes_3)

        ## Opérateur Savoie Drone Services
        operateur_savoie = Operateur(2, "Savoie Drone Services", base_savoie_sud)
        drone_savoie_4 = Drone(4, 5.0 * ureg.kg, 120.0 * ureg.km)
        drone_savoie_5 = Drone(5, 4.0 * ureg.kg, 130.0 * ureg.km)


        operateur_savoie.add_drone(drone_savoie_4)
        operateur_savoie.add_drone(drone_savoie_5)


        # Ajout des opérateurs aux bases
        base_alpes_nord.add_operateur(operateur_alpes)
        base_savoie_sud.add_operateur(operateur_savoie)

        # Création des commandes du scénario
        ## Commandes pour SDIS-38 depuis Base Alpes Nord

        # Commandes de 3.0kg vers les zones 1, 2, 3
        commande1 = Commande(1, service_sdis_38, base_alpes_nord, 3.0 * ureg.kg, zone_grenoble)
        commande2 = Commande(2, service_sdis_38, base_alpes_nord, 3.0 * ureg.kg, zone_villard)
        commande3 = Commande(3, service_sdis_38, base_alpes_nord, 3.0 * ureg.kg, zone_alpe_huez)
        # Commandes de 2.5kg vers les zones 4, 5
        commande4 = Commande(4, service_sdis_38, base_alpes_nord, 2.5 * ureg.kg, zone_deux_alpes)
        commande5 = Commande(5, service_sdis_38, base_alpes_nord, 2.5 * ureg.kg, zone_chamrousse)
        service_sdis_38.add_commande(commande1) 
        service_sdis_38.add_commande(commande2) 
        service_sdis_38.add_commande(commande3)
        service_sdis_38.add_commande(commande4)     
        service_sdis_38.add_commande(commande5) 


        ## Commandes pour SDIS-73 depuis Base Savoie Sud

        # Commandes de 2.0kg vers les zones 6, 7, 8
        commande6 = Commande(6, service_sdis_73, base_savoie_sud, 2.0 * ureg.kg, zone_chambery)
        commande7 = Commande(7, service_sdis_73, base_savoie_sud, 2.0 * ureg.kg, zone_courchevel)
        commande8 = Commande(8, service_sdis_73, base_savoie_sud, 2.0 * ureg.kg, zone_val_thorens)
        service_sdis_73.add_commande(commande6) 
        service_sdis_73.add_commande(commande7) 
        service_sdis_73.add_commande(commande8)


        print("[Main] Tous les objets créés avec succès de façon statique")
        print(f"[Main] Administrateur: {administrateur.nom}, Services: {len(administrateur.liste_services)}, Bases: {len(administrateur.liste_bases)}", "creation")    
        print("[Main] Étape 2: Livraison") 

        administrateur.executer_livraison()

        print("[Main] Étape 3: Rapport") 
        administrateur.generer_rapport_final()
    except Exception as e:
        print(f"[Main] Erreur critique: {e}")
        raise

if __name__ == "__main__":
     main()
