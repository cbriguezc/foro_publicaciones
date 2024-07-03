from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app

#importamos un modelo
from flask_app.models.users import User 
from flask_app.models.post import Post

#importar bcrypt 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#plantilla que muestra formularios 
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=['post'])
def register():

    #validar la info
    if not User.validate_user(request.form):
        #si no es valida la informacion, regresa al formurio(pagina principal)
        return redirect("/")
    
    #encriptar o hashear contraseña
    pass_hash = bcrypt.generate_password_hash(request.form["password"])

    #crear un diccionario que simule un form, incluyendo la contraseña hasheada
    form = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pass_hash
    }
    #creo una variable
    id = User.save(form) #recibo el id del nuevo usuario
    session["user_id"] = id #guardamos en sesion el ID del usuario
    return redirect("/dashboard") 

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect("/")
    
    dicc = {"id": session['user_id']}
    user = User.get_by_id(dicc)

    #pend: enviar todas las publicaciones, para que se muestren en la pagina principal
    posts = Post.get_all()

    return render_template("dashboard.html", user=user, posts=posts)

@app.route("/login", methods=['post'])
def login():
    #verificar que el email este en mi base de datos
    user = User.get_by_email(request.form) #dos opciones, recibo False si no existe ese usuario en mi bs o recibo un objeto de Usuario si es que si existe

    if not user: #si user es False
        flash("E-mail not found", "login")
        return redirect("/")
    
    #si user si es objeto user, es decir, valido
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("password incorrect", "login")
        return redirect("/")
    
    session["user_id"] = user.id
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

#cuando quiero acceder a un objeto uso un punto -> user.id
#cuando quiero usar un diccionario, va en corchetes -> session["user_id"]
#cuando es una lista, va en corchetes -> result [0]

