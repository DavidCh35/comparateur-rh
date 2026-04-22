#%%
import pandas as pd

# %%
data_gouv = pd.read_csv("index-egalite-fh(1).csv", sep=';')
# %%
data_gouv.columns
# %%
data_gouv['Raison Sociale'].head()
# %%
data_gouv[data_gouv['Raison Sociale'].str.match("Amazon")]

# %%
data_gouv.info()

# %%
def passage_numerique():
    liste_colonnes = ['Note Ecart rémunération', "Note Ecart taux d'augmentation (hors promotion)", "Note Ecart taux de promotion", "Note Ecart taux d'augmentation", "Note Retour congé maternité", "Note Hautes rémunérations", "Note Index"]
    for colonnes in liste_colonnes:
        data_gouv[colonnes] = data_gouv[colonnes].str.replace(',', '.')
        data_gouv[colonnes] = pd.to_numeric(data_gouv[colonnes], errors="coerce")
# %%
passage_numerique()
# %%
data_gouv.info()
# %%
data_gouv['SIREN'] = data_gouv['SIREN'].astype(str)
data_gouv['Année'] = data_gouv['SIREN'].astype(str)

#%%
#Liste des 30 entreprises
liste_entreprises = [
    "BNP PARIBAS", "SOCIETE GENERALE", "CREDIT AGRICOLE",
    "AXA", "BPCE", "CARREFOUR", "AUCHAN", "DECATHLON",
    "LEROY MERLIN", "L'OREAL", "SEPHORA", "EDF",
    "TOTAL", "RENAULT", "AIRBUS", "SCHNEIDER ELECTRIC",
    "SANOFI", "MICHELIN", "SAINT-GOBAIN", "AIR FRANCE",
    "ACCOR", "BOUYGUES TELECOM", "VINCI", "ORANGE",
    "CAPGEMINI", "SOPRA STERIA", "LA POSTE", 
    "SEPHORA", "VEOLIA", "FNAC", "INTERSPORT", "SAFRAN", 
    "IKEA", "AMAZON", "VERISURE"
]

#Mettre tout en majuscule pour faciliter la recherche
data_gouv['Raison Sociale'] = data_gouv['Raison Sociale'].str.upper()

# 3Boucle pour chercher et renommer
for entreprise in liste_entreprises:
    # création d'un masque 
    # na=False gère les lignes vides pour éviter les erreurs
    masque = data_gouv['Raison Sociale'].str.contains(entreprise, na=False)
    
    # On renomme toutes ces lignes avec le nom propre
    data_gouv.loc[masque, 'Raison Sociale'] = entreprise

# 4. On ne garde que les entreprises de la liste
data_gouv = data_gouv[data_gouv['Raison Sociale'].isin(liste_entreprises)]
# %%
data_gouv.head()
# %%
data_gouv.shape
# %%
data_gouv['Raison Sociale'].unique()
# %%
data_gouv['Raison Sociale'].value_counts()
# %%
manquants = set(liste_entreprises) - set(data_gouv['Raison Sociale'].unique())
print(f"Les entreprises introuvables sont : {manquants}")

# %%
df_indeed = pd.read_csv("avis_entreprises_sentiment.csv")
# %%
df_indeed.head(3)
# %%
df_indeed['Entreprise'] = df_indeed['Entreprise'].str.upper().str.strip()
# %%
# ÉTAPE 1 : On écrase le fichier Gouvernement pour n'avoir qu'une ligne par entreprise
# On prend data_clean et on fait la moyenne de tout (2019, 2020, etc.)
df_gouv_final = data_gouv.groupby('Raison Sociale').mean(numeric_only=True).reset_index()


# ÉTAPE 2 : On prépare le fichier Indeed
df_indeed['Entreprise'] = df_indeed['Entreprise'].str.upper().str.strip()

# On compacte les avis (Note moyenne + Tous les textes collés)
df_indeed_final = df_indeed.groupby('Entreprise').agg({
    'Note': 'mean',
    'Commentaire': lambda x: " // ".join(str(v) for v in x)
}).reset_index()


# Jointure finale
df_final = pd.merge(
    df_gouv_final,             # Gauche
    df_indeed_final,           # Droite
    left_on='Raison Sociale',
    right_on='Entreprise',
    how='inner'
)

# VERIFICATION

df_final.head()
# %%
df_final.head(3)
# %%
# 1. On récupère la liste des noms dans le Gouv 
noms_gouv = set(df_gouv_final['Raison Sociale'])

# 2. On récupère la liste des noms dans Indeed
noms_indeed = set(df_indeed_final['Entreprise'])

# 3. Qui est dans Gouv MAIS PAS dans Indeed ?
perdus = noms_gouv - noms_indeed

print(f"Voici les {len(perdus)} entreprises qui bloquent :")
for nom in perdus:
    print(f"- {nom}")
# %%
# Mots-clés pour retrouver tes disparus dans Indeed
indices = [
    "OREAL",      # Pour L'OREAL
    "GENERALE",   # Pour SOCIETE GENERALE
    "POSTE",      # Pour LA POSTE
    "AGRICOLE",   # Pour CREDIT AGRICOLE
    "FNAC",       # Pour FNAC
    "CAP",        # Pour CAPGEMINI
    "TOTAL",      # Pour TOTAL
    "BPCE"        # Pour BPCE
]

print("--- NOMS TROUVÉS DANS INDEED ---")
for mot in indices:
    # On cherche les noms qui contiennent le mot clé
    trouves = df_indeed[df_indeed['Entreprise'].str.contains(mot, na=False)]['Entreprise'].unique()
    print(f"Mot '{mot}' : {trouves}")
# %%
# Nouveaux indices plus précis (avec accents)
indices_manquants = [
    "ORÉAL",     # Avec l'accent
    "SOCIÉTÉ",   # Avec les accents
    "GEMINI",    # Pour Capgemini
    "LAPOSTE"    # Tout attaché ?
]

print("--- RECHERCHE APPROFONDIE ---")
for mot in indices_manquants:
    res = df_indeed[df_indeed['Entreprise'].str.contains(mot, na=False)]['Entreprise'].unique()
    print(f"Mot '{mot}' : {res}")
# %%
# 1. LE DICTIONNAIRE DE CORRECTION ---
# On dit à Python : "Si tu vois la clé (gauche), remplace par la valeur (droite)"
corrections = {
    "TOTAL ÉNERGIES": "TOTAL",          # On enlève 'Energies'
    "GROUPE BPCE": "BPCE",              # On enlève 'Groupe'
    "GROUPE FNAC DARTY": "FNAC",        # On garde juste Fnac
    "CRÉDIT AGRICOLE": "CREDIT AGRICOLE", # On enlève l'accent
    "L'ORÉAL": "L'OREAL",               # On enlève l'accent sur le E
    "SOCIÉTÉ GÉNÉRALE": "SOCIETE GENERALE" # On enlève les accents
}

# On applique les corrections sur le fichier Indeed
df_indeed['Entreprise'] = df_indeed['Entreprise'].replace(corrections)

# 2. LE COMPACTAGE 
# Côté GOUV : Une seule ligne par entreprise
df_gouv_final = data_gouv.groupby('Raison Sociale').mean(numeric_only=True).reset_index()

# Côté INDEED : Une seule ligne par entreprise
SEPARATEUR = " \n --- NOUVEL AVIS --- \n "
df_indeed_final = df_indeed.groupby('Entreprise').agg({
    'Note': 'mean',
    'Commentaire': lambda x: SEPARATEUR.join(str(v) for v in x if str(v) != 'nan')
}).reset_index()

# --- 3. LA FUSION FINALE ---
df_final = pd.merge(
    df_gouv_final,
    df_indeed_final,
    left_on='Raison Sociale',
    right_on='Entreprise',
    how='inner'
)

# --- 4. SAUVEGARDE ET RÉSULTAT ---
print(f" {len(df_final)} entreprises prêtes.")
df_final.to_csv('data_final.csv', index=False)

# %%
