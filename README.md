# 🎮 Filtre d'IDs Grand Fantasia 

## 📋 Description

Ce projet contient deux scripts Python pour filtrer et organiser les IDs du jeu Grand Fantasia. Ils permettent de nettoyer et catégoriser automatiquement les données pour faciliter la gestion des items. Pour trouver les fichiers aves les ID's rendez-vous sur -> 

```
/root/gf-server/Data/Translate
```

Je conseille : Itemmall.ini |
Il contient la majorité des IDs intéressants.

## 🚀 Installation

### Prérequis
- Python 3+
- Fichier avec les IDs

### Structure des fichiers
```
📁 VotreDossier/
├── 🔧 filtreLimite.py      (Script de nettoyage - Étape 1)
├── 🔧 filtreCategorie.py   (Script de tri - Étape 2)
└── 📄 VotreFichierIDs.txt  (Vos données source)
```

## 📖 Utilisation

### Étape 1 : Nettoyage avec `filtreLimite.py`

**Objectif** : Supprimer les items indésirables (versions limitées, lignes corrompues/inutiles)

1. Lancez le script :
   ```bash
   python filtreLimite.py
   ```

2. Suivez les prompts :
    - ✅ **Fichier source** : Entrez le nom de votre fichier d'IDs (format .txt obligatoire)
    - ✅ **Fichier de sortie** : Nommez le résultat ou laissez vide pour `IDs_GF_Sorted.txt`

**Ce que fait le script** :
- ❌ Supprime les versions limitées (1-30 jours)
- ❌ Supprime les lignes corrompues commençant par `$`
- ✅ Crée un fichier de backup `backup.txt` avec les éléments supprimés
- ✅ Génère un rapport détaillé du nettoyage

**Résultat** : Un fichier de base qui dépasse 50k de lignes, qui se retrouve avec seulement 15k de lignes, nettoyé et prêt pour l'étape 2 !

---

### Étape 2 : Tri avec `filtreCategorie.py`

**Objectif** : Organiser les items par catégories

1. Lancez le script :
   ```bash
   python filtreCategorie.py
   ```

2. Suivez les prompts :
    - ✅ **Fichier source** : Entrez `IDs_GF_Sorted.txt` (Valeur par défaut) ou votre fichier nettoyé

**Ce que fait le script** :
- 📂 Crée un dossier `sorted_categories/`
- 🏷️ Trie les items dans 6 catégories principales :
    - **Fantasias** : Costumes (tête/corps/dos)
    - **Montaria** : Montures et véhicules
    - **Moveis** : Mobilier
    - **Sprites** : Effets visuels
    - **Nucleos** : Nucléus de statistiques
    - **Containers** : Conteneurs et packs
    - **Divers** : Items non classés

**Résultat** : Des fichiers organisés dans le dossier `sorted_categories/` !

## 🎯 Catégories Disponibles

### Fantasias
*Costumes et accessoires*
- ✅ Têtes, corps, dos
- ✅ Armes
- ✅ Accessoires (ailes, chapeaux, etc.)
- ✅ Uniformes et tenues spéciales

### Montaria
*Transport*
- ✅ Montures animales
- ✅ Véhicules

### Autres Catégories
- 🪑 **Moveis** : Mobilier de décoration
- ✨ **Sprites** : Effets visuels et particules
- 💎 **Nucleos** : Boosters de statistiques
- 📦 **Containers** : Boîtes et inventaires

## ⚙️ Personnalisation

### Modifier les catégories
Si vous connaissez un minimum, vous pouvez personalize le filtre à vos besoins.
Éditez le dictionnaire `categories` dans `filtreCategorie.py` :

```
"MaNouvelleCategorie": {
    "keywords": ["mot1", "mot2", "mot3"],
    "description": "Description optionnelle"
}
```

### Modifier les filtres de nettoyage
Éditez `patterns_a_supprimer` dans `filtreLimite.py` pour ajouter/supprimer des motifs.

## 📊 Exemple de Résultat

```
📁 sorted_categories/
├── 📄 ids_gf_fantasias.txt    (1,200 items)
├── 📄 ids_gf_montaria.txt     (150 items)
├── 📄 ids_gf_sprites.txt      (80 items)
├── 📄 ids_gf_nucleos.txt      (200 items)
├── 📄 ids_gf_containers.txt   (75 items)
└── 📄 ids_gf_divers.txt       (50 items)
```

## 🆘 Dépannage

### Erreurs Courantes
- ❌ **"Fichier introuvable"** : Vérifiez le nom et l'emplacement du fichier
- ❌ **Format .txt requis** : Assurez-vous que vos fichiers sont en .txt
- ❌ **Encodage** : Les scripts utilisent l'encodage UTF-8

### Performance
- ⚡ Sur 50,000 lignes : Réduction à ~15,000 lignes après nettoyage
- ⚡ Tri rapide grâce aux algorithmes optimisés

## 📝 Notes

- 🔍 **Précision** : Le tri est basé sur les mots-clés dans les noms d'items
- 📈 **Améliorations** : Certains items génériques peuvent aller dans "Divers"
- 💡 **Projet futur** : Interface graphique pour la gestion d'alchimie

## 🤝 Support

Problèmes ou questions ? Contactez-moi sur Discord !

---
