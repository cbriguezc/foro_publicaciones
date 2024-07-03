from flask_app.config.mysqlconnection import connectToMySQL #me ayuda a conectarme con mi base de datos

from flask import flash #me ayuda a tener mensajes de flash para crear una validacion

class Post:

    def __init__(self, data):
        #data sera un diccionario con mi info de mi base de ddatos
        self.id = data["id"]
        self.content = data["content"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

        self.user_name = data["user_name"]

    #asi creamos un metodo para guardar una nueva publicacion 
    @classmethod
    def save(cls, form):
        query = "INSERT INTO posts(content, user_id) VALUES (%(content)s, %(user_id)s)"
        return connectToMySQL("foro_publicaciones").query_db(query, form)
    
    @staticmethod
    def validate_post(form):
        is_valid = True

        if len(form["content"]) < 1:
            flash("Post content is required.", "post")
            is_valid = False

        return is_valid
    
    @classmethod
    def get_all(cls):
        query = "SELECT posts.*, users.first_name as user_name FROM posts JOIN users ON posts.user_id = users.id ORDER BY created_at DESC"
        results = connectToMySQL("foro_publicaciones").query_db(query)
        posts = []
        for post in results:
            posts.append(cls(post))
        return posts

    @classmethod
    def delete(cls, data):
        #data hace que tenga un diccionario con la identificacion que quiero
        query = "DELETE FROM posts WHERE id = %(id)s"
        connectToMySQL("foro_publicaciones").query_db(query, data) #necesito data porque nos dice de donde va a sacar la informacion