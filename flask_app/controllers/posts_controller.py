from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app

from flask_app.models.post import Post

@app.route("/create_post", methods=['post'])
def create_post():
    if not Post.validate_post(request.form):
        return redirect("/dashboard")
    
    Post.save(request.form)
    return redirect("/dashboard")

@app.route("/delete_post/<int:id>")
def delete_post(id):
    #metodo que borra un registro en base a su id
    dicc = {"id":id}
    Post.delete(dicc)
    
    return redirect("/dashboard")