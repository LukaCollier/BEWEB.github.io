from flask import Flask, render_template,request, redirect, session
import mysql.connector
from myApp.config import DB_SERVER

app =Flask(__name__)
app.template_folder="template"
app.static_folder="static"
app.layout_folder="layout"
app.config.from_object("myApp.config")

@app.route("/")

def index():
    return render_template("index.html")

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