import pandas as pd
import mysql.connector
import re
import nltk
import joblib

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

try:
    stopwords.words("french")
except LookupError:
    nltk.download("stopwords")


connexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="data_citoyen"
)

query = """
SELECT texte_complet, categorie_ml
FROM reclamations
WHERE categorie_ml IS NOT NULL
AND texte_complet IS NOT NULL
AND texte_complet <> '';
"""

df = pd.read_sql(query, connexion)
connexion.close()


def nettoyer_texte(texte):
    texte = str(texte).lower()
    texte = re.sub(r"[^a-zA-Zàâçéèêëîïôûùüÿñæœ ]", " ", texte)
    texte = re.sub(r"\s+", " ", texte).strip()

    stop_words = set(stopwords.words("french"))
    mots = texte.split()
    mots = [mot for mot in mots if mot not in stop_words and len(mot) > 2]

    return " ".join(mots)


df["texte_nettoye"] = df["texte_complet"].apply(nettoyer_texte)

X = df["texte_nettoye"]
y = df["categorie_ml"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

modele = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 2),
        max_df=0.90,
        min_df=2
    )),
    ("classifier", LogisticRegression(
        max_iter=1000,
        C=0.7
    ))
])

modele.fit(X_train, y_train)

y_pred = modele.predict(X_test)

print("Accuracy :", accuracy_score(y_test, y_pred))
print("\nRapport de classification :")
print(classification_report(y_test, y_pred))

scores = cross_val_score(modele, X, y, cv=5)
print("\nValidation croisée :", scores)
print("Moyenne :", scores.mean())

joblib.dump(modele, "ml/modele_reclamations.pkl")

print("\nModèle sauvegardé dans ml/modele_reclamations.pkl")