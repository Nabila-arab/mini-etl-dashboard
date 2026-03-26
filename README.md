# Mini-ETL Automatisé - Analyse de Données Produits

## Présentation générale
Ce projet est un pipeline automatisé pour l’analyse de jeux de données produits (CSV), composé de :
- Un script ETL Python pour nettoyage/agrégation/exports
- Un notebook de visualisation pour l’analyse graphique
- Une API Flask pour exposer les résultats

---

## 1. Fonctionnement global

1. **Dataset brut**  
   - Ex : `data/products.csv` (données produits Kaggle)
2. **Pipeline ETL (`etl/run.py`)**
   - Nettoie les données (doublons, valeurs manquantes, etc.)
   - Agrège prix par produit et par catégorie
   - Calcule les indicateurs clés (prix total, marge totale, nb de produits)
   - Génère les exports dans le dossier `exports/`
3. **Visualisation**
   - Le notebook Jupyter utilise les exports pour produire des graphes interactifs et lister des KPIs
4. **API Flask**
   - Sert dynamiquement les fichiers exportés et résultats sur une interface web (`http://127.0.0.1:5000`)

---

## 2. Structure des dossiers

```
Mini_etl/
│
├── data/
│     └── products.csv              # Jeux de données source (Kaggle)
│
├── etl/
│     └── run.py                    # ETL principal
│
├── exports/                        # Exports générés automatiquement
│     └── clean_data.csv
│     └── prix_par_produit.csv
│     └── prix_par_categorie.csv
│     └── indicateurs.csv
│
├── api/
│     └── app.py                    # API Flask (option)
│
├── visualisation.ipynb             # Notebook principal pour analyse & graphes
└── README.md
```

---

## 3. Exécution - Mode d’emploi

### ● **1. Lancer le pipeline**  
```bash
python etl/run.py
```

### ● **2. Visualiser les résultats**
Ouvrir `visualisation.ipynb` et exécuter toutes les cellules :
- Affichage KPIs
- Tableau nettoyé
- Graphiques Top produits, catégories, produits chers

### ● **3. Lancer l’API Flask**
```bash
python api/app.py
```
Consulter sur : [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 4. Adaptabilité & réutilisation

- Il suffit de remplacer le fichier `data/products.csv` par n’importe quel dataset compatible et de relancer le pipeline pour tout recalculer.
- Changez un paramètre (exemple : seuil du prix “produit cher”) dans l’ETL pour obtenir une nouvelle analyse automatiquement.

---

## 5. KPIs/Exports (Exemple)

| kpi          | valeur   |
|--------------|----------|
| prix_total   | 143562   |
| nb_produits  | 1197     |
| marge_totale | 50643    |

---

## 6. Graphiques Principaux (screens à insérer)
- **Top 10 produits par chiffre d’affaires**
- **Répartition prix par catégorie**
- **Table des produits “chers”**

---

## 7. Conclusion

- Pipeline automatisé, clé-en-main, adapté à tout nouveau jeu de données
- Visualisations dynamiques faciles à enrichir
- API prête pour l’intégration avec d’autres applications (frontend, plateforme web, etc.)