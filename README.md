# Autonomous Vehicle Test Scenario Generator

Étude de cas : freinage d'urgence automatique (AEB, *Autonomous Emergency Braking*).

## Présentation

Ce programme Python génère automatiquement des scénarios de test pour un système AEB, calcule si la collision peut être évitée dans chaque situation, puis exporte et affiche les résultats.

L'objectif est de couvrir beaucoup plus de situations qu'avec des cas écrits à la main, et d'identifier les conditions dans lesquelles le freinage ne suffit plus. Le projet est entièrement gratuit et s'exécute en local.

## Fonctionnement

```text
Paramètres → Combinaisons (729) → Filtre (594) → Calculs → CSV / JSON → Interface Streamlit
```

## Paramètres d'entrée

| Paramètre | Valeurs |
|---|---|
| Vitesse de l'ego (km/h) | 30, 50, 80 |
| Type de cible | voiture, cycliste, piéton |
| Vitesse de la cible (km/h) | 0, 10, 30 |
| Distance à la détection (m) | 20, 40, 60 |
| État de la route (décélération) | sec (8 m/s²), mouillé (5 m/s²), verglas (2 m/s²) |
| Latence du système (s) | 0,1 ; 0,3 ; 0,5 |

Sont retirés de la génération :

- les scénarios sans rapprochement (`vitesse ego - vitesse cible <= 0`) ;
- les piétons à 30 km/h, jugés irréalistes.

## Modèle de calcul

```text
v_rel = (vitesse_ego - vitesse_cible) / 3,6
TTC = distance / v_rel
distance_necessaire = v_rel × latence + v_rel² / (2 × deceleration)
collision évitée si distance_necessaire <= distance
```

Niveau de risque, selon le TTC :

| Cible | Critique | Élevé | Modéré |
|---|---|---|---|
| Voiture | TTC < 1 s | 1 s ≤ TTC < 2 s | TTC ≥ 2 s |
| Cycliste ou piéton | TTC < 1,5 s | 1,5 s ≤ TTC < 3 s | TTC ≥ 3 s |

## Résultats

Sur les 594 scénarios valides, 168 aboutissent à une collision (28,3 %).

| Route | Collisions | Scénarios | Taux |
|---|---|---|---|
| Sec | 21 | 198 | 10,6 % |
| Mouillé | 51 | 198 | 25,8 % |
| Verglas | 96 | 198 | 48,5 % |

Le TTC ne dépend pas de l'adhérence, alors que la distance nécessaire en dépend fortement : à TTC identique, une route glissante peut rendre la collision inévitable.

Ces taux décrivent uniquement la grille de valeurs testée. Ce ne sont pas des statistiques sur des véhicules réels.

## Limites du modèle

- Modèle physique simplifié, sans dynamique du véhicule.
- Le freinage commence juste après la latence : la logique de déclenchement d'un AEB réel n'est pas simulée.
- La cible est dans la même voie, arrêtée ou roulant dans le même sens à vitesse constante. Les piétons qui traversent ne sont pas modélisés.
- Les décélérations et les seuils de risque sont des hypothèses.
- Le niveau de risque dépend du TTC et du type de cible, pas du verdict : un scénario en collision peut donc être classé « modéré ».

## Installation et utilisation

Testé avec Python 3.9.7, sous Windows.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Générer les scénarios et les fichiers de résultats :

```bash
python generateur.py
```

Lancer l'interface :

```bash
streamlit run app.py
```

## Structure du projet

| Fichier | Rôle |
|---|---|
| `scenario.py` | Fonctions de calcul (TTC, distance, verdict, risque) |
| `generateur.py` | Génération, filtrage, calculs, exports et analyse |
| `app.py` | Interface Streamlit |
| `resultats.csv`, `resultats.json` | Résultats générés |

## Pistes d'amélioration

- Simuler le freinage dans le temps avec un déclenchement selon un seuil de TTC.
- Exporter les scénarios au format OpenSCENARIO.
- Comparer le test exhaustif à une approche pairwise.
- Ajouter des tests automatisés.
