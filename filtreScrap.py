import json
import csv
import os
from collections import defaultdict


TYPES_INUTILES = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    24, 25, 26, 27, 28, 29, 30, 32, 33, 34, 43, 46, 48, 49, 50, 53, 54, 55,
    56, 57, 58, 59, 60, 63
]


TYPE_22_INUTILES = [13, 27, 28, 29, 30, 32, 33, 37, 40, "VAZIO"]


TYPES_UTILES = [21, 31, 35, 36, 37, 41, 42, 45, 47, 61, 62]


TYPE_22_UTILES = [31, 38, 47, 53]

NOMS_CATEGORIES = {
    "21": "Mochila",
    "22.31": "Mascara_Pedra_Invoc",
    "22.38": "Montaria",
    "22.47": "Trono",
    "22.53": "Nucleo",
    "31": "Roupa_Sprite",
    "35": "Skins_Cabeca_Costas",
    "36": "Skin_Arma_1M",
    "37": "Skin_Arma_2M",
    "41": "Skin_Escudo",
    "42": "Skin_Corpo",
    "45": "Decoracao_Ilha",
    "47": "Mochila_Sprite",
    "61": "Cartao_Postal",
    "62": "Memorio"
}

def charger_donnees(fichier_json):
    with open(fichier_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def determiner_categorie(item):
    try:
        type_val = int(item.get('type', ''))
    except (ValueError, TypeError):
        return 'inutile', None

    auction_type = item.get('auctionType', '').strip()

# Type 22 !!!
    if type_val == 22:
        if not auction_type or auction_type == '':
            return 'inutile', '22.VAZIO'
        try:
            auction_val = int(auction_type)
            if auction_val in TYPE_22_UTILES:
                return 'utile', f'22.{auction_val}'
            elif auction_val in TYPE_22_INUTILES:
                return 'inutile', f'22.{auction_val}'
            else:
                return 'inutile', f'22.{auction_val}'
        except (ValueError, TypeError):
            return 'inutile', '22.VAZIO'


    if type_val in TYPES_INUTILES:
        return 'inutile', str(type_val)

    if type_val in TYPES_UTILES:
        return 'utile', str(type_val)

    return 'inutile', str(type_val)

def sauvegarder_json(donnees, chemin):
    with open(chemin, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, ensure_ascii=False, indent=2)

def sauvegarder_csv(donnees, chemin):
    if not donnees:
        return

    with open(chemin, 'w', encoding='utf-8', newline='') as f:

        cles = list(donnees[0].keys())
        writer = csv.DictWriter(f, fieldnames=cles)
        writer.writeheader()
        writer.writerows(donnees)

def trier_donnees(fichier_entree):

    dossier_sortie = 'sorted_Scrap'
    os.makedirs(dossier_sortie, exist_ok=True)

    print("Chargement des données...")
    donnees = charger_donnees(fichier_entree)
    print(f"✓ {len(donnees)} items chargés")

    items_inutiles = []
    items_utiles = defaultdict(list)

    print("\nTri des items...")
    for item in donnees:
        categorie, type_key = determiner_categorie(item)

        if categorie == 'inutile':
            items_inutiles.append(item)
        else:
            items_utiles[type_key].append(item)

    print(f"✓ {len(items_inutiles)} items inutiles")
    print(f"✓ {len(items_utiles)} catégories utiles")

    print("\nSauvegarde des items inutiles...")
    backup_json = os.path.join(dossier_sortie, 'Backup-Delete.json')
    backup_csv = os.path.join(dossier_sortie, 'Backup-Delete.csv')
    sauvegarder_json(items_inutiles, backup_json)
    sauvegarder_csv(items_inutiles, backup_csv)
    print(f"✓ Backup-Delete.json ({len(items_inutiles)} items)")
    print(f"✓ Backup-Delete.csv ({len(items_inutiles)} items)")

    print("\nSauvegarde des catégories utiles...")
    for type_key, items in sorted(items_utiles.items()):

        nom_fichier = NOMS_CATEGORIES.get(type_key)
        if not nom_fichier:

            if '.' in str(type_key):
                nom_fichier = f"Type_{type_key.replace('.', '_')}"
            else:
                nom_fichier = f"Type_{type_key}"

        json_path = os.path.join(dossier_sortie, f'{nom_fichier}.json')
        csv_path = os.path.join(dossier_sortie, f'{nom_fichier}.csv')

        sauvegarder_json(items, json_path)
        sauvegarder_csv(items, csv_path)

        print(f"✓ {nom_fichier}.json/.csv ({len(items)} items)")

    print(f"\n Tri terminé ! Tous les fichiers sont dans le dossier '{dossier_sortie}'")

    total_utiles = sum(len(items) for items in items_utiles.values())
    print(f"\n Statistiques:")
    print(f"   • Total items: {len(donnees)}")
    print(f"   • Items utiles: {total_utiles}")
    print(f"   • Items inutiles: {len(items_inutiles)}")
    print(f"   • Catégories créées: {len(items_utiles)}")

if __name__ == "__main__":

    fichier_entree = ''

    try:
        trier_donnees(fichier_entree)
    except FileNotFoundError:
        print(f"❌ Erreur: Le fichier '{fichier_entree}' n'a pas été trouvé.")
        print("   Assure-toi que le fichier existe dans le même dossier que ce script.")
    except json.JSONDecodeError:
        print(f"❌ Erreur: Le fichier '{fichier_entree}' n'est pas un JSON valide.")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")