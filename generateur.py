import csv
import json
from itertools import product
from scenario import kmh_vers_ms, calculer_ttc, calculer_distance_necessaire, calculer_verdict, calculer_risque

vitesses_ego = [30, 50, 80]
types_cible = ["voiture", "cycliste", "pieton"]
vitesses_cible = [0, 10, 30]
distances = [20, 40, 60]
routes = ["sec","mouille", "verglas"]
latences = [0.1, 0.3, 0.5]

combinaisons = list(product(vitesses_ego, types_cible, vitesses_cible, distances, routes, latences))

print("Nombre de combinaisons :", len(combinaisons)) # 729 3**6
print("Premiere :", combinaisons[0])
print("Derniere :", combinaisons[-1])




def est_valide(combinaison):
    ego, type_cible, v_cible, distance, route, latence = combinaison

    if ego - v_cible <= 0:
        return False
    if type_cible== "pieton" and  v_cible == 30 :
        return False
    return True


scenarios_valides = []

for combinaison in combinaisons:
    if est_valide(combinaison):
        scenarios_valides.append(combinaison)

print("Scenarios valides :", len(scenarios_valides))
DECELERATIONS = {"sec": 8, "mouille": 5, "verglas": 2}

resultats = []

for scenario in scenarios_valides:
    ego, type_cible, v_cible, distance, route, latence = scenario

    v_rel = kmh_vers_ms(ego - v_cible)
    ttc = calculer_ttc(distance, v_rel)
    deceleration = DECELERATIONS[route]
    necessaire = calculer_distance_necessaire(v_rel, latence, deceleration)
    verdict = calculer_verdict(necessaire, distance)
    risque = calculer_risque(ttc, type_cible)

    resultats.append(scenario + (round(ttc, 2), round(necessaire, 2), verdict, risque))

print("Resultats :", len(resultats))
print("Exemple :", resultats[0])


colonnes = [
    "vitesse_ego_kmh", "type_cible", "vitesse_cible_kmh", "distance_m",
    "route", "latence_s", "ttc_s", "distance_necessaire_m", "verdict", "risque",
]

with open("resultats.csv", "w", newline="", encoding="utf-8") as fichier:
    writer = csv.writer(fichier, delimiter=";")
    writer.writerow(colonnes)
    writer.writerows(resultats)


print("Fichier resultats.csv cree")


scenarios_json = []

for ligne in resultats:
    scenarios_json.append(dict(zip(colonnes, ligne)))

with open("resultats.json", "w", encoding="utf-8") as fichier:
    json.dump(scenarios_json, fichier, indent=2)

print("Fichier resultats.json cree")


print("\nCollisions par route :")

for route in routes:
    lignes_route = [r for r in resultats if r[4] == route]
    collisions = [r for r in lignes_route if r[8] == "collision"]
    print(route, ":", len(collisions), "/", len(lignes_route))
