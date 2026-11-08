def kmh_vers_ms(vitesse_kmh):
    return vitesse_kmh / 3.6


def calculer_ttc(distance, v_rel):
    return distance / v_rel


def calculer_distance_necessaire(v_rel, latence, deceleration):
    return v_rel * latence + v_rel ** 2 / (2 * deceleration)


def calculer_verdict(distance_necessaire, distance):
    if distance_necessaire <= distance:
        return "collision evitee"
    else:
        return "collision"


def calculer_risque(ttc, type_cible):
    if type_cible == "voiture":
        seuil_critique = 1
        seuil_eleve = 2
    else:
        seuil_critique = 1.5
        seuil_eleve = 3

    if ttc < seuil_critique:
        return "critique"
    elif ttc < seuil_eleve:
        return "eleve"
    else:
        return "modere"


if __name__ == "__main__":
    v_rel = kmh_vers_ms(50 - 10)
    print("v_rel :", v_rel)
    print("TTC :", calculer_ttc(40, v_rel))
    necessaire = calculer_distance_necessaire(v_rel, 0.3, 5)
    print("Distance necessaire :", necessaire)
    print("A :", calculer_verdict(25, 60))
    print("B :", calculer_verdict(35, 20))
    print("C :", calculer_verdict(40, 40))
    print("Risque cycliste :", calculer_risque(3.6, "cycliste"))
    print("Risque voiture :", calculer_risque(1.5, "voiture"))
    print("Risque pieton :", calculer_risque(1.2, "pieton"))
