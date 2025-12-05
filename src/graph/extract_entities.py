import pandas as pd
import re
from collections import defaultdict

# --- 1. Charger le dataset nettoyé ---
df = pd.read_csv("../../data/medtext_2clean.csv")

# --- 2. Définir des listes initiales de mots-clés (option hybride) ---
# Tu peux compléter ou améliorer ces listes plus tard
disease_keywords = [
    "diabetes", "rosacea", "osteoarthritis", "acl tear", "pneumonia",
    "hepatitis", "scaphoid fracture", "sciatica", "esophageal cancer"
]

symptom_keywords = [
    "pain", "fever", "weight loss", "fatigue", "dizziness", "swelling",
    "numbness", "redness", "cough", "shortness of breath"
]

treatment_keywords = [
    "MRI", "CT scan", "antibiotics", "fluids", "physical therapy",
    "surgery", "RICE therapy", "brace", "topical treatment"
]

# --- 3. Créer des ensembles pour stocker les entités uniques ---
diseases_set = set()
symptoms_set = set()
treatments_set = set()

# Relations
has_symptom = []
treated_by = []

# --- 4. Fonction d'extraction simple par mot-clé ---
def find_entities(text, keywords):
    found = set()
    text_lower = text.lower()
    for kw in keywords:
        if kw.lower() in text_lower:
            found.add(kw)
    return found

# --- 5. Parcourir le dataset et extraire les entités et relations ---
for idx, row in df.iterrows():
    prompt = row['Prompt']
    completion = row['Completion']

    # Extraire maladies du prompt et completion
    diseases_in_text = find_entities(prompt, disease_keywords).union(
        find_entities(completion, disease_keywords)
    )
    symptoms_in_text = find_entities(prompt, symptom_keywords)
    treatments_in_text = find_entities(completion, treatment_keywords)

    # Ajouter aux sets
    diseases_set.update(diseases_in_text)
    symptoms_set.update(symptoms_in_text)
    treatments_set.update(treatments_in_text)

    # Relations
    for disease in diseases_in_text:
        for symptom in symptoms_in_text:
            has_symptom.append((disease, symptom))
        for treatment in treatments_in_text:
            treated_by.append((disease, treatment))

# --- 6. Convertir en DataFrames pour sauvegarde ---
df_diseases = pd.DataFrame({"Disease": list(diseases_set)})
df_symptoms = pd.DataFrame({"Symptom": list(symptoms_set)})
df_treatments = pd.DataFrame({"Treatment": list(treatments_set)})

df_has_symptom = pd.DataFrame(has_symptom, columns=["Disease", "Symptom"])
df_treated_by = pd.DataFrame(treated_by, columns=["Disease", "Treatment"])

# --- 7. Sauvegarder tous les fichiers dans le dossier data/ ---
df_diseases.to_csv("../../data/diseases.csv", index=False)
df_symptoms.to_csv("../../data/symptoms.csv", index=False)
df_treatments.to_csv("../../data/treatments.csv", index=False)
df_has_symptom.to_csv("../../data/has_symptom.csv", index=False)
df_treated_by.to_csv("../../data/treated_by.csv", index=False)

print("Extraction terminée !")
print(f"Maladies : {diseases_set}")
print(f"Symptômes : {symptoms_set}")
print(f"Traitements : {treatments_set}")
print(f"Relations HAS_SYMPTOM : {len(has_symptom)}")
print(f"Relations TREATED_BY : {len(treated_by)}")
print("Fichiers sauvegardés dans 'data/'")
