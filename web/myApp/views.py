from flask import Flask, render_template
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
@app.route("/signin")
def signin():
    return render_template("signin.html")
@app.route("/signup")
def signup():
    return render_template("signup.html")



