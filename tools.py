from typing import  Tuple
import pint
import icontract
import math



# Créer une seule instance globale
ureg = pint.UnitRegistry()


@icontract.require(lambda  pos1: pos1 is not None and len(pos1) == 2, "La position 1 doit être un tuple de 2 éléments")
@icontract.require(lambda  pos2: pos2 is not None and len(pos2) == 2, "La position 2 doit être un tuple de 2 éléments")
@icontract.ensure(lambda result: result >= 0, "La distance ne peut pas être négative")
def calculer_distance( pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
    #distance= sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)#metode de calcul de distance euclidienne inefficace
    
    # Formule de Haversine
    try:
        if pos1 == pos2:
            return 0.0
        lat1, lon1 = math.radians(pos1[0]), math.radians(pos1[1])
        lat2, lon2 = math.radians(pos2[0]), math.radians(pos2[1])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        R = 6371.0  # Rayon terrestre en km
        distance = R * c
        #print(f"[Tools] Calcul distance entre {pos1} et {pos2}: {distance:.2f} km" )
        return distance
        
    except (ValueError, TypeError) as e:
        print(f"Erreur: {e}")
        return 0.0   


