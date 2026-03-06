#%%
import pandas as pd
from transformers import pipeline

# %%
df = pd.read_csv("avis_entreprises_clean.csv", sep = ',')
# %%
notation = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
# %%
def recuperer_score(commentaire):
    #On s'assure que c'est du texte et de ne pas dépasser la limite de 512 caractères
    texte = str(commentaire)[:512]
    #On passe le commentaire dans l'IA
    resultat = notation(texte)
    #On recupere le texte du label avec [0] pour la liste puis ['label'] pour le dictionnaire
    note = resultat[0]['label']
    #On prend le premier caractère et on le transforme en entier
    return int(note[0])
# %%
df_test = df.head(5).copy()
df_test['Sentiment_IA'] = df_test['Commentaire'].apply(recuperer_score)
print(df_test[['Commentaire', 'Note', 'Sentiment_IA']])

# Application sur tout le dataset
df['Sentiment_IA'] = df['Commentaire'].apply(recuperer_score)


# Sauvegarde
df.to_csv("avis_entreprises_sentiment.csv", index=False)
# %%
