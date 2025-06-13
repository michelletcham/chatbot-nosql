from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import pymongo
import spacy

load_dotenv()
uri = os.getenv("MONGO_URI")

client = pymongo.MongoClient(uri)
db = client["chatbotDB"]
collection = db["produits"]

nlp = spacy.load("fr_core_news_sm")

app = Flask(__name__)

def extraire_mots_cles(question):
    doc = nlp(question.lower())
    return [token.text for token in doc if token.pos_ in ("NOUN", "PROPN", "ADJ")]

def chercher_produit(mots_cles):
    for mot in mots_cles:
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
        return f"{produit['nom']}: {produit['description']} (Prix: {produit['prix']} €)"

@app.route("/", methods=["GET", "POST"])
def index():
    reponse = None
    if request.method == "POST":
        question = request.form.get("question")
        reponse = repondre(question)
    return render_template("index.html", reponse=reponse)

if __name__ == "__main__":
    app.run(debug=True)
