#en terminal poner: python3 -m pipenv install flask pymysql flask-bcrypt. en la carpeta de tu proyecto se debe hacer esta instalacion no en flask_app

#Importar la app
from flask_app import app

#Importar controladores (puede ser más de uno)
from flask_app.controllers import users_controller
from flask_app.controllers import posts_controller

#Ejecución app
if __name__ == "__main__":
    app.run(debug=True)

