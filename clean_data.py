#%%
import pandas as pd

#%%
df = pd.read_csv("resultats_avis_complets.csv", sep= ',')

#%%
print(df.head())
# %%
print(df.info())

# %%
df['Note'] = pd.to_numeric(df['Note'], errors='coerce')
df = df.drop_duplicates(subset=['Entreprise', 'Titre', 'Commentaire'])
df.info()
# %%
df = df.dropna(subset=['Note'])
df.info()
# %%
df['Titre'] = df['Titre'].fillna('Aucun titre')
df.info()
# %%
df.to_csv("avis_entreprises_clean.csv", index= False)
# %%
classement = df.groupby('Entreprise')['Note'].mean().sort_values(ascending=False)
# %%
classement
# %%
verisure = df[df['Entreprise'] == 'Verisure']
print(verisure['Note'].value_counts())
# %%
# 
flop_df = df[df['Entreprise'] == 'Intersport']
print(flop_df['Note'].value_counts())
# %%
