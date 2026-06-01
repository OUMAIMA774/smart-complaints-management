from flask import Flask, redirect, render_template, request, send_from_directory, session, send_file, url_for, flash
from streamlit import pdf
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import mysql.connector
from config import DB_CONFIG, SECRET_KEY, UPLOAD_FOLDER
import os
from datetime import datetime
import joblib
import re
import nltk
from nltk.corpus import stopwords
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from config import GEMINI_API_KEY
import google.generativeai as genai
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
import io

app = Flask(__name__)

genai.configure(api_key=GEMINI_API_KEY)

gemini_model = genai.GenerativeModel("gemini-2.5-flash")
app.secret_key = SECRET_KEY
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
modele_ml = joblib.load("ml/modele_reclamations.pkl")

try:
    stopwords.words("french")
except LookupError:
    nltk.download("stopwords")


def get_db_connection():
    connexion = mysql.connector.connect(**DB_CONFIG)
    return connexion
def traduire_vers_arabe(texte):
    if not texte:
        return ""

    prompt = f"""
Tu es un traducteur administratif.
Traduis uniquement le texte suivant du français vers l'arabe.
Garde un style clair, officiel et professionnel.
Ne rajoute aucune explication.

Texte :
{texte}
"""

    try:
        response = gemini_model.generate_content(prompt)

        if response and response.text:
            print("TRADUCTION GEMINI OK")
            print(response.text)
            return response.text.strip()

        print("Gemini n'a retourné aucun texte")
        return texte

    except Exception as e:
        print("ERREUR GEMINI DETAIL :", e)
        return texte
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper
def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return redirect("/login")

        if session["role"] != "admin":
            return "Accès réservé à l'administrateur", 403

        return f(*args, **kwargs)

    return wrapper
def contient_arabe(texte):
    if not texte:
        return False

    return bool(re.search(r'[\u0600-\u06FF]', texte))


def traduire_vers_francais(texte):
    if not texte:
        return ""

    prompt = f"""
Tu es un traducteur administratif.
Traduis uniquement le texte suivant de l'arabe vers le français.
Garde le sens exact de la réclamation.
Ne rajoute aucune explication.

Texte :
{texte}
"""

    try:
        response = gemini_model.generate_content(prompt)

        if response and response.text:
            print("TRADUCTION ARABE -> FR OK")
            print(response.text)
            return response.text.strip()

        return texte

    except Exception as e:
        print("ERREUR TRADUCTION ARABE -> FR :", e)
        return texte


def preparer_texte_pour_ml(texte):
    if contient_arabe(texte):
        return traduire_vers_francais(texte)

    return texte


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/test-db")
def test_db():
    try:
        connexion = get_db_connection()
        cursor = connexion.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        cursor.close()
        connexion.close()

        return f"Connexion réussie à la base : {db_name[0]}"

    except Exception as e:
        return f"Erreur de connexion : {e}"


def generer_code_reclamation():
    connexion = get_db_connection()
    cursor = connexion.cursor()

    cursor.execute("SELECT MAX(id) FROM reclamations")
    dernier_id = cursor.fetchone()[0]

    cursor.close()
    connexion.close()

    if dernier_id is None:
        dernier_id = 0

    annee = datetime.now().year

    return f"REC-{annee}-{dernier_id + 1:04d}"

@app.route("/deposer", methods=["GET", "POST"])
def deposer_reclamation():
    if request.method == "POST":
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        cin = request.form["cin"]
        telephone = request.form["telephone"]
        email = request.form["email"]
        zone = request.form["zone"]
        objet = request.form["objet"]
        description = request.form["description"]

        code_reclamation = generer_code_reclamation()
        texte_pour_ml = preparer_texte_pour_ml(description)

        categorie_predite = classifier_reclamation(texte_pour_ml)
        priorite, score_priorite = detecter_priorite(texte_pour_ml)
        division_id = get_division_id(categorie_predite)

        fichier_nom = None
        fichier = request.files.get("fichier")

        if fichier and fichier.filename != "":
            fichier_nom = code_reclamation + "_" + fichier.filename
            chemin = os.path.join(app.config["UPLOAD_FOLDER"], fichier_nom)
            fichier.save(chemin)

        connexion = get_db_connection()
        cursor = connexion.cursor()

        cursor.execute("""
            INSERT INTO citoyens (nom, prenom, cin, telephone, email)
            VALUES (%s, %s, %s, %s, %s)
        """, (nom, prenom, cin, telephone, email))

        citoyen_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO reclamations (
                code_reclamation, citoyen_id, zone, objet,
                description, categorie_predite, priorite,
                score_priorite, division_id, fichier_joint, statut
             )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                code_reclamation,
                citoyen_id,
                zone,
                objet,
                description,
                categorie_predite,
                priorite,
                score_priorite,
                division_id,
                fichier_nom,
                "nouvelle"
            ))

        reclamation_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO historique_reclamations (
            reclamation_id, action, nouveau_statut, nouvelle_division
        )
        VALUES (%s, %s, %s, %s)
        """, (
            reclamation_id,
            f"Réclamation déposée, classifiée automatiquement en '{categorie_predite}' avec priorité '{priorite}'",
            "nouvelle",
            division_id
        ))

        connexion.commit()
        cursor.close()
        connexion.close()

        return render_template(
    "confirmation.html",
    code_reclamation=code_reclamation
)

    return render_template("deposer_reclamation.html")
@app.route('/suivi', methods=['GET', 'POST'])
def suivi():
    error = None

    if request.method == 'POST':
        cin = request.form.get('cin', '').strip().upper()
        code = request.form.get('code', '').strip().upper()

        connexion = get_db_connection()
        cur = connexion.cursor(dictionary=True)

        cur.execute("""
            SELECT r.*, d.nom_division
            FROM reclamations r
            LEFT JOIN divisions d ON r.division_id = d.id
            LEFT JOIN citoyens c ON r.citoyen_id = c.id
            WHERE UPPER(c.cin) = %s AND UPPER(r.code_reclamation) = %s
        """, (cin, code))

        reclamation = cur.fetchone()

        if reclamation:
            cur.execute("""
                SELECT *
                FROM reponses
                WHERE reclamation_id = %s
                ORDER BY date_reponse DESC
                LIMIT 1
            """, (reclamation['id'],))

            reponse = cur.fetchone()

            cur.close()
            connexion.close()

            # VERSION FRANÇAISE
            objet_fr = reclamation["objet"]
            zone_fr = reclamation["zone"]

            if contient_arabe(reclamation["objet"]):
                objet_fr = traduire_vers_francais(reclamation["objet"])

            if contient_arabe(reclamation["zone"]):
                zone_fr = traduire_vers_francais(reclamation["zone"])

            # VERSION ARABE
            objet_ar = reclamation["objet"]
            zone_ar = reclamation["zone"]

            if not contient_arabe(reclamation["objet"]):
                objet_ar = traduire_vers_arabe(reclamation["objet"])

            if not contient_arabe(reclamation["zone"]):
                zone_ar = traduire_vers_arabe(reclamation["zone"])

            # CATÉGORIE ET DIVISION
            categories_ar = {
                "eclairage": "الإنارة العمومية",
                "eau": "الماء",
                "voirie": "الطرق",
                "proprete": "النظافة"
            }

            divisions_ar = {
                "Division Éclairage Public": "قسم الإنارة العمومية",
                "Division Eau": "قسم الماء",
                "Division Voirie": "قسم الطرق",
                "Division Propreté": "قسم النظافة"
            }

            categorie_ar = categories_ar.get(
                reclamation["categorie_predite"],
                reclamation["categorie_predite"]
            )

            division_ar = divisions_ar.get(
                reclamation["nom_division"],
                reclamation["nom_division"] or "—"
            )

            reponse_traduite = ""

            if reponse:
                if contient_arabe(reponse["message"]):
                    reponse_traduite = reponse["message"]
                else:
                    reponse_traduite = traduire_vers_arabe(reponse["message"])

            return render_template(
                'resultat_suivi.html',
                reclamation=reclamation,
                reponse=reponse,

                objet_fr=objet_fr,
                zone_fr=zone_fr,

                objet_ar=objet_ar,
                zone_ar=zone_ar,
                categorie_ar=categorie_ar,
                division_ar=division_ar,

                reponse_traduite=reponse_traduite
            )

        else:
            error = "Aucune réclamation trouvée. Vérifiez votre CIN et votre code."

            cur.close()
            connexion.close()

    return render_template('suivi.html', error=error)
def classifier_reclamation(description):
    texte_nettoye = nettoyer_texte(description)
    prediction = modele_ml.predict([texte_nettoye])
    return prediction[0]

def detecter_priorite(description):
    texte = description.lower()

    mots_urgents = ["danger", "accident", "risque", "école", "enfant", "grave", "urgent"]
    mots_eleves = ["fuite", "débordement", "coupure", "égout", "odeur forte", "bloqué"]
    mots_moyens = ["depuis plusieurs jours", "problème", "dérange"]

    if any(mot in texte for mot in mots_urgents):
        return "urgente", 90

    elif any(mot in texte for mot in mots_eleves):
        return "elevee", 70

    elif any(mot in texte for mot in mots_moyens):
        return "moyenne", 50

    else:
        return "faible", 30


def get_division_id(categorie):
    connexion = get_db_connection()
    cursor = connexion.cursor()

    cursor.execute("""
        SELECT id FROM divisions
        WHERE categorie_associee = %s
    """, (categorie,))

    result = cursor.fetchone()

    cursor.close()
    connexion.close()

    if result:
        return result[0]

    return None
def nettoyer_texte(texte):
    texte = str(texte).lower()
    texte = re.sub(r"[^a-zA-Zàâçéèêëîïôûùüÿñæœ ]", " ", texte)
    texte = re.sub(r"\s+", " ", texte).strip()

    stop_words = set(stopwords.words("french"))
    mots = texte.split()
    mots = [mot for mot in mots if mot not in stop_words and len(mot) > 2]

    return " ".join(mots)

@app.route("/dashboard/<int:division_id>")
@login_required
def dashboard_division(division_id):

    if session["role"] == "admin":
        return redirect("/admin/dashboard")

    if session["role"] == "chef_division" and session["division_id"] != division_id:
        return "Accès interdit", 403
    statut = request.args.get("statut", "")
    priorite = request.args.get("priorite", "")
    recherche = request.args.get("recherche", "")

    connexion = get_db_connection()
    cursor = connexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT nom_division
        FROM divisions
        WHERE id = %s
    """, (division_id,))
    division = cursor.fetchone()

    query = """
        SELECT r.*, d.nom_division, c.nom, c.prenom
        FROM reclamations r
        LEFT JOIN divisions d ON r.division_id = d.id
        LEFT JOIN citoyens c ON r.citoyen_id = c.id
        WHERE r.division_id = %s
    """

    params = [division_id]

    if statut:
        query += " AND r.statut = %s"
        params.append(statut)

    if priorite:
        query += " AND r.priorite = %s"
        params.append(priorite)

    if recherche:
        query += """
            AND (
                r.code_reclamation LIKE %s
                OR r.objet LIKE %s
                OR r.zone LIKE %s
                OR c.nom LIKE %s
                OR c.prenom LIKE %s
            )
        """
        mot = f"%{recherche}%"
        params.extend([mot, mot, mot, mot, mot])

    query += """
        ORDER BY 
            CASE r.priorite
                WHEN 'urgente' THEN 1
                WHEN 'elevee' THEN 2
                WHEN 'moyenne' THEN 3
                WHEN 'faible' THEN 4
                ELSE 5
            END,
            r.date_creation DESC
    """

    cursor.execute(query, params)
    reclamations = cursor.fetchall()
    cursor.execute("""
    SELECT 
        COUNT(*) AS total,

        SUM(CASE WHEN statut = 'nouvelle' THEN 1 ELSE 0 END) AS nouvelles,
        SUM(CASE WHEN statut = 'en_cours' THEN 1 ELSE 0 END) AS en_cours,

        SUM(
            CASE 
                WHEN statut IN ('repondue', 'cloturee')
                THEN 1 ELSE 0
            END
        ) AS repondues,

        SUM(CASE WHEN statut = 'cloturee' THEN 1 ELSE 0 END) AS cloturees,

        /* PRIORITÉS */
        SUM(CASE WHEN priorite = 'urgente' THEN 1 ELSE 0 END) AS priorite_urgente,
        SUM(CASE WHEN priorite = 'elevee' THEN 1 ELSE 0 END) AS priorite_elevee,
        SUM(CASE WHEN priorite = 'moyenne' THEN 1 ELSE 0 END) AS priorite_moyenne,
        SUM(CASE WHEN priorite = 'faible' THEN 1 ELSE 0 END) AS priorite_faible

    FROM reclamations
    WHERE division_id = %s
""", (division_id,))

    stats = cursor.fetchone()

    cursor.close()
    connexion.close()

    return render_template(
    "dashboard_division.html",
    reclamations=reclamations,
    division=division,
    stats=stats,
    division_id=division_id,
    statut=statut,
    priorite=priorite,
    recherche=recherche,
    utilisateur=session
)
@app.route("/exports/<int:division_id>")
@login_required
def exports_division(division_id):

    connexion = get_db_connection()
    cursor = connexion.cursor(dictionary=True)

    # Division
    cursor.execute("""
        SELECT *
        FROM divisions
        WHERE id = %s
    """, (division_id,))
    division = cursor.fetchone()

    # Statistiques
    cursor.execute("""
        SELECT
            COUNT(*) AS total,

            SUM(CASE WHEN statut='nouvelle' THEN 1 ELSE 0 END) AS nouvelles,
            SUM(CASE WHEN statut='en_cours' THEN 1 ELSE 0 END) AS en_cours,
            SUM(CASE WHEN statut='cloturee' THEN 1 ELSE 0 END) AS cloturees,

            SUM(
                CASE
                    WHEN priorite IN ('urgente','elevee')
                    THEN 1 ELSE 0
                END
            ) AS urgentes

        FROM reclamations
        WHERE division_id = %s
    """, (division_id,))

    stats = cursor.fetchone()

    cursor.close()
    connexion.close()

    return render_template(
        "exports.html",
        division=division,
        division_id=division_id,
        stats=stats,
        utilisateur=session
    )
def verifier_acces_division(division_id):
    if session.get("role") == "admin":
        return True

    if session.get("role") == "chef_division" and session.get("division_id") == division_id:
        return True

    return False


def get_reclamations_export(division_id, statut=None, priorite=None, urgentes=False):
    connexion = get_db_connection()
    cursor = connexion.cursor(dictionary=True)

    query = """
        SELECT 
            r.code_reclamation AS Code,
            c.nom AS Nom,
            c.prenom AS Prénom,
            c.cin AS CIN,
            r.zone AS Zone,
            r.objet AS Objet,
            r.description AS Description,
            r.priorite AS Priorité,
            r.score_priorite AS Score,
            r.statut AS Statut,
            r.date_creation AS Date
        FROM reclamations r
        LEFT JOIN citoyens c ON r.citoyen_id = c.id
        WHERE r.division_id = %s
    """

    params = [division_id]

    if urgentes:
        query += " AND r.priorite IN ('urgente', 'elevee') AND r.statut != 'cloturee'"

    if statut:
        query += " AND r.statut = %s"
        params.append(statut)

    if priorite:
        query += " AND r.priorite = %s"
        params.append(priorite)

    query += " ORDER BY r.date_creation DESC"

    cursor.execute(query, params)
    data = cursor.fetchall()

    cursor.close()
    connexion.close()

    return data


@app.route("/exports/<int:division_id>/excel")
@login_required
def export_division_excel(division_id):
    if not verifier_acces_division(division_id):
        return "Accès interdit", 403

    statut = request.args.get("statut", "")
    priorite = request.args.get("priorite", "")

    data = get_reclamations_export(division_id, statut, priorite)

    df = pd.DataFrame(data)

    output = io.BytesIO()
    df.to_excel(output, index=False, sheet_name="Réclamations")
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name=f"reclamations_division_{division_id}.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@app.route("/exports/<int:division_id>/csv")
@login_required
def export_division_csv(division_id):
    if not verifier_acces_division(division_id):
        return "Accès interdit", 403

    statut = request.args.get("statut", "")
    priorite = request.args.get("priorite", "")

    data = get_reclamations_export(division_id, statut, priorite)

    df = pd.DataFrame(data)

    output = io.BytesIO()
    output.write(df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"))
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name=f"reclamations_division_{division_id}.csv",
        mimetype="text/csv"
    )


@app.route("/exports/<int:division_id>/urgentes")
@login_required
def export_division_urgentes(division_id):
    if not verifier_acces_division(division_id):
        return "Accès interdit", 403

    data = get_reclamations_export(division_id, urgentes=True)

    df = pd.DataFrame(data)

    output = io.BytesIO()
    df.to_excel(output, index=False, sheet_name="Urgentes")
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name=f"reclamations_urgentes_division_{division_id}.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@app.route("/exports/<int:division_id>/pdf")
@login_required
def export_division_pdf(division_id):
    if not verifier_acces_division(division_id):
        return "Accès interdit", 403

    statut = request.args.get("statut", "")
    priorite = request.args.get("priorite", "")

    data = get_reclamations_export(division_id, statut, priorite)

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    # Police compatible avec l'arabe
    font_path = r"C:\Windows\Fonts\arial.ttf"
    pdfmetrics.registerFont(TTFont("ArabicFont", font_path))

    pdf.setFont("ArabicFont", 15)
    pdf.drawString(50, 800, "Rapport des réclamations - Division")

    pdf.setFont("ArabicFont", 10)
    pdf.drawString(50, 775, f"Nombre total : {len(data)}")

    y = 745

    for r in data:
        if y < 80:
            pdf.showPage()
            pdf.setFont("ArabicFont", 10)
            y = 800

        zone_pdf = prepare_arabic_text(r["Zone"])

        ligne = f"{r['Code']} | {r['Nom']} {r['Prénom']} | {r['Priorité']} | {r['Statut']} | {zone_pdf}"

        pdf.drawString(50, y, ligne[:120])
        y -= 20

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"rapport_division_{division_id}.pdf",
        mimetype="application/pdf"
    )
@app.route("/reclamation/<int:reclamation_id>")
@login_required
def detail_reclamation(reclamation_id):
    connexion = get_db_connection()
    cursor = connexion.cursor(dictionary=True)

    # Récupération de la réclamation
    cursor.execute("""
        SELECT 
            r.*, 
            c.nom, c.prenom, c.cin, c.telephone, c.email,
            d.nom_division
        FROM reclamations r
        JOIN citoyens c ON r.citoyen_id = c.id
        LEFT JOIN divisions d ON r.division_id = d.id
        WHERE r.id = %s
    """, (reclamation_id,))
    reclamation = cursor.fetchone()

    if not reclamation:
        cursor.close()
        connexion.close()
        return "Réclamation introuvable", 404

    if session["role"] == "admin":
        cursor.close()
        connexion.close()
        return redirect(f"/admin/reclamation/{reclamation_id}")

    if session["role"] == "chef_division" and session["division_id"] != reclamation["division_id"]:
        cursor.close()
        connexion.close()
        return "Accès interdit", 403

    # Liste des autres divisions disponibles pour transfert
    cursor.execute("""
        SELECT id, nom_division
        FROM divisions
        WHERE id != %s
        ORDER BY nom_division ASC
    """, (reclamation["division_id"],))
    divisions = cursor.fetchall()

    # Historique
    cursor.execute("""
        SELECT *
        FROM historique_reclamations
        WHERE reclamation_id = %s
        ORDER BY date_action ASC
    """, (reclamation_id,))
    historique = cursor.fetchall()

    # Réponses
    cursor.execute("""
        SELECT *
        FROM reponses
        WHERE reclamation_id = %s
        ORDER BY date_reponse DESC
    """, (reclamation_id,))
    reponses = cursor.fetchall()

    cursor.close()
    connexion.close()

    return render_template(
    "detail_reclamation.html",
    reclamation=reclamation,
    historique=historique,
    reponses=reponses,
    divisions=divisions,
    utilisateur=session
)
    

@app.route("/repondre/<int:reclamation_id>", methods=["POST"])
@login_required
def repondre_reclamation(reclamation_id):
    message = request.form["message"]
    fichier = request.files.get("fichier_reponse")

    fichier_nom = None

    if fichier and fichier.filename != "":
        fichier_nom = f"reponse_{reclamation_id}_{fichier.filename}"
        chemin = os.path.join(app.config["UPLOAD_FOLDER"], fichier_nom)
        fichier.save(chemin)

    connexion = get_db_connection()
    cursor = connexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT statut
        FROM reclamations
        WHERE id = %s
    """, (reclamation_id,))
    ancienne_reclamation = cursor.fetchone()

    ancien_statut = ancienne_reclamation["statut"] if ancienne_reclamation else "nouvelle"

    utilisateur_id = None

    cursor.execute("""
        INSERT INTO reponses (
            reclamation_id, utilisateur_id, message, fichier_reponse
        )
        VALUES (%s, %s, %s, %s)
    """, (
        reclamation_id,
        utilisateur_id,
        message,
        fichier_nom
    ))

    cursor.execute("""
        UPDATE reclamations
        SET statut = 'repondue'
        WHERE id = %s
    """, (reclamation_id,))

    cursor.execute("""
        INSERT INTO historique_reclamations (
            reclamation_id, action, ancien_statut, nouveau_statut, utilisateur_id
        )
        VALUES (%s, %s, %s, %s, %s)
    """, (
        reclamation_id,
        "Réponse envoyée au citoyen par la division",
        ancien_statut,
        "repondue",
        utilisateur_id
    ))

    connexion.commit()
    cursor.close()
    connexion.close()

    return redirect(f"/reclamation/{reclamation_id}")
@app.route('/admin/divisions')
@login_required
@admin_required
def admin_divisions():
    recherche = request.args.get('recherche', '')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            d.id,
            d.nom_division,
            d.categorie_associee,

            COALESCE(r.total, 0) AS total_reclamations,
            COALESCE(r.nouvelles, 0) AS nouvelles,
            COALESCE(r.en_cours, 0) AS en_cours,
            COALESCE(r.repondues, 0) AS repondues,
            COALESCE(r.cloturees, 0) AS cloturees,

            COALESCE(u.total_chefs, 0) AS total_chefs,
            u.chefs_noms,
            u.chefs_emails

        FROM divisions d

        LEFT JOIN (
            SELECT 
                division_id,
                COUNT(*) AS total,
                SUM(CASE WHEN statut = 'nouvelle' THEN 1 ELSE 0 END) AS nouvelles,
                SUM(CASE WHEN statut = 'en_cours' THEN 1 ELSE 0 END) AS en_cours,
                SUM(CASE WHEN statut = 'repondue' THEN 1 ELSE 0 END) AS repondues,
                SUM(CASE WHEN statut = 'cloturee' THEN 1 ELSE 0 END) AS cloturees
            FROM reclamations
            GROUP BY division_id
        ) r ON r.division_id = d.id

        LEFT JOIN (
            SELECT 
                division_id,
                COUNT(*) AS total_chefs,
                GROUP_CONCAT(nom SEPARATOR ', ') AS chefs_noms,
                GROUP_CONCAT(email SEPARATOR ', ') AS chefs_emails
            FROM utilisateurs
            WHERE role = 'chef_division'
            GROUP BY division_id
        ) u ON u.division_id = d.id

        WHERE 1=1
    """

    params = []

    if recherche:
        query += """
            AND (
                d.nom_division LIKE %s
                OR d.categorie_associee LIKE %s
            )
        """
        mot = f"%{recherche}%"
        params.extend([mot, mot])

    query += " ORDER BY d.nom_division ASC"

    cursor.execute(query, params)
    divisions = cursor.fetchall()

    total_divisions = len(divisions)
    total_reclamations = sum(d["total_reclamations"] or 0 for d in divisions)
    total_chefs = sum(d["total_chefs"] or 0 for d in divisions)
    total_cloturees = sum(d["cloturees"] or 0 for d in divisions)

    taux_cloture = round((total_cloturees / total_reclamations) * 100, 1) if total_reclamations > 0 else 0

    cursor.close()
    conn.close()

    return render_template(
        'admin_divisions.html',
        divisions=divisions,
        total_divisions=total_divisions,
        total_reclamations=total_reclamations,
        total_chefs=total_chefs,
        total_cloturees=total_cloturees,
        taux_cloture=taux_cloture,
        recherche=recherche,
        utilisateur=session
    )

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/cloturer/<int:reclamation_id>", methods=["POST"])
@login_required
def cloturer_reclamation(reclamation_id):
    connexion = get_db_connection()
    cursor = connexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT statut
        FROM reclamations
        WHERE id = %s
    """, (reclamation_id,))
    reclamation = cursor.fetchone()

    ancien_statut = reclamation["statut"]

    cursor.execute("""
        UPDATE reclamations
        SET statut = 'cloturee'
        WHERE id = %s
    """, (reclamation_id,))

    cursor.execute("""
        INSERT INTO historique_reclamations (
            reclamation_id, action, ancien_statut, nouveau_statut, utilisateur_id
        )
        VALUES (%s, %s, %s, %s, %s)
    """, (
        reclamation_id,
        "Réclamation clôturée par la commune après traitement",
        ancien_statut,
        "cloturee",
        None
    ))

    connexion.commit()
    cursor.close()
    connexion.close()

    return redirect(f"/reclamation/{reclamation_id}")

@app.route("/transferer/<int:reclamation_id>", methods=["POST"])
@login_required
def transferer_reclamation(reclamation_id):
    nouvelle_division_id = request.form["nouvelle_division_id"]
    motif = request.form["motif"]

    connexion = get_db_connection()
    cursor = connexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT r.division_id, r.statut, r.est_transferee,
               d.nom_division AS ancienne_division_nom
        FROM reclamations r
        LEFT JOIN divisions d ON r.division_id = d.id
        WHERE r.id = %s
    """, (reclamation_id,))
    reclamation = cursor.fetchone()

    if not reclamation:
        cursor.close()
        connexion.close()
        return "Réclamation introuvable", 404
    

    if reclamation["statut"] in ["repondue", "cloturee"]:
        cursor.close()
        connexion.close()
        return "Impossible de transférer une réclamation déjà répondue ou clôturée", 400

    if reclamation["est_transferee"] == 1:
        cursor.close()
        connexion.close()
        return "Cette réclamation a déjà été transférée", 400

    ancienne_division_id = reclamation["division_id"]
    ancien_statut = reclamation["statut"]

    cursor.execute("""
        SELECT nom_division
        FROM divisions
        WHERE id = %s
    """, (nouvelle_division_id,))
    nouvelle_division = cursor.fetchone()

    if not nouvelle_division:
        cursor.close()
        connexion.close()
        return "Division introuvable", 404

    cursor.execute("""
        UPDATE reclamations
        SET division_id = %s,
            statut = 'nouvelle',
            est_transferee = 1
        WHERE id = %s
    """, (nouvelle_division_id, reclamation_id))

    action = f"Réclamation transférée de {reclamation['ancienne_division_nom']} vers {nouvelle_division['nom_division']}"

    cursor.execute("""
        INSERT INTO historique_reclamations (
            reclamation_id, action, ancien_statut, nouveau_statut,
            ancienne_division, nouvelle_division, utilisateur_id, commentaire
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        reclamation_id,
        action,
        ancien_statut,
        "nouvelle",
        ancienne_division_id,
        nouvelle_division_id,
        None,
        motif
    ))

    connexion.commit()
    cursor.close()
    connexion.close()

    return redirect(f"/dashboard/{ancienne_division_id}")

@app.route("/login", methods=["GET", "POST"])
def login():
    erreur = None

    if request.method == "POST":
        email = request.form["email"]
        mot_de_passe = request.form["mot_de_passe"]

        connexion = get_db_connection()
        cursor = connexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM utilisateurs WHERE email = %s", (email,))
        utilisateur = cursor.fetchone()

        cursor.close()
        connexion.close()
        # Vérification si le compte est désactivé
        if utilisateur and utilisateur.get("actif") == 0:
            erreur = "Votre compte est désactivé. Veuillez contacter l'administrateur."
            return render_template("login.html", erreur=erreur)

        if utilisateur and check_password_hash(utilisateur["mot_de_passe"], mot_de_passe):
            session["user_id"] = utilisateur["id"]
            session["nom"] = utilisateur["nom"]
            session["role"] = utilisateur["role"]
            session["division_id"] = utilisateur["division_id"]

            if utilisateur["doit_changer_mot_de_passe"] == 1:
                return redirect("/changer-mot-de-passe")

            if utilisateur["role"] == "chef_division":
                return redirect(f"/dashboard/{utilisateur['division_id']}")

            if utilisateur["role"] == "admin":
                return redirect("/admin/dashboard")

        erreur = "Email ou mot de passe incorrect."

    return render_template("login.html", erreur=erreur)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login") 

@app.route("/changer-mot-de-passe", methods=["GET", "POST"])
@login_required
def changer_mot_de_passe():
    erreur = None
    succes = None

    if request.method == "POST":
        nouveau = request.form["nouveau_mot_de_passe"]
        confirmation = request.form["confirmation"]

        if nouveau != confirmation:
            erreur = "Les mots de passe ne correspondent pas."
        elif len(nouveau) < 6:
            erreur = "Le mot de passe doit contenir au moins 6 caractères."
        else:
            mot_de_passe_hash = generate_password_hash(nouveau)

            connexion = get_db_connection()
            cursor = connexion.cursor()

            cursor.execute("""
                UPDATE utilisateurs
                SET mot_de_passe = %s,
                    doit_changer_mot_de_passe = 0
                WHERE id = %s
            """, (mot_de_passe_hash, session["user_id"]))

            connexion.commit()
            cursor.close()
            connexion.close()

            succes = "Mot de passe modifié avec succès."

            if session["role"] == "chef_division":
                return redirect(f"/dashboard/{session['division_id']}")

    return render_template("changer_mot_de_passe.html", erreur=erreur, succes=succes)

@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    date_debut = request.args.get('date_debut')
    date_fin = request.args.get('date_fin')

    where_date = ""
    params = []

    if date_debut and date_fin:
        where_date = " WHERE date_creation BETWEEN %s AND %s "
        params = [date_debut + " 00:00:00", date_fin + " 23:59:59"]

    connexion = get_db_connection()
    cursor = connexion.cursor(dictionary=True)

    cursor.execute(f"""
        SELECT 
            COUNT(*) AS total,
            SUM(CASE WHEN statut = 'nouvelle' THEN 1 ELSE 0 END) AS nouvelles,
            SUM(CASE WHEN statut = 'en_cours' THEN 1 ELSE 0 END) AS en_cours,
            SUM(CASE WHEN statut = 'repondue' OR statut = 'cloturee' THEN 1 ELSE 0 END) AS repondues,
            SUM(CASE WHEN statut = 'cloturee' THEN 1 ELSE 0 END) AS cloturees,
            SUM(CASE WHEN priorite = 'urgente' THEN 1 ELSE 0 END) AS urgentes,
            SUM(CASE WHEN est_transferee = 1 THEN 1 ELSE 0 END) AS transferees
        FROM reclamations
        {where_date}
    """, params)

    stats = cursor.fetchone()

    if stats is None:
        stats = {
            "total": 0,
            "nouvelles": 0,
            "en_cours": 0,
            "repondues": 0,
            "cloturees": 0,
            "urgentes": 0,
            "transferees": 0
        }

    where_date_join = ""
    params_join = []

    if date_debut and date_fin:
        where_date_join = """
            AND r.date_creation BETWEEN %s AND %s
        """
        params_join = [date_debut + " 00:00:00", date_fin + " 23:59:59"]

    cursor.execute(f"""
        SELECT 
            d.nom_division,
            COUNT(r.id) AS total,
            SUM(CASE WHEN r.statut = 'nouvelle' THEN 1 ELSE 0 END) AS nouvelles,
            SUM(CASE WHEN r.statut = 'en_cours' THEN 1 ELSE 0 END) AS en_cours,
            SUM(CASE WHEN r.statut = 'repondue' OR r.statut = 'cloturee' THEN 1 ELSE 0 END) AS repondues,
            SUM(CASE WHEN r.statut = 'cloturee' THEN 1 ELSE 0 END) AS cloturees
        FROM divisions d
        LEFT JOIN reclamations r 
            ON r.division_id = d.id
            {where_date_join}
        GROUP BY d.id, d.nom_division
        ORDER BY d.nom_division ASC
    """, params_join)

    stats_divisions = cursor.fetchall()

    labels_divisions = []
    data_total = []
    data_cloturees = []

    for d in stats_divisions:
        labels_divisions.append(d["nom_division"])
        data_total.append(d["total"] or 0)
        data_cloturees.append(d["cloturees"] or 0)

    total = stats["total"] or 0
    cloturees = stats["cloturees"] or 0

    taux_cloture = round((cloturees / total) * 100, 2) if total > 0 else 0

    cursor.close()
    connexion.close()

    return render_template(
        "admin_dashboard.html",
        stats=stats,
        stats_divisions=stats_divisions,
        labels_divisions=labels_divisions,
        data_total=data_total,
        data_cloturees=data_cloturees,
        taux_cloture=taux_cloture,
        utilisateur=session,
        date_debut=date_debut,
        date_fin=date_fin
    )

@app.route('/admin/utilisateurs')
@login_required
@admin_required
def admin_utilisateurs():
    recherche = request.args.get('recherche', '')
    role = request.args.get('role', '')
    division_id = request.args.get('division_id', '')
    statut = request.args.get('statut', '')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            u.id,
            u.nom,
            u.email,
            u.role,
            u.division_id,
            u.doit_changer_mot_de_passe,
            u.actif,
            d.nom_division
        FROM utilisateurs u
        LEFT JOIN divisions d ON u.division_id = d.id
        WHERE 1=1
    """
    params = []

    if recherche:
        query += " AND (u.nom LIKE %s OR u.email LIKE %s OR d.nom_division LIKE %s)"
        params.extend([f"%{recherche}%", f"%{recherche}%", f"%{recherche}%"])

    if role:
        query += " AND u.role = %s"
        params.append(role)

    if division_id:
        query += " AND u.division_id = %s"
        params.append(division_id)

    if statut != '':
        query += " AND u.actif = %s"
        params.append(statut)

    query += " ORDER BY u.id DESC"

    cursor.execute(query, params)
    utilisateurs = cursor.fetchall()

    cursor.execute("SELECT * FROM divisions ORDER BY nom_division")
    divisions = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) AS total FROM utilisateurs")
    total_utilisateurs = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM utilisateurs WHERE role = 'chef_division'")
    total_chefs = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM utilisateurs WHERE role = 'admin'")
    total_admins = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM utilisateurs WHERE actif = 1")
    total_actifs = cursor.fetchone()["total"]

    cursor.close()
    conn.close()

    return render_template(
        'admin_utilisateurs.html',
        utilisateurs=utilisateurs,
        divisions=divisions,
        total_utilisateurs=total_utilisateurs,
        total_chefs=total_chefs,
        total_admins=total_admins,
        total_actifs=total_actifs,
        recherche=recherche,
        role=role,
        division_id=division_id,
        statut=statut
    )

@app.route('/admin/utilisateurs/ajouter', methods=['POST'])
@login_required
@admin_required
def ajouter_utilisateur():
    nom = request.form.get('nom')
    email = request.form.get('email')
    role = request.form.get('role')
    division_id = request.form.get('division_id') or None
    mot_de_passe = request.form.get('mot_de_passe')

    mot_de_passe_hash = generate_password_hash(mot_de_passe)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO utilisateurs 
        (nom, email, mot_de_passe, role, division_id, doit_changer_mot_de_passe, actif)
        VALUES (%s, %s, %s, %s, %s, 1, 1)
    """, (nom, email, mot_de_passe_hash, role, division_id))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Utilisateur ajouté avec succès.", "success")
    return redirect(url_for('admin_utilisateurs'))


@app.route('/admin/utilisateurs/reset/<int:id>', methods=['POST'])
@login_required
@admin_required
def reset_mot_de_passe(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT u.id, d.nom_division
        FROM utilisateurs u
        LEFT JOIN divisions d ON u.division_id = d.id
        WHERE u.id = %s
    """, (id,))
    user = cursor.fetchone()

    if user and user["nom_division"]:
        division_clean = user["nom_division"].replace("Division ", "").replace(" ", "")
        nouveau_mdp = division_clean + "123"
    else:
        nouveau_mdp = "Admin123"

    nouveau_mdp_hash = generate_password_hash(nouveau_mdp)

    cursor.execute("""
        UPDATE utilisateurs
        SET mot_de_passe = %s, doit_changer_mot_de_passe = 1
        WHERE id = %s
    """, (nouveau_mdp_hash, id))

    conn.commit()
    cursor.close()
    conn.close()

    flash(f"Mot de passe réinitialisé : {nouveau_mdp}", "success")
    return redirect(url_for('admin_utilisateurs'))


@app.route('/admin/utilisateurs/desactiver/<int:id>', methods=['POST'])
@login_required
@admin_required
def desactiver_utilisateur(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE utilisateurs
        SET actif = 0
        WHERE id = %s
    """, (id,))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Compte désactivé avec succès.", "success")
    return redirect(url_for('admin_utilisateurs'))


@app.route('/admin/utilisateurs/activer/<int:id>', methods=['POST'])
@login_required
@admin_required
def activer_utilisateur(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE utilisateurs
        SET actif = 1
        WHERE id = %s
    """, (id,))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Compte activé avec succès.", "success")
    return redirect(url_for('admin_utilisateurs'))

@app.route('/admin/utilisateurs/statut/<int:id>', methods=['POST'])
@login_required
@admin_required
def changer_statut_utilisateur(id):
    actif = request.form.get('actif')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE utilisateurs
        SET actif = %s
        WHERE id = %s
    """, (actif, id))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Statut du compte modifié avec succès.", "success")
    return redirect(url_for('admin_utilisateurs'))
@app.route('/admin/reclamations')
@login_required
@admin_required
def admin_reclamations():
    recherche = request.args.get('recherche', '')
    statut = request.args.get('statut', '')
    priorite = request.args.get('priorite', '')
    division_id = request.args.get('division_id', '')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            r.*,
            c.nom,
            c.prenom,
            c.cin,
            d.nom_division
        FROM reclamations r
        LEFT JOIN citoyens c ON r.citoyen_id = c.id
        LEFT JOIN divisions d ON r.division_id = d.id
        WHERE 1=1
    """
    params = []

    if recherche:
        query += """
            AND (
                r.code_reclamation LIKE %s
                OR c.nom LIKE %s
                OR c.prenom LIKE %s
                OR r.zone LIKE %s
                OR r.objet LIKE %s
            )
        """
        mot = f"%{recherche}%"
        params.extend([mot, mot, mot, mot, mot])

    if statut:
        query += " AND r.statut = %s"
        params.append(statut)

    if priorite:
        query += " AND r.priorite = %s"
        params.append(priorite)

    if division_id:
        query += " AND r.division_id = %s"
        params.append(division_id)

    query += " ORDER BY r.date_creation DESC"

    cursor.execute(query, params)
    reclamations = cursor.fetchall()

    cursor.execute("SELECT * FROM divisions ORDER BY nom_division")
    divisions = cursor.fetchall()

    cursor.execute("""
        SELECT 
            COUNT(*) AS total,
            SUM(CASE WHEN statut = 'nouvelle' THEN 1 ELSE 0 END) AS nouvelles,
            SUM(CASE WHEN statut = 'en_cours' THEN 1 ELSE 0 END) AS en_cours,
            SUM(CASE WHEN statut = 'repondue' THEN 1 ELSE 0 END) AS repondues,
            SUM(CASE WHEN statut = 'cloturee' THEN 1 ELSE 0 END) AS cloturees
        FROM reclamations
    """)
    stats = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        'admin_reclamations.html',
        reclamations=reclamations,
        divisions=divisions,
        stats=stats,
        recherche=recherche,
        statut=statut,
        priorite=priorite,
        division_id=division_id
    )

@app.route("/admin/reclamation/<int:reclamation_id>")
@admin_required
def admin_detail_reclamation(reclamation_id):
    connexion = get_db_connection()
    cursor = connexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            r.*, 
            c.nom, c.prenom, c.cin, c.telephone, c.email,
            d.nom_division
        FROM reclamations r
        JOIN citoyens c ON r.citoyen_id = c.id
        LEFT JOIN divisions d ON r.division_id = d.id
        WHERE r.id = %s
    """, (reclamation_id,))
    reclamation = cursor.fetchone()

    if not reclamation:
        cursor.close()
        connexion.close()
        return "Réclamation introuvable", 404

    cursor.execute("""
        SELECT id, nom_division FROM divisions
        WHERE id != %s ORDER BY nom_division ASC
    """, (reclamation["division_id"],))
    divisions = cursor.fetchall()

    cursor.execute("""
        SELECT * FROM historique_reclamations
        WHERE reclamation_id = %s ORDER BY date_action ASC
    """, (reclamation_id,))
    historique = cursor.fetchall()

    cursor.execute("""
        SELECT * FROM reponses
        WHERE reclamation_id = %s ORDER BY date_reponse DESC
    """, (reclamation_id,))
    reponses = cursor.fetchall()

    cursor.close()
    connexion.close()

    return render_template(
        "admin_detail_reclamation.html",
        reclamation=reclamation,
        historique=historique,
        reponses=reponses,
        divisions=divisions,
        utilisateur=session
    )

@app.route('/admin/exports')
@login_required
@admin_required
def admin_exports():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM reclamations")
    total_reclamations = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM reclamations WHERE statut = 'cloturee'")
    total_cloturees = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM divisions")
    total_divisions = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM utilisateurs WHERE role = 'chef_division'")
    total_chefs = cursor.fetchone()["total"]

    cursor.close()
    conn.close()

    return render_template(
        "admin_exports.html",
        total_reclamations=total_reclamations,
        total_cloturees=total_cloturees,
        total_divisions=total_divisions,
        total_chefs=total_chefs,
        utilisateur=session
    )


@app.route('/admin/exports/reclamations/excel')
@login_required
@admin_required
def export_reclamations_excel():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            r.code_reclamation AS Code,
            c.nom AS Nom,
            c.prenom AS Prénom,
            c.cin AS CIN,
            r.zone AS Zone,
            r.objet AS Objet,
            r.description AS Description,
            d.nom_division AS Division,
            r.priorite AS Priorité,
            r.score_priorite AS Score,
            r.statut AS Statut,
            r.date_creation AS Date
        FROM reclamations r
        LEFT JOIN citoyens c ON r.citoyen_id = c.id
        LEFT JOIN divisions d ON r.division_id = d.id
        ORDER BY r.date_creation DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    df = pd.DataFrame(data)

    output = io.BytesIO()
    df.to_excel(output, index=False, sheet_name="Réclamations")
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="reclamations_commune.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@app.route('/admin/exports/reclamations/pdf')
@login_required
@admin_required
def export_reclamations_pdf():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            r.code_reclamation,
            c.nom,
            c.prenom,
            r.objet,
            r.statut,
            r.priorite,
            d.nom_division,
            r.date_creation
        FROM reclamations r
        LEFT JOIN citoyens c ON r.citoyen_id = c.id
        LEFT JOIN divisions d ON r.division_id = d.id
        ORDER BY r.date_creation DESC
    """)

    reclamations = cursor.fetchall()

    cursor.close()
    conn.close()

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 800, "Rapport des réclamations - Commune de Kénitra")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 775, f"Nombre total : {len(reclamations)}")

    y = 745

    for r in reclamations:
        if y < 80:
            pdf.showPage()
            y = 800
            pdf.setFont("Helvetica", 10)

        ligne = f"{r['code_reclamation']} | {r['nom']} {r['prenom']} | {r['priorite']} | {r['statut']} | {r['nom_division'] or '-'}"
        pdf.drawString(50, y, ligne[:115])
        y -= 20

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="reclamations_commune.pdf",
        mimetype="application/pdf"
    )
def prepare_arabic_text(text):
    if not text:
        return ""

    text = str(text)

    if contient_arabe(text):
        reshaped_text = arabic_reshaper.reshape(text)
        return get_display(reshaped_text)

    return text
if __name__ == "__main__":
    app.run(debug=True, port=5001)