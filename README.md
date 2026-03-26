# 🛠️ Mini-ETL Produits : Pipeline de Traitement Automatisé et Dashboard Interactif

**Auteur : Nabila ARAB – Master 1 Informatique Big Data – Paris 8**  
Date : Mars 2026

---

## 🚀 Présentation du projet

Ce projet propose un pipeline ETL automatisé pour le traitement de fichiers produits, ainsi qu’un dashboard **interactif** pour explorer, analyser et exporter ces données facilement, sans compétences techniques requises.

### **Objectifs :**
- Automatiser la préparation, le nettoyage, l’agrégation et l’analyse de données produits.
- Fournir une interface **Streamlit** simple d’utilisation pour le filtrage, la visualisation et l’export des résultats.
- Faciliter la prise de décision métier sur les données produits (ex : identification best-sellers, zones de risque...)

---

## 🏗️ Structure du projet

| Dossier/Fichier           | Rôle                                                                |
|---------------------------|---------------------------------------------------------------------|
| `etl/`                    | Scripts de traitement ETL (run.py)                                  |
| `data/`                   | Donn��es brutes à traiter (ex: products.csv)                         |
| `exports/`                | Résultats produits par le pipeline ETL (clean_data.csv, prix, kpis…) |
| `dashboard.py`            | Script principal du dashboard Streamlit                             |
| `requirements.txt`        | Dépendances Python à installer                                      |
| `README.md`               | Documentation du projet…                                            |

---

## 🛠️ Technologies et librairies utilisées

- **Python 3.8+**
- **Pandas**, **DuckDB** : traitement de données
- **Streamlit** : dashboard interactif (web)
- **Matplotlib** : graphiques et visualisations
- **Pdfkit**/**wkhtmltopdf** : génération d’exports PDF
- **Jupyter Notebook** : exploration initiale & validation

---

## ⚡️ Installation et démarrage

1. **Cloner le projet** :
    ```bash
    git clone https://github.com/Nabila-arab/mini-etl-dashboard.git
    cd mini-etl-dashboard
    ```

2. **Créer et activer un environnement virtuel** :
    ```bash
    python -m venv .venv
    source .venv/bin/activate    # Sur Mac/Linux
    .venv\Scripts\activate       # Sur Windows
    ```

3. **Installer les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```

4. **Lancer le pipeline ETL** (à adapter selon ton script !):
    ```bash
    python etl/run.py
    ```
    ➔ Les fichiers propres sont alors générés dans le dossier `exports/`.

5. **Lancer le dashboard** :
    ```bash
    streamlit run dashboard.py
    ```
    ➔ L’interface s’ouvre dans votre navigateur.

---

## 🖥️ Fonctionnalités du dashboard

- **Recherche et filtrage dynamiques** : par nom, catégorie, intervalle de prix, etc.
- **Visualisation des indicateurs clés** : prix total, marge, top produits, etc.
- **Graphiques interactifs** : bar chart, pie chart, etc.
- **Export des résultats** : CSV, Excel, PDF personnalisés
- **Alertes et analyses intelligentes** : détection automatiques de cas métier (catégorie dominante, marges faibles, etc.)
- **Téléchargement rapide de tous les résultats, y compris les rapports PDF/Excel**

---

## 📑 Exemple de workflow type

1. **Lancer le pipeline ETL pour traiter les nouveaux fichiers**
2. **Démarrer le dashboard**
3. **Appliquer les filtres voulus dans la sidebar**
4. **Analyser les KPIs, tableaux et graphiques**
5. **Exporter les résultats en un clic au format souhaité**

---

## 📝 Astuces et conseils d’utilisation

- Si le dashboard affiche une erreur “Fichier non trouvé”, pensez à relancer le pipeline ETL (étape 4).
- Le bouton “Télécharger PDF” nécessite que `wkhtmltopdf` soit installé sur votre PC.
- Le projet peut facilement être adapté à d’autres jeux de données (ventes, stocks…), ou déployé sur le cloud (Streamlit Cloud, Heroku, etc.)

---

## 🧑‍💻 Auteur / Contact

- **Nabila ARAB**
- Email : _[Ajoute ton email étudiant si tu veux]_
- Université Paris 8 – Master Informatique Big Data

---

## 🏆 Bonus

Scannez le QR code ci-dessous ou cliquez ici pour explorer le code source !  
[https://github.com/Nabila-arab/mini-etl-dashboard](https://github.com/Nabila-arab/mini-etl-dashboard)

---

## 📜 Licence

Projet académique – Usage non commercial
