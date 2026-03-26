import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pdfkit
import io
import os

st.set_page_config(page_title="Mini-ETL Dashboard", layout="wide")

# ---- Chargement des données ----
try:
    df = pd.read_csv("exports/clean_data.csv")
    prix_par_produit = pd.read_csv("exports/prix_par_produit.csv")
    prix_par_categorie = pd.read_csv("exports/prix_par_categorie.csv")
    kpi = pd.read_csv("exports/indicateurs.csv")
except Exception as e:
    st.error("Erreur lors du chargement des fichiers. Lance d'abord le pipeline ETL !")
    st.stop()

# ---- Sidebar - Filtres ----
st.sidebar.title("🔎 Filtres")

# Recherche texte produit/catégorie
search = st.sidebar.text_input("🔤 Recherche (nom ou catégorie)", "")
df_filtré = df[
    df["name"].str.contains(search, case=False, na=False) |
    df["category"].str.contains(search, case=False, na=False)
] if search else df

# Multi-filtre catégorie
categories = st.sidebar.multiselect(
    "🗂️ Filtrer par catégorie",
    options=df["category"].unique(),
    default=list(df["category"].unique())
)

if len(categories) == 0:
    st.warning("⚠️ Veuillez sélectionner au moins une catégorie.")
    st.stop()
else:
    df_filtré = df_filtré[df_filtré["category"].isin(categories)]

# --- Bloc sécurisé pour min/max prix (gestion NaN si filtre vide) ---
if not df_filtré.empty and df_filtré["price_usd"].dropna().size > 0:
    min_price_val = df_filtré["price_usd"].min()
    max_price_val = df_filtré["price_usd"].max()
    min_price = int(min_price_val) if not pd.isna(min_price_val) else 0
    max_price = int(max_price_val) if not pd.isna(max_price_val) else 1
else:
    min_price = 0
    max_price = 1

seuil = st.sidebar.slider(
    "💵 Seuil prix ($, filtre produits chers)", 
    min_value=min_price,
    max_value=max_price if max_price > min_price else min_price + 1,
    value=min(500, max_price if max_price > min_price else min_price + 1)
)
df_cher = df_filtré[df_filtré["price_usd"] > seuil]

# Téléchargement du tableau filtré général (recherche/catégorie uniquement)
csv_filtre = df_filtré.to_csv(index=False).encode()
st.sidebar.download_button(
    label="⬇️ Télécharger produits filtrés (CSV)",
    data=csv_filtre,
    file_name="produits_filtres.csv",
    mime="text/csv"
)

# Téléchargement du tableau "produits chers"
csv_chers = df_cher.to_csv(index=False).encode()
st.sidebar.download_button(
    label="⬇️ Télécharger produits chers (CSV)",
    data=csv_chers,
    file_name="produits_chers.csv",
    mime="text/csv"
)

# --- Bouton d'export Excel ---
excel_bytes = io.BytesIO()
df_filtré.to_excel(excel_bytes, index=False, engine='openpyxl')
excel_bytes.seek(0)
st.sidebar.download_button(
    label="⬇️ Télécharger produits filtrés (Excel)",
    data=excel_bytes,
    file_name="produits_filtres.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# --- Bouton d'export PDF ---
html_rapport = f"""
<h1 style='color:#1f77b4;'>Rapport Produits Filtres</h1>
<h2>Resume</h2>
<ul>
  <li>Nombre de produits: {df_filtré.shape[0]}</li>
  <li>Prix moyen: {df_filtré['price_usd'].mean():.2f} $</li>
  <li>Marge moyenne: {df_filtré['margin_usd'].mean():.2f} $</li>
</ul>
<h2>Top 10 produits</h2>
{df_filtré.sort_values('price_usd', ascending=False).head(10).to_html(index=False)}
"""

try:
    pdfkit_config = None
    if os.name == "nt":  # Seulement sur Windows local avec wkhtmltopdf installé
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    pdf_bytes = pdfkit.from_string(html_rapport, False, configuration=pdfkit_config)
    st.sidebar.download_button(
        label="⬇️ Télécharger le rapport filtré (PDF)",
        data=pdf_bytes,
        file_name="rapport_filtre.pdf",
        mime="application/pdf"
    )
except Exception as e:
    st.sidebar.warning("⚠️ Export PDF impossible ici (wkhtmltopdf non disponible). Export Excel/CSV : OK.")

st.sidebar.markdown("---")
st.sidebar.markdown("**Réalisé par : Nabila ARAB**")
# st.sidebar.image("logo.png", width=100)

# ---- Indicateurs clés (KPI) ----
st.title("📊 Dashboard Mini-ETL Produits")
st.markdown(
    """
    > **ℹ️ Mode d'emploi** :  
    > 1. Utilisez les filtres à gauche pour explorer les données produits.
    > 2. Visualisez et analysez les KPIs et graphiques générés automatiquement.
    > 3. Cliquez sur l'un des boutons d'export pour récupérer les résultats sous format CSV, Excel ou PDF.
    """
)
col1, col2, col3 = st.columns(3)
col1.metric("💰 Prix total", f"{df['price_usd'].sum():,.2f} $")
col2.metric("📦 Nombre de produits", int(df['product_id'].nunique()))
col3.metric("📈 Marge totale", f"{df['margin_usd'].sum():,.2f} $")

top_prod = prix_par_produit.sort_values("price_usd", ascending=False).iloc[0]
st.info(f"**Top produit (CA)** : {top_prod['name']} ({top_prod['price_usd']}$)")

st.markdown("---")

# ---- Tableau stylé des produits filtrés ----
st.header("📝 Tableau des produits (filtres)")
st.dataframe(
    df_filtré.style.background_gradient(subset=["margin_usd"], cmap="Greens"),
    use_container_width=True
)

# ---- Produits chers ----
st.header(f"🔥 Produits dont le prix > {seuil} $")
if not df_cher.empty:
    st.dataframe(df_cher)
else:
    st.warning("Aucun produit ne correspond à ce filtre dans la sélection courante.")

# ---- Visualisation : Top N produits (CA) ----
st.header("🏆 Produits stars par chiffre d'affaires")
n = st.slider("Nombre de TOP produits à afficher", min_value=3, max_value=20, value=10)
topN = prix_par_produit.sort_values("price_usd", ascending=False).head(n)
fig1, ax1 = plt.subplots(figsize=(max(6, n/2), 4))
bars = ax1.bar(topN["name"], topN["price_usd"], color="skyblue")
plt.xticks(rotation=30, ha="right", fontsize=10)
plt.ylabel("CA ($)")
plt.title(f"Top {n} produits")
ax1.bar_label(bars, fmt="%.0f", padding=2, fontsize=8)
st.pyplot(fig1)

# ---- Visualisation : Répartition CA par catégorie ----
st.header("📈 Répartition du CA par catégorie")
fig2, ax2 = plt.subplots()
ax2.pie(
    prix_par_categorie["price_usd"], 
    labels=prix_par_categorie["category"], 
    autopct="%1.1f%%", 
    startangle=90
)
plt.title("Part du CA par catégorie")
st.pyplot(fig2)

# ---- Alerte catégorie dominante ----
part_max = prix_par_categorie["price_usd"].max() / prix_par_categorie["price_usd"].sum() * 100
cat_dom = prix_par_categorie.sort_values("price_usd", ascending=False).iloc[0]["category"]
if part_max > 60:
    st.error(f"🚨 Attention : La catégorie '{cat_dom}' représente {part_max:.1f}% du CA total !")
else:
    st.info(f"La répartition du CA par catégorie est équilibrée (catégorie max : {cat_dom} = {part_max:.1f}%).")

# ---- Zone d'analyse automatique sympa (bonus) ----
st.markdown("### 🤖 Analyse automatique :")
prix_moyen = df["price_usd"].mean()
marge_moyenne = df["margin_usd"].mean()
if prix_moyen > 500:
    st.info(f"Le prix moyen des produits est élevé ({prix_moyen:.2f} $) : votre offre cible probablement un marché haut de gamme.")
else:
    st.info(f"Le prix moyen des produits est abordable ({prix_moyen:.2f} $). Cela peut indiquer une offre compétitive ou entrée/milieu de gamme.")

if marge_moyenne < 120:
    st.warning(f"La marge moyenne est plutôt basse ({marge_moyenne:.2f} $) : attention à la rentabilité des produits !")
else:
    st.success(f"La marge moyenne est correcte ({marge_moyenne:.2f} $).")

nb_outliers = df[df["price_usd"] > df["price_usd"].quantile(0.95)].shape[0]
if nb_outliers > 0:
    st.info(f"💡 {nb_outliers} produit(s) ont un prix exceptionnellement élevé (top 5% du dataset).")

# ---- Footer ----
st.markdown("---")
st.markdown(
    "<div style='text-align:right; font-size:13px;'>Mini-ETL • Dashboard interactif avec Pandas, Streamlit, Matplotlib.</div>",
    unsafe_allow_html=True
)