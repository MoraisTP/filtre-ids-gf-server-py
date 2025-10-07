import re
import os
import sys
#

# La V1 du script est à passer en premier lieu pour avoir un résultat plus propre (Sur un fichier de 50k, on passe à 15k lignes). Il éliminera les items ids contenant des versions limités (1-30 jours) puis en deuxième supprimera toutes les $35$ qui n'ont pas d'ID. utilisez le V2 pour "trier" selon les catégories.
# Le code est documenté pour faciliter la compréhension de ceux qui ne connaissent pas Python.

# À LIRE OBLIGATOIREMENT |Placez le fichier avec les ID's dans le dossier ! |
nom_fichier = input("Quel est le fichier que vous voulez traiter ? (format .txt obligatoire) : ").strip()
backup_fichier = "backup.txt"
# NE PAS TOUCHER !
if not nom_fichier.endswith(".txt"):
    print("Erreur : lLe fichier doit être au format .txt !")
    exit(1)

if not os.path.exists(nom_fichier):
    print(f"Erreur : le fichier '{nom_fichier}' n'existe pas dans ce dossier.")
    exit(1)

nouveau_fichier = input(
    "Quel nom voulez-vous donner au fichier de sortie ? (ou laissez vide pour 'IDs_GF_Sorted.txt') : ").strip()
if nouveau_fichier == "":
    nouveau_fichier = "IDs_GF_Sorted.txt"
elif not nouveau_fichier.endswith(".txt"):
    nouveau_fichier += ".txt"

# REGEX, vous pouvez le modifier pour être plus précis dans les lignes à supprimer.
patterns_a_supprimer = [
    r"vers[aã]o limitada",  # versão limitada / versao limitada
    r"\(\s*\d{1,2}\s*dias?\s*\)",  # (3 dias), (30 dias), (7 dia)
    r"\d{1,2}\s*dias?\s*\)",  # 3 dias )
    r"vers[aã]o limitada\s*de\s*\d{1,2}\s*dias?"  # versão limitada de 3 dias
]

# Permet de normaliser le texte pour avoir un meilleur résultat
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


# Partie Gestion
def ligne_contient_pattern(ligne: str) -> bool:
    ligne_normalisee = normaliser_regex(ligne)
    return any(re.search(pattern, ligne_normalisee) for pattern in patterns_a_supprimer)

# Cœur du script, on lit le fichier de l'user et on vérifie si c'est un .txt.
def charger_lignes(fichier: str) -> list[str]:
    try:
        with open(fichier, "r", encoding="utf-8") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Erreur : le fichier '{fichier}' est introuvable. Veuillez importer un fichier valide (.txt).")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur lors de la lecture de '{fichier}' : {e}")
        sys.exit(1)
def filtrer_lignes(lignes: list[str]) -> tuple[list[str], list[str]]:
#  Je retourne deux lignes, celles qu'on veut conserver et celles qui partent à la poubelle (backup.txt)
    lignes_filtrees = []
    lignes_supprimees = []
# Puis on supprime les $
    for ligne in lignes:
        if ligne.strip().startswith("$"):
            lignes_supprimees.append(ligne)
            continue

# et aussi les lignes supprimées
        if ligne_contient_pattern(ligne):
            lignes_supprimees.append(ligne)
        else:
            lignes_filtrees.append(ligne)

    return lignes_filtrees, lignes_supprimees

# Save + Backup
def sauvegarder_resultats(lignes_filtrees: list[str], lignes_supprimees: list[str]):
    try:
        with open(nouveau_fichier, "w", encoding="utf-8") as file:
            file.writelines(lignes_filtrees)

        with open(backup_fichier, "w", encoding="utf-8") as file:
            file.writelines(lignes_supprimees)
    except Exception as e:
        print(f" Erreur lors de la sauvegarde : {e}")
        sys.exit(1)

# Affichage

def afficher_resume(lignes: list[str], filtrees: list[str], supprimees: list[str]):

    print("\n✨ Nettoyage terminé avec succès ✨")
    print("===================================")
    print(f"Fichier source       : {nom_fichier}")
    print(f"Lignes originales    : {len(lignes)}")
    print(f"Lignes conservées    : {len(filtrees)}")
    print(f"Lignes supprimées    : {len(supprimees)}")
    print(f"Fichier filtré       : {nouveau_fichier}")
    print(f"Backup supprimées    : {backup_fichier}")

    if supprimees:
        print("\nAperçu des lignes supprimées :")
        for i, ligne in enumerate(supprimees[:5]):
            print(f"  {i + 1}. {ligne.strip()}")
        if len(supprimees) > 5:
            print("  ...")


# Main

def main():
    lignes = charger_lignes(nom_fichier)
    lignes_filtrees, lignes_supprimees = filtrer_lignes(lignes)
    sauvegarder_resultats(lignes_filtrees, lignes_supprimees)
    afficher_resume(lignes, lignes_filtrees, lignes_supprimees)


if __name__ == "__main__":
    main()