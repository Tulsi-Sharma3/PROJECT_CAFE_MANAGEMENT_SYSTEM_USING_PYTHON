# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "<h1>Welcome to Smart Cafe Management System</h1>"

# if __name__ == "__main__":
#     app.run(debug=True)

# UPDATE:
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
