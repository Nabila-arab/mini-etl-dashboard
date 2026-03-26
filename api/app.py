from flask import Flask, jsonify, request
import duckdb

# Initialisation de l'application Flask
app = Flask(__name__)

# Route d'accueil, indiquer à l'utilisateur les endpoints disponibles
@app.route("/")
def accueil():
    return "API du mini-ETL : utilise /indicateurs, /clean_data ou /prix_par_produit"

# Endpoint pour retourner les indicateurs (KPI globaux)
@app.route("/indicateurs")
def indicateurs():
    con = duckdb.connect("duckdb/pipeline.duckdb")
    df = con.execute("SELECT * FROM indicateurs").fetchdf()
    con.close()
    # Conversion du DataFrame en JSON pour l'API
    return jsonify(df.to_dict(orient="records"))

# Endpoint pour retourner le jeu de données nettoyé
@app.route("/clean_data")
def clean_data():
    con = duckdb.connect("duckdb/pipeline.duckdb")
    df = con.execute("SELECT * FROM clean_data").fetchdf()
    con.close()
    return jsonify(df.to_dict(orient="records"))

# Endpoint pour retourner le prix total par produit agrégé
@app.route("/prix_par_produit")
def prix_par_produit():
    con = duckdb.connect("duckdb/pipeline.duckdb")
    df = con.execute("SELECT * FROM prix_par_produit").fetchdf()
    con.close()
    return jsonify(df.to_dict(orient="records"))

@app.route("/produits_chers")
def produits_chers():
    seuil = float(request.args.get("seuil", 500))  # Par défaut 500 si rien n’est spécifié
    con = duckdb.connect("duckdb/pipeline.duckdb")
    df = con.execute("SELECT * FROM clean_data WHERE price_usd > ?", [seuil]).fetchdf()
    con.close()
    return jsonify(df.to_dict(orient="records"))

# Lancement en mode debug si exécuté en script principal
if __name__ == "__main__":
    app.run(debug=True)