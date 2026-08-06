from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import check_password_hash
from database.db import get_connection


auth = Blueprint("auth", __name__)


@auth.route("/")
def home():
    return redirect("/login")


@auth.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE username=%s",
            (username,)
        )


        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:

            if check_password_hash(user["password"], password):

                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["role"] = user["role"]

                return redirect("/dashboard")


        return "Invalid Username or Password"


    return render_template("login.html")



@auth.route("/logout")
def logout():

    session.clear()

    return redirect("/login")