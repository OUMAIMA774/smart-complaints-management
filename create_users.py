from werkzeug.security import generate_password_hash
import mysql.connector
from config import DB_CONFIG

connexion = mysql.connector.connect(**DB_CONFIG)
cursor = connexion.cursor(dictionary=True)

# Récupérer toutes les divisions existantes
cursor.execute("""
    SELECT id, nom_division
    FROM divisions
""")

divisions = cursor.fetchall()

# Création ADMIN
admin_email = "admin@commune.ma"

cursor.execute("""
    SELECT id FROM utilisateurs
    WHERE email = %s
""", (admin_email,))

admin_existe = cursor.fetchone()

if not admin_existe:
    cursor.execute("""
        INSERT INTO utilisateurs (
            nom,
            email,
            mot_de_passe,
            role,
            division_id,
            doit_changer_mot_de_passe
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        "Administrateur Commune",
        admin_email,
        generate_password_hash("admin123"),
        "admin",
        None,
        1
    ))

    print("Admin créé : admin@commune.ma / admin123")

# Création automatique des chefs de divisions
for division in divisions:

    division_id = division["id"]
    nom_division = division["nom_division"]

    nom_normalise = nom_division.lower()

    nom_normalise = (
        nom_normalise
        .replace("division", "")
        .replace("é", "e")
        .replace("è", "e")
        .replace("ê", "e")
        .replace("à", "a")
        .replace("ù", "u")
        .replace("ô", "o")
        .replace("î", "i")
        .replace(" ", "")
        .strip()
    )

    email = f"{nom_normalise}@commune.ma"
    mot_de_passe = f"{nom_normalise}123"

    cursor.execute("""
        SELECT id FROM utilisateurs
        WHERE email = %s
    """, (email,))

    existe = cursor.fetchone()

    if not existe:
        cursor.execute("""
            INSERT INTO utilisateurs (
                nom,
                email,
                mot_de_passe,
                role,
                division_id,
                doit_changer_mot_de_passe
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            f"Chef {nom_division}",
            email,
            generate_password_hash(mot_de_passe),
            "chef_division",
            division_id,
            1
        ))

        print(f"Utilisateur créé : {email} / {mot_de_passe}")

connexion.commit()
cursor.close()
connexion.close()

print("Tous les utilisateurs ont été créés avec succès.")