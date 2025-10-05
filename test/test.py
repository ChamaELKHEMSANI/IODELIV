
import pytest



from tools import ureg

from main import main
from zone import Zone
from base import Base
from drone import Drone
from operateur import Operateur
from commande import Commande
from livraison import Livraison
from services_etat import Services_etat
from administrateur import Administrateur
from etat import Etat

class TestZone:
    
    def test_creation_zone(self):
        zone = Zone(1,"TestZone", 500, (45.0, 5.0))
        assert zone.nom == "TestZone"
        assert zone.nombre_personnes == 500
        assert zone.position == (45.0, 5.0)
    



class TestDrone:
    
    def test_creation_drone(self):
        drone = Drone(1, 5 * ureg.kg, 50 * ureg.km)
        assert drone.id_drone == 1
    

class TestOperateur:
    
    def test_creation_operateur(self):
        zone_dep = Zone(1,"Dep", 0, (0, 0))
        operateur = Operateur(1,"TestOp",zone_dep)
        assert operateur.nom == "TestOp"
        assert operateur.id == 1

class TestCommande:
    
    def test_creation_commande(self):
        base = Base(1,"base",  (0, 0),100)
        zone_arr = Zone(2,"Arr", 100, (1, 1))
        services = Services_etat(1,"SDIS-Test")       
        commande = Commande(1,services,base,  2 * ureg.kg,  zone_arr)
        assert commande.id_commande == 1

class TestServicesEtat:
    
    def test_creation_services(self):
        services = Services_etat(1,"SDIS-Test")
        assert services.nom == "SDIS-Test"
    
    def test_alertes_sans_commande(self):
        base = Base(1,"base",  (0, 0),100)
        services = Services_etat(1,"SDIS-Test")
        livraison = Livraison(1)
        zone = Zone(2,"TestZone", 100, (0, 0))
        
        zone_dep = Zone(2,"Dep", 0, (0, 0))
        commande = Commande(1,services,base,  1 * ureg.kg, zone)
        
class TestScenario:
    def test_scenario_complet(self):
    # Tester un scénario end-to-end
        main()



def run_tests():
    print("LANCEMENT DES TESTS UNITAIRES ")
    
    pytest.main([__file__, "-v", "--tb=short"])

if __name__ == "__main__":
    run_tests()
