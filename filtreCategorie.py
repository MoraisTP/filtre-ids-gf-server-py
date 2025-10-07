import os
import re
import sys
from collections import defaultdict

# Le filtre fonctionne mais vu la quantité d'ids et leurs "titre/description" foireuses, certains ID's seront mal placé (Exemple : Les skins de dos comme "Livro/Sachê/Chama Shuriken" sont trop génériques et seront forcément placés dans dDivers). Vu que c'est un script simple, c'est surtout pour faciliter le triage d'ids rapidement. Je l'améliorerai par la suite si j'ai du temps, j'ai pour projet de créer une gestion d'alchimie avec une belle interface et c'est pour ça que j'ai réalisé ce filtre, un besoin spécifique pour l'autre projet. Vous pouvez trouver tous les IDs dans Data/Translate et si vous arrivez pas, contactez moi sur Discord. :)


# Valeur par défaut
fichier_par_defaut = "IDs_GF_Sorted.txt"

fichier_source = input(f"Quel est le nom de votre fichier ? (Par défaut '{fichier_par_defaut}') : ").strip()

# Utiliser le fichier par défaut.
if not fichier_source:
    fichier_source = fichier_par_defaut

if not fichier_source.endswith(".txt"):
    print("Erreur : Le fichier doit être au format .txt")
    sys.exit(1)

if not os.path.exists(fichier_source):
    print(f"Le fichier '{fichier_source}' est introuvable.")
    sys.exit(1)

output_dir = "sorted_categories"
os.makedirs(output_dir, exist_ok=True)

# Catégories [Vous pouvez le modifier en suivant la même logique "Votre catégorie","Votre deuxième catégorie"...
categories = {
    "Fantasias": {
        "keywords": ["Vestido", "Terno", "Armadura", "Roupa", "Roupas", "Roupao", "Camiseta", "Uniforme", "Traje",
                     "Fantasia", "Costume", "Cabelo", "Pente", "Flor", "Laço", "Arco",
                     "Outfit", "Espada", "Rabo", "Rabos", "Machado", "Escudo", "Criada", "General", "Quimono",
                     "Cheongsam", "Suspensorio", "Saia", "Biquini", "Smoking", "Vestuario", "Cueca", "Calçao",
                     "Calçoes", "Shorts", "Hakama", "Mini-saia", "Veste", "Vestes", "Capa", "Costa", "Costas", "Asa",
                     "Asas", "Mochila", "Espadas", "Lamina", "Piao", "Koala", "Tambor", "Canhao", "Batida", "Capacete",
                     "Adereço", "Chapeu", "Orelha", "Orelhas", "Cocar", "Oculos", "Cabelos", "Mascara", "Mancha",
                     "Cabeça", "Cobertura", "Roda", "Penteado", "Icone", "Laços","Aureola","Batedeira","Leque","Colher","Espadao","Cruz","Clava","Maleta","Garfo","Vela","Cajado","Sabre","Vara","Varinha","Buque","Espetinho","Alabarda"],
        "description": "Costumes Tête/Corps/Dos/2M et 1M"
    },
    "Montaria": {
        "keywords": ["Montaria", "Mount", "Cavalo", "Animal", "Veículo"],
    },
    "Moveis": {
        "keywords": ["Trono"]
    },
    "Sprites": {
        "keywords": ["Sprite"],
        "description": "Costumes et divers sprites."
    },
    "Nucleos": {
        "keywords": ["Nucleo", "Núcleo", "Nucleos", "Núcleos", "Nucleo", "N�cleo"],
        "description": "Nucléus de Force/Vit/Agi etc."
    },
    "Containers": {
        "keywords": ["Caixa", "Box", "Container", "Baú", "Chest", "Inventário"],
        "description": "Conteneurs,Packs etc"
    }
}


# NE PAS TOUCHER A CETTE PARTIE, RISQUE DE CASSE.
def normaliser_regex(texte: str) -> str:
    texte = texte.lower()
    texte = re.sub(r'[àáâãäå]', 'a', texte)
    texte = re.sub(r'[èéêë]', 'e', texte)
    texte = re.sub(r'[ìíîï]', 'i', texte)
    texte = re.sub(r'[òóôõö]', 'o', texte)
    texte = re.sub(r'[ùúûü]', 'u', texte)
    texte = re.sub(r'[ç]', 'c', texte)
    texte = re.sub(r'[�]', '.', texte)
    return texte

# NE PAS TOUCHER A CETTE PARTIE, Ordre de priorité du filtre. Montaria > Armas > Fantasias etc.
ordre_priorite = ["Montaria", "Armas", "Fantasias", "Sprites", "Divers"]


# Extraction du premier | |, on évite les descriptions pour éviter des confusions et casser le filtre.
def categoriser_ligne(ligne, categories):

    parties = ligne.split('|')
    if len(parties) >= 2:
        nom_item = parties[1]
    else:
        nom_item = ligne

    nom_normalise = normaliser_regex(nom_item)

    for categorie, config in categories.items():
        for keyword in config["keywords"]:
            keyword_normalise = normaliser_regex(keyword)
            if re.search(r'\b' + re.escape(keyword_normalise) + r'\b', nom_normalise):
                return categorie
    return "Divers"


# Partie AFFICHAGE
def analyser_statistiques(categorized_lines):
    print("\n✨ Statistiques du tri ✨")
    print("===================================")
    total_lignes = sum(len(lignes) for lignes in categorized_lines.values())

    for categorie, lignes in sorted(categorized_lines.items(), key=lambda x: len(x[1]), reverse=True):
        pourcentage = (len(lignes) / total_lignes) * 100 if total_lignes > 0 else 0
        print(f"{categorie}: {len(lignes)} lignes ({pourcentage:.1f}%)")

    print(f"\nTotal: {total_lignes} lignes triées")


# Cœur
def main():
    try:
        with open(fichier_source, 'r', encoding='utf-8') as file:
            lignes_filtrees = file.readlines()
    except FileNotFoundError:
        print(f"Erreur : le fichier '{fichier_source}' est introuvable.")
        return
    except Exception as e:
        print(f"Erreur lors de la lecture : {e}")
        return

    categorized_lines = defaultdict(list)
    for category in categories.keys():
        categorized_lines[category]
    categorized_lines["Divers"] = []

    for line in lignes_filtrees:
        categorie = categoriser_ligne(line, categories)
        categorized_lines[categorie].append(line)

# Save
    fichiers_crees = 0
    for category, lines in categorized_lines.items():
        if lines:
            file_path = os.path.join(output_dir, f'IDS_GF_{category.lower()}.txt')
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.writelines(lines)
                print(f"Fichier créé : {file_path} ({len(lines)} lignes)")
                fichiers_crees += 1
            except Exception as e:
                print(f"Erreur lors de la sauvegarde de {file_path}: {e}")

    # Résultats
    analyser_statistiques(categorized_lines)
    print(f"Tri terminé : {sum(len(v) for v in categorized_lines.values())} lignes traitées, {fichiers_crees} fichiers créés.")


if __name__ == "__main__":
    main()