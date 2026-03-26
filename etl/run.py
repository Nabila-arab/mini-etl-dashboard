import pandas as pd
import duckdb

# 1. Charger le nouveau dataset
df = pd.read_csv('data/products.csv')

print("Aperçu du CSV original :")
print(df.info())
print(df.head())

# 2. Nettoyage de base : doublons, valeurs manquantes & assez stricte
print("\nNettoyage : suppression doublons et valeurs manquantes...")
lignes_avant = len(df)
df = df.drop_duplicates()
df = df.dropna(subset=['product_id', 'name', 'price_usd'])
df = df[df['price_usd'] > 0]
df['name'] = df['name'].str.title().str.strip()  # Standardisation du nom du produit
lignes_apres = len(df)
print(f"Lignes avant : {lignes_avant}, après nettoyage : {lignes_apres}")

print("\nAperçu des données nettoyées :")
print(df.info())
print(df.head())

# 3. Agrégation : prix total par produit  
prix_par_produit = df.groupby('name', as_index=False)['price_usd'].sum()
prix_par_produit.to_csv('exports/prix_par_produit.csv', index=False)
print("\nPrix total par produit : ")
print(prix_par_produit.head())

# 4. Agrégation : prix total par catégorie
prix_par_categorie = df.groupby('category', as_index=False)['price_usd'].sum()
prix_par_categorie.to_csv('exports/prix_par_categorie.csv', index=False)
print("\nPrix total par catégorie : ")
print(prix_par_categorie.head())

# 5. Indicateurs/KPI (prix total, nb produits, marge totale)
kpi_data = {
    'kpi': ['prix_total', 'nb_produits', 'marge_totale'],
    'valeur': [df['price_usd'].sum(), df['product_id'].nunique(), df['margin_usd'].sum()]
}
kpi_df = pd.DataFrame(kpi_data)
kpi_df.to_csv('exports/indicateurs.csv', index=False)
print("\nIndicateurs créés : ")
print(kpi_df)

# 6. Export du jeu nettoyé (clean_data)
df.to_csv('exports/clean_data.csv', index=False)


# Connexion à la base DuckDB
con = duckdb.connect("duckdb/pipeline.duckdb")

# Met à jour ou crée les tables DuckDB à partir des DataFrames pandas
con.execute("CREATE OR REPLACE TABLE clean_data AS SELECT * FROM df")
con.execute("CREATE OR REPLACE TABLE prix_par_produit AS SELECT * FROM prix_par_produit")
con.execute("CREATE OR REPLACE TABLE prix_par_categorie AS SELECT * FROM prix_par_categorie")
con.execute("CREATE OR REPLACE TABLE indicateurs AS SELECT * FROM kpi_df")

con.close()
print("\nTables DuckDB mises à jour avec le nouveau dataset.")