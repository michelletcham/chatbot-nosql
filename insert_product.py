import os
from dotenv import load_dotenv
import pymongo

# Charger les variables d'environnement
load_dotenv()
uri = os.getenv("MONGO_URI")

# Connexion MongoDB
client = pymongo.MongoClient(uri)
db = client["chatbotDB"]
collection = db["produits"]

# Produits à insérer
produits = [
    {
        "nom": "Ordinateur Portable",
        "prix": 799.99,
        "description": "Ordinateur performant avec 16 Go de RAM et un écran Full HD.",
        "catégorie": "Électronique"
    },
    {
        "nom": "Casque Bluetooth",
        "prix": 59.99,
        "description": "Casque sans fil avec réduction de bruit active.",
        "catégorie": "Audio"
    },
    {
        "nom": "Smartphone",
        "prix": 499.99,
        "description": "Smartphone avec écran OLED et appareil photo 12MP.",
        "catégorie": "Électronique"
    },
    {
        "nom": "Clavier Mécanique",
        "prix": 89.99,
        "description": "Clavier mécanique rétroéclairé avec touches programmables.",
        "catégorie": "Informatique"
    },
    {
        "nom": "Montre Connectée",
        "prix": 199.99,
        "description": "Montre avec suivi d'activité et notifications smartphone.",
        "catégorie": "Wearable"
    }
]

# Insérer les produits dans la collection
result = collection.insert_many(produits)
print(f"{len(result.inserted_ids)} produits insérés avec succès.")
