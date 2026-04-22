import streamlit as st
import pandas as pd
from groq import Groq
import json
import os

# --- 1. CONFIGURATION & THÈME VISUEL ---
st.set_page_config(
    page_title="RH Analytics | Comparateur IA",
    layout="wide",
    page_icon="⚖️"
)

# Injection de CSS pour le style "Corporate RH" (Bleus, Gris, Blancs)
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .stMetric {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        h1, h2, h3 {
            color: #1e3a8a; /* Bleu Corporate */
        }
        .stButton>button {
            background-color: #1e3a8a;
            color: white;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. GARDIEN DE FICHIER ---
FICHIER_DATA = "data/data_final.csv"

if not os.path.exists(FICHIER_DATA):
    st.error("🚨 Fichier de données absent.")
    st.stop()

# --- 3. FONCTIONS CACHÉES (LOGIQUE) ---
@st.cache_resource
def get_groq_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

@st.cache_data(show_spinner=False)
def load_data(path):
    return pd.read_csv(path)

@st.cache_data(show_spinner=False)
def generer_synthese_robuste(avis):
    client = get_groq_client()
    prompt = (
        f"Agis en expert RH. Analyse ces avis : {avis}. "
        "Tu dois impérativement répondre au format JSON avec exactement ces deux clés : "
        "'points_forts' (une liste de max 6 points) et 'points_faibles' (une liste de max 6 points). "
        "Sois factuel, direct, et ne produis aucun texte en dehors du bloc JSON."
    )
    try:
        reponse = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        return json.loads(reponse.choices[0].message.content)
    except Exception:
        return {"erreur": "Désolé, l'analyse automatique rencontre une difficulté technique, merci de réessayer."}

# --- 4. BARRE LATÉRALE (SIDEBAR) & SECTION "À PROPOS" ---
df = load_data(FICHIER_DATA)

with st.sidebar:
    st.title("💼 RH Insight IA")
    
    # Section À Propos (Nouveauté)
    with st.expander("🛠️ Stack Technique", expanded=True):
        st.markdown(f"""
        **Moteur :** Llama 3.1-8b (Groq API)  
        **Langage :** Python  
        **Interface :** Streamlit  
        **Données :** Pandas  
        """)
        st.caption("Ce projet utilise le RAG (Retrieval Augmented Generation) simplifié pour l'analyse de sentiment RH.")

    st.divider()
    
    liste_entreprises = df['Raison Sociale'].unique()
    choix = st.selectbox("Sélectionner une entreprise", liste_entreprises)
    infos = df[df['Raison Sociale'] == choix].iloc[0]
    
    st.markdown("---")
    st.markdown("🔍 *Développé pour l'aide à la décision stratégique.*")

# --- 5. INTERFACE PRINCIPALE & INDICATEURS DYNAMIQUES ---
st.title(f"Analyse Stratégique : {choix}")

# Logique de couleur pour les indicateurs
def get_color(valeur, seuil_haut=75, seuil_bas=40):
    if valeur >= seuil_haut: return "#28a745" # Vert
    if valeur <= seuil_bas: return "#dc3545"  # Rouge
    return "#fd7e14" # Orange

col1, col2 = st.columns(2)

with col1:
    val_index = round(infos['Note Index'], 1)
    color_index = get_color(val_index)
    st.markdown(f"""
        <div style="padding:10px; border-left: 5px solid {color_index}; background:white; border-radius:5px">
            <p style="margin:0; font-size:14px; color:gray;">Index Égalité Professionnelle</p>
            <h2 style="margin:0; color:{color_index};">{val_index} / 100</h2>
        </div>
    """, unsafe_allow_html=True)

with col2:
    val_note = round(infos['Note'], 1)
    # On ramène la note sur 100 pour la logique de couleur (ex: 4/5 = 80/100)
    color_note = get_color(val_note * 20)
    st.markdown(f"""
        <div style="padding:10px; border-left: 5px solid {color_note}; background:white; border-radius:5px">
            <p style="margin:0; font-size:14px; color:gray;">Satisfaction Salariés (Indeed)</p>
            <h2 style="margin:0; color:{color_note};">{val_note} / 5</h2>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- 6. SECTION ANALYSE IA ---
st.subheader("🤖 Synthèse de l'Expertise IA")
avis_bruts = str(infos['Commentaire'])

if len(avis_bruts) < 30:
    st.warning("Volume d'avis insuffisant pour une analyse statistique représentative.")
else:
    if st.button("Lancer l'analyse sémantique"):
        with st.spinner("Extraction des tendances RH en cours..."):
            resultat = generer_synthese_robuste(avis_bruts[:15000])
            
            if "erreur" in resultat:
                st.warning(resultat["erreur"])
            else:
                c1, c2 = st.columns(2)
                with c1:
                    st.success("**✅ Forces Identifiées**")
                    for p in resultat.get('points_forts', []):
                        st.markdown(f"- {p}")
                with c2:
                    st.error("**⚠️ Points de Vigilance**")
                    for p in resultat.get('points_faibles', []):
                        st.markdown(f"- {p}")

st.divider()
st.caption("© 2026 | Application de démonstration RH | Données confidentielles traitées localement.")