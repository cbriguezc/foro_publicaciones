# hacer la importacion de la conexion con mi base de datos
from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash #flash es el encargado de mostrar los mensajes

import re #expresiones regulares, buscamos empatar con un patron de texto
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #Expresion regular de email

#la clase siempre va con la primera mayuscula y en singular
class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    #metodo que crea y guarda un nuevo registro - registro
    @classmethod
    def save(cls, form):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUE (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL("foro_publicaciones").query_db(query, form) # va a regresar el id del nuevo registro
    
    #metodo que regresa objeto de usuraio en base a e-mail - inicio de sesion
    @classmethod
    def get_by_email(cls, form):
        #form = {"email": "elena@cd.com", "password": "hola123"}
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL("foro_publicaciones").query_db(query, form)

        if len(result) < 1:
            return False
        else:
            user = cls(result[0])
            return user
    
    #metodo  que valida la informacion que recibimos del form
    @staticmethod
    def validate_user(form):
        #form= {diccionario con toda la info del formulario}
        is_valid = True #inocente hasta demostrar lo contrario, el formulario esta valido hasta este punto, más abajo se ponen las condiciones para ver si es correcto o no, si una de esas condiciones no es correcta, ya no va a ser valido.

        #validamos que el nombre tenga al menos dos caracteres
        if len(form["first_name"]) < 2:
            flash("first_name must have at least 2 chars", "register") #(mensaje, categoria )
            is_valid = False

        #validamos que el apellido tenga al menos dos caracteres
        if len(form["last_name"]) < 2:
            flash("last_name must have at least 2 chars", "register")
            is_valid = False

        #validamos que el password tenga al menos dos caracteres
        if len(form["password"]) < 6:
            flash("password must have at least 2 chars", "register")
            is_valid = False

        #validar que el correo sea unico
        query = "SELECT *FROM users WHERE email = %(email)s"
        result = connectToMySQL("foro_publicaciones").query_db(query, form) #lista de diccionario
        #lista vacia o lista con 1 diccionario
        if len(result) >= 1: 
            flash("e-mail already registered", "register")
            is_valid = False
        
        #verificamos que las contraseñas coincidan
        if form["password"] != form["confirm"]: #diferente de -> !=
            flash("password do not match", "register")
            is_valid = False
        
        #validar que el email tenga el formato correcto
        if not EMAIL_REGEX.match(form["email"]): #match compara una expresion regular con un texto
            flash("e-mail not valid", "register")
            is_valid = False

        return is_valid
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('foro_publicaciones').query_db(query, data)
        user = cls(result[0])
        return user