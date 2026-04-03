# 🛠️ Mini-ETL Produits — Pipeline Automatisé & Dashboard Interactif

**Auteur : Nabila ARAB — Master 1 Informatique Big Data — Paris 8**  
Date : Avril 2026

---

## 🚀 Présentation

Ce projet met à disposition une solution tout-en-un pour :
- Nettoyer, agréger et analyser des données produits automatiquement (via scripts Python ETL)
- Visualiser/interroger/explorer ces données dans un dashboard web interactif (Streamlit)
- Exposer les résultats via une API simple (Flask)
- Proposer un déploiement cloud sans installation complexe (Railway)

---

## 🏗️ Structure du projet

```
.
├── api/               # API Flask
│   └── app.py
├── data/              # Jeux de données bruts à traiter
│   └── products.csv
├── duckdb/            # Base DuckDB persistée
│   └── pipeline.duckdb
├── etl/               # Scripts ETL (préparation et agrégation)
│   └── run.py
├── exports/           # Résultats produits par le pipeline ETL
│   ├── clean_data.csv
│   ├── prix_par_categorie.csv
│   ├── prix_par_produit.csv
│   ├── indicateurs.csv
│   └── produits_chers.csv
├── streamlit_app.py   # Dashboard Streamlit (interface principale)
├── requirements.txt   # Dépendances Python
├── Procfile           # (si déploiement cloud/Railway)
├── README.md
```

---

## ⚡️ Installation & prise en main rapide

### 1. **Cloner le projet**
```bash
git clone https://github.com/Nabila-arab/mini-etl-dashboard.git
cd mini-etl-dashboard
```

### 2. **Créer et activer un environnement virtuel**
```bash
python -m venv .venv
# Sous Windows :
.venv\Scripts\activate
# Sous Mac/Linux :
source .venv/bin/activate
```

### 3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

### 4. **Lancer le pipeline ETL**
(Traite le CSV de `data/`, génère les fichiers nettoyés dans `exports/`, met à jour la base DuckDB)
```bash
python etl/run.py
```

Les fichiers résultats (`clean_data.csv`, `prix_par_produit.csv`, etc.) sont créés/écrasés dans `exports/`.

### 5. **Lancer le dashboard interactif**
```bash
streamlit run streamlit_app.py
```
Ouvre automatiquement le dashboard dans le navigateur (interface web).

---

## 🖥️ Fonctionnement du dashboard

- Recherchez/filtrez/visualisez vos produits (par nom, catégorie, prix, etc.).
- Consultez les indicateurs clés (total CA, marge, nombre de produits...).
- Affichez graphiques dynamiques (tops produits, répartition catégorie...).
- Exportez à tout moment les données filtrées (CSV ou Excel).
- Téléchargez rapidement les résultats (produits chers, etc.).
- Si besoin, vous pouvez **importer un autre CSV** depuis la barre latérale.

---

## 🌐 Tester en ligne (Railway / déploiement cloud)


Accédez directement à la version cloud ici :  
👉 https://mini-etl-dashboard-production-e19a.up.railway.app/  
Ou scannez le QR Code 

_Note : pour tester en local, suivez simplement les étapes ci-dessus._

---

## 🏷️ API (endpoints principaux)

- `GET /indicateurs` : KPIs globaux du catalogue  
- `GET /clean_data`   : Jeu de données nettoyé
- `GET /prix_par_produit` : Agrégation CA par produit
- `GET /produits_chers?seuil=500` : Filtre produits chers (> 500€ par défaut)  

Pour démarrer l’API seul :
```bash
python api/app.py
```
Modifier l’URL si besoin dans votre code.

---

## 📦 Exemples fournis

- **Jeu de test** (`data/products.csv`) : catalogue produit fictif
- **Notebooks d’analyse** : visualisation des résultats générés (facultatif)

---

## ❓ Problèmes fréquents / FAQ

- **Erreur “Fichier non trouvé” sur le dashboard** :  
  → Relancez le pipeline ETL (`python etl/run.py`) pour regénérer les exports.

- **Problème de dépendance (duckdb, pyarrow, etc.)** :  
  → Vérifiez que l’environnement virtuel est bien activé avant l’installation.

- **Port déjà utilisé avec Streamlit** :  
  → Fermez l’instance précédente ou changez le port (`streamlit run streamlit_app.py --server.port 8502`).

---

## ✉️ Contact

- Auteur : Nabila ARAB

---

## 📜 Licence

Projet académique — Usage pédagogique

---

## 💡 Améliorations possibles (prochaines versions)

- API multi-user et authentification
- Imports multi-formats (Excel, API, SQL…)
- Dashboard collaboratif / exports PDF automatiques
- Intégration prédiction (Machine Learning) / analyse intelligente

---

\_Dernière mise à jour : avril 2026\_