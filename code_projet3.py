import pandas as pd
import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Configuration
dossier_projet = os.getcwd()
chemin_profil = os.path.join(dossier_projet, "profil_indeed")

options = Options()
options.add_argument(f"user-data-dir={chemin_profil}")
options.add_argument("--disable-blink-features=AutomationControlled") 
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

donnees_finales = []

try:
    df_entreprises = pd.read_csv('entreprises_cibles.csv')
    
    # Boucle 1 : Les entreprises
    for index, row in df_entreprises.iterrows():
        entreprise = row['nom_entreprise']
        url_base = row['url_indeed']
        
        print(f"\n🏢 [{index+1}/{len(df_entreprises)}] ENTREPRISE : {entreprise}")
        
        # Boucle 2 : LES PAGES (0, 20, 40, 60, 80) ---
        for offset in [0, 20, 40, 60, 80]:
            
            if offset == 0:
                url_page = url_base
            else:
                # Petite astuce : si l'URL a déjà un '?', on met '&', sinon '?'
                separateur = "&" if "?" in url_base else "?"
                url_page = f"{url_base}{separateur}start={offset}"
            
            print(f"   📄 Page (offset {offset})...")
            driver.get(url_page)
            
            # Pause aléatoire (très important pour ne pas se faire bloquer en changeant de page)
            time.sleep(random.uniform(3, 6))
            
            # extraction
            cartes_avis = driver.find_elements(By.CSS_SELECTOR, "[data-testid='reviews[]']")
            
            # Si pas d'avis sur cette page (ex: l'entreprise n'a que 30 avis au total), on arrête cette boucle
            if len(cartes_avis) == 0:
                print("Plus d'avis disponibles, on passe à l'entreprise suivante.")
                break
                
            for carte in cartes_avis:
                try:
                    titre = carte.find_element(By.CSS_SELECTOR, ".css-15r9gu1").text
                    
                    el_note = carte.find_element(By.CSS_SELECTOR, ".css-2wfjnm")
                    note_brute = el_note.get_attribute("aria-label") or el_note.text
                    note_propre = note_brute.split('/')[0].replace(',', '.').strip()
                    
                    texte = carte.find_element(By.CSS_SELECTOR, "[data-testid='reviewDescription']").text
                    
                    donnees_finales.append({
                        "Entreprise": entreprise,
                        "Note": note_propre,
                        "Titre": titre,
                        "Commentaire": texte
                    })
                except:
                    pass 

except Exception as e:
    print(f"❌ Erreur critique : {e}")

finally:
    driver.quit()
    
    if donnees_finales:
        df_resultat = pd.DataFrame(donnees_finales)
        df_resultat.to_csv('resultats_avis_complets.csv', index=False)
    else:
        print("⚠️ Aucun avis récupéré.")