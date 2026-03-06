import pandas as pd

# On charge ton fichier tout chaud
df = pd.read_csv('resultats_avis_complets.csv')

# On compte combien d'avis on a pour chaque entreprise
comptage = df['Entreprise'].value_counts()

print("📊 DISTRIBUTION DES AVIS PAR ENTREPRISE :")
print(comptage)

print("\n" + "="*30)
print(f"Total avis : {len(df)}")
print(f"Moyenne par entreprise : {comptage.mean():.1f}")
print(f"Entreprise avec le moins d'avis : {comptage.min()}")
print("="*30)