import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Mini-ETL Dashboard", layout="wide")

# ---- Chargement des données ----
uploaded_file = st.sidebar.file_uploader("🗂️ Importer un fichier CSV (optionnel)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    # Remarque : si tu veux pouvoir calculer les mêmes stats/graphes, adapte ici selon tes besoins
    prix_par_produit = pd.DataFrame(columns=["name", "price_usd"])
    prix_par_categorie = pd.DataFrame(columns=["category", "price_usd"])
    kpi = pd.DataFrame()
else:
    try:
        df = pd.read_csv("exports/clean_data.csv")
        prix_par_produit = pd.read_csv("exports/prix_par_produit.csv")
        prix_par_categorie = pd.read_csv("exports/prix_par_categorie.csv")
        kpi = pd.read_csv("exports/indicateurs.csv")
    except Exception as e:
        st.error("Erreur lors du chargement des fichiers. Lance d'abord le pipeline ETL !")
        st.stop()

# ===== MENU "À PROPOS DU PROJET" EN HAUT DE LA PAGE =====
with st.expander("ℹ️ À propos du projet", expanded=False):
    st.markdown("""
    **Mini-ETL Dashboard**

    - _Projet universitaire Data/Master 1_
    - Réalisé par **Nabila ARAB**
    - Mars 2026  
    - [Lien GitHub du projet](https://github.com/Nabila-arab/mini-etl-dashboard)

    **Mode d'emploi rapide :**
    1. Utilisez les filtres pour explorer les données (recherche, catégories, seuil, etc.).
    2. Téléchargez les résultats filtrés en CSV ou Excel.
    3. Visualisez les graphiques (KPI, top produits, répartitions…).
    4. FAQ/contact dans la sidebar.

    <sub>⚠️ Export PDF désactivé sur le cloud pour compatibilité universelle.</sub>
    """, unsafe_allow_html=True)

st.title("📊 Dashboard Mini-ETL Produits")


# ---- Filtres sidebar ----
st.sidebar.title("🔎 Filtres")

search = st.sidebar.text_input("🔤 Recherche (nom ou catégorie)", "")
df_filtré = df[
    df["name"].astype(str).str.contains(search, case=False, na=False) |
    df["category"].astype(str).str.contains(search, case=False, na=False)
] if search else df

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

# ---- Boutons d'export ----
csv_filtre = df_filtré.to_csv(index=False).encode()
st.sidebar.download_button(
    label="⬇️ Télécharger produits filtrés (CSV)",
    data=csv_filtre,
    file_name="produits_filtres.csv",
    mime="text/csv"
)
csv_chers = df_cher.to_csv(index=False).encode()
st.sidebar.download_button(
    label="⬇️ Télécharger produits chers (CSV)",
    data=csv_chers,
    file_name="produits_chers.csv",
    mime="text/csv"
)
excel_bytes = io.BytesIO()
df_filtré.to_excel(excel_bytes, index=False, engine='openpyxl')
excel_bytes.seek(0)
st.sidebar.download_button(
    label="⬇️ Télécharger produits filtrés (Excel)",
    data=excel_bytes,
    file_name="produits_filtres.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.sidebar.warning("⚠️ Export PDF désactivé (fonctionnalité non supportée sur cette plateforme). Export Excel & CSV : OK.")

# ---- Bloc FAQ/Contact ----
with st.sidebar.expander("❓ FAQ / Contact", expanded=False):
    st.markdown("""
    - **Contact** : nabila.arab@email.com
    - Problème d'affichage ? Rafraîchissez la page.
    - Téléchargement impossible ? Essayez un autre navigateur.
    - Infos projet sur [GitHub](https://github.com/Nabila-arab/mini-etl-dashboard).
    """)

st.sidebar.markdown("---")
st.sidebar.markdown("**Projet – Nabila ARAB | MSc Data – 2026**")

# ---- Partie principale du dashboard : KPIs etc ----

if not uploaded_file:
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Prix total", f"{df['price_usd'].sum():,.2f} $")
    col2.metric("📦 Nombre de produits", int(df['product_id'].nunique()))
    col3.metric("📈 Marge totale", f"{df['margin_usd'].sum():,.2f} $")

    if not prix_par_produit.empty:
        top_prod = prix_par_produit.sort_values("price_usd", ascending=False).iloc[0]
        st.info(f"**Top produit (CA)** : {top_prod['name']} ({top_prod['price_usd']}$)")

    st.markdown("---")
else:
    st.info("Analytics et graphiques détaillés désactivés sur import CSV utilisateur (démo simplifiée).")

# ---- Tableau stylé des produits filtrés ----
st.header("📝 Tableau des produits (filtres)")
st.dataframe(df_filtré.astype(str), use_container_width=True)

# ---- Produits chers (si les colonnes sont présentes) ----
if "price_usd" in df_filtré.columns and "category" in df_filtré.columns:
    st.header(f"🔥 Produits dont le prix > {seuil} $")
    if not df_cher.empty:
        st.dataframe(df_cher.astype(str))
    else:
        st.warning("Aucun produit ne correspond à ce filtre dans la sélection courante.")
# ---- Graphiques principaux ----
if not uploaded_file and not prix_par_produit.empty and not prix_par_categorie.empty:
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

    # Alertes analytiques
    part_max = prix_par_categorie["price_usd"].max() / prix_par_categorie["price_usd"].sum() * 100
    cat_dom = prix_par_categorie.sort_values("price_usd", ascending=False).iloc[0]["category"]
    if part_max > 60:
        st.error(f"🚨 Attention : La catégorie '{cat_dom}' représente {part_max:.1f}% du CA total !")
    else:
        st.info(f"La répartition du CA par catégorie est équilibrée (catégorie max : {cat_dom} = {part_max:.1f}%).")

    # Analyse automatique
    st.markdown("### 🤖 Analyse automatique :")
    prix_moyen = df["price_usd"].mean()
    marge_moyenne = df["margin_usd"].mean()
    if prix_moyen > 500:
        st.info(f"Le prix moyen des produits est élevé ({prix_moyen:.2f} $).")
    else:
        st.info(f"Le prix moyen des produits est abordable ({prix_moyen:.2f} $).")

    if marge_moyenne < 120:
        st.warning(f"La marge moyenne est plutôt basse ({marge_moyenne:.2f} $) : attention à la rentabilité !")
    else:
        st.success(f"La marge moyenne est correcte ({marge_moyenne:.2f} $).")

    nb_outliers = df[df["price_usd"] > df["price_usd"].quantile(0.95)].shape[0]
    if nb_outliers > 0:
        st.info(f"💡 {nb_outliers} produit(s) ont un prix exceptionnellement élevé (top 5 % du dataset).")

st.markdown("---")
st.markdown(
    "<div style='text-align:right; font-size:13px;'>Mini-ETL • Dashboard interactif | Pandas / Streamlit / Matplotlib • 2026</div>",
    unsafe_allow_html=True
)