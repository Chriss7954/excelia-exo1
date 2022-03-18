from difflib import ndiff
from bottle import route, run, template, request, response, redirect, abort
import sqlite3
import random
from helpers import generate_cookie_value, somme



@route('/hello/<name>')
def index(name="Elsa"):
    response.set_cookie("my_value",name, path="/")
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/index/')
def index():
    cookie_name = request.get_cookie("my_value")
    return template('<b>Hello {{retrieve_name}}</b>!', retrieve_name=cookie_name)

@route('/signup', method=["GET","POST"])
@route('/signup/', method=["GET","POST"])
def signup():
    if request.method=="GET":
        return template("signup_template")
    else:
        username = request.forms.username
        email = request.forms.email
        password = request.forms.password
        print(username)
        print(email)
        print(password)
        conn = sqlite3.connect('fb.db')
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO facebook (username, email, password) VALUES ('{username}', '{email}', '{password}')")
        conn.commit()
        return{
            "error": False,
            "message": f"Bien enregistré en tant que {username} id: {cursor.lastrowid}",
        }

@route('/login', method=["GET","POST"])
@route('/login/', method=["GET","POST"])
def login():
    if request.method=="GET":
        return template("login_template")
    else:
        username = request.forms.username
        password = request.forms.password

        conn = sqlite3.connect('fb.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT password FROM facebook WHERE username ='{username}'")
        db_password = cursor.fetchone()
        print(db_password)
        if(db_password[0] ==""):
            return {"error": True, "message":"Utilisateur inconnu"}
        if(db_password[0] != password):
            return {"error": True, "message":"Mot de passe erroné"}

        cookie_value = generate_cookie_value()

        cursor.execute(f"UPDATE facebook SET cookie = '{cookie_value}' WHERE username = '{username}'")
        conn.commit()

        response.set_cookie("fb_session", cookie_value, path="/")
        redirect("/user/")



@route('/user', method=["GET","POST"])
@route('/user/', method=["GET","POST"])
def user_info():
    fb_session = request.get_cookie('fb_session')

    conn = sqlite3.connect('fb.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM facebook WHERE cookie ='{fb_session}'")
    result = cursor.fetchone()

    if result is None:
        abort(404, "Déso, t'es pas sur la liste ")
    return template("user_info", username=result[1],email=result[2])




@route('/addition/<a>/<b>')
def addition(a="0", b="0"):
    
    res = somme(a, b)
    return template('<b>Hello {{res}}</b>!', res=res)
    



    
    


run(host='localhost', port=8080, reloader=True)