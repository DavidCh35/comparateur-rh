# RH Insight IA : Analyseur de Marque Employeur

> **Automatisez votre benchmark RH et décryptez l'expérience collaborateur grâce à l'IA.**

Ce projet est une solution de **Business Intelligence** conçue pour les services RH. Elle permet de comparer les performances sociales des entreprises et de générer des synthèses d'avis salariés en temps réel via des modèles de langage (LLM).

---

## Le Besoin Métier
L'objectif est de fournir aux décideurs RH un outil d'aide à la décision pour :
*   **Benchmarker la concurrence :** Comparer la satisfaction globale et l'égalité professionnelle entre plusieurs entreprises cibles.
*   **Analyser le sentiment à grande échelle :** Extraire automatiquement les points forts et axes d'amélioration à partir de milliers d'avis salariés textuels.
*   **Fiabiliser les données :** Réconcilier les données de satisfaction avec les bases de données officielles (SIREN / Index Égalité F-H).

## Fonctionnalités Clés
*   **Analyse Sémantique Haute Performance :** Utilisation de l'API Groq (Llama 3.1 8B) pour une analyse de sentiment et de thématiques quasi-instantanée.
*   **Interface Décisionnelle :** Dashboard interactif avec indicateurs dynamiques (KPIs) basés sur l'Index Égalité et le scoring collaborateur.
*   **Réconciliation de données :** Croisement intelligent entre les données collectées (Scraping) et les référentiels gouvernementaux

## 🏗️ Architecture & Data Pipeline
1.  **Collecte :** Scraping d'avis sur les plateformes de notation (Indeed).
2.  **Traitement :** Nettoyage des données avec Python & Pandas et normalisation des SIREN.
3.  **Analyse :** Extraction de thématiques (NLP) et scoring via LLM.
4.  **Visualisation :** Application Web interactive développée avec Streamlit.

## 🛠️ Stack Technique
*   **Langage :** Python 3.9+
*   **Data Analysis :** Pandas, NumPy
*   **IA / LLM :** Groq (Llama 3.1)
*   **Restitution :** Streamlit
*   **Architecture :** Caching (`@st.cache_data`), Parsing JSON structuré, Gestion des secrets (Secrets management).

---

## 📦 Installation & Utilisation
1. Cloner le projet : `git clone [ton-lien-github]`
2. Installer les dépendances : `pip install -r requirements.txt`
3. Lancer l'application : `streamlit run app.py`

---
**Développé par David C. — Data Analyst (Bordeaux Métropole)**