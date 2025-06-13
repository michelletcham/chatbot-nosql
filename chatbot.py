import os
from dotenv import load_dotenv
import pymongo
import spacy

# Charger variables d'environnement
load_dotenv()
uri = os.getenv("MONGO_URI")

# Connexion à MongoDB
client = pymongo.MongoClient(uri)
db = client["chatbotDB"]
collection = db["produits"]

# Charger modèle spaCy français
nlp = spacy.load("fr_core_news_sm")

def extraire_mots_cles(question):
    doc = nlp(question.lower())
    # On garde noms communs, noms propres et adjectifs
    mots_cles = [token.text for token in doc if token.pos_ in ("NOUN", "PROPN", "ADJ")]
    return mots_cles

def chercher_produit(mots_cles):
    # On cherche un produit dont le nom contient au moins un mot clé
    for mot in mots_cles:
        # Recherche insensible à la casse dans 'nom'
        produit = collection.find_one({"nom": {"$regex": mot, "$options": "i"}})
        if produit:
            return produit
    return None

def repondre(question):
    mots_cles = extraire_mots_cles(question)
    produit = chercher_produit(mots_cles)
    if not produit:
        return "Désolé, je n'ai pas trouvé ce produit."
    
    if "prix" in question.lower():
        return f"Le prix de {produit['nom']} est de {produit['prix']} €."
    elif "description" in question.lower() or "informations" in question.lower():
        return f"Description de {produit['nom']}: {produit['description']}"
    else:
        # Réponse générique
        return f"{produit['nom']}: {produit['description']} (Prix: {produit['prix']} €)"

def main():
    print("Bienvenue dans le chatbot produit ! Tapez 'quit' pour sortir.")
    while True:
        question = input("Vous: ")
        if question.lower() in ("quit", "exit"):
            print("Au revoir !")
            break
        reponse = repondre(question)
        print("Chatbot:", reponse)

if __name__ == "__main__":
    main()
