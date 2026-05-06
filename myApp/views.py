from flask import Flask, render_template,request, redirect, session, url_for
import mysql.connector
from myApp.config import DB_SERVER

app =Flask(__name__)
app.template_folder="template"
app.static_folder="static"
app.layout_folder="layout"
app.config.from_object("myApp.config")


def get_db_connection():
    return mysql.connector.connect(**DB_SERVER)


def get_flashcard_banks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT c.idcategorie AS id,
               c.nomcategorie AS name,
               COUNT(carte.idcarte) AS card_count
        FROM categorie c
        LEFT JOIN carte ON carte.idcategorie = c.idcategorie
        GROUP BY c.idcategorie, c.nomcategorie
        ORDER BY c.nomcategorie
        """
    )
    banks = cursor.fetchall()
    cursor.close()
    conn.close()
    return banks


def get_flashcards_by_bank(bank_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT c.idcarte AS id,
               c.question,
               c.reponse,
               cat.nomcategorie AS category_name
        FROM carte c
        INNER JOIN categorie cat ON cat.idcategorie = c.idcategorie
        WHERE cat.idcategorie = %s
        ORDER BY c.idcarte
        """,
        (bank_id,)
    )
    cards = cursor.fetchall()
    cursor.close()
    conn.close()
    return cards

@app.route("/")

def index():
    return render_template("index.html")


@app.route("/banques")
def banques():
    error = None
    banks = []
    try:
        banks = get_flashcard_banks()
    except Exception:
        error = "Impossible de charger les banques de flashcards pour le moment."
    return render_template("banques.html", banks=banks, error=error)


@app.route("/banques/<int:bank_id>")
def banque_detail(bank_id):
    error = None
    banks = []
    cards = []
    selected_bank = None
    try:
        banks = get_flashcard_banks()
        selected_bank = next((bank for bank in banks if bank["id"] == bank_id), None)
        cards = get_flashcards_by_bank(bank_id)
    except Exception:
        error = "Impossible d'afficher cette banque pour le moment."
    return render_template(
        "banques.html",
        banks=banks,
        cards=cards,
        selected_bank=selected_bank,
        error=error,
    )

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        # Vérifier dans la base de données (à connecter après)
        # Pour l'instant on peut tester avec des valeurs fixes :
        if email == "test@test.com" and password == "1234":
            session["user"] = email
            return redirect("/")
        else:
            return render_template("signin.html", error="Identifiants incorrects")
    
    return render_template("signin.html")
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        statut = request.form["statut"]

        # Vérifier que les mots de passe correspondent
        if password != confirm_password:
            return render_template("signup.html", error="Les mots de passe ne correspondent pas")

        # Vérifier que les champs obligatoires sont remplis
        if not email or not password:
            return render_template("signup.html", error="Email et mot de passe obligatoires")

        # Insérer dans la base de données
        try:
            conn = mysql.connector.connect(**DB_SERVER)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)",
                (firstname, lastname, email, password)
            )
            conn.commit()
            conn.close()
            return render_template("signup.html", success="Compte créé avec succès ! Vous pouvez vous connecter.")
        except:
            return render_template("signup.html", error="Cet email est déjà utilisé")

    return render_template("signup.html")


def get_user(email, password):
    conn = mysql.connector.connect(**DB_SERVER)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

@app.route("/team/camille")
def team_camille():
    return render_template("team/camille.html")

@app.route("/team/etienne")
def team_etienne():
    return render_template("team/etienne.html")

@app.route("/team/luka")
def team_luka():
    return render_template("team/luka.html")

@app.route("/team/darya")
def team_darya():
    return render_template("team/darya.html")