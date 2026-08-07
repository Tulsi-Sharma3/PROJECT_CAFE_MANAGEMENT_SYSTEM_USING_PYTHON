# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "<h1>Welcome to Smart Cafe Management System</h1>"

# if __name__ == "__main__":
#     app.run(debug=True)

# UPDATE:
# from flask import Flask, render_template

# app = Flask(__name__)


# @app.route("/")
# def login():
#     return render_template("login.html")


# @app.route("/dashboard")
# def dashboard():
#     return render_template("dashboard.html")


# if __name__ == "__main__":
#     app.run(debug=True)

# UPDATE:
from flask import Flask,render_template,session, redirect
from routes.auth import auth
from routes.product import product
from routes.customer import customer
from routes.order import order

app=Flask(__name__)

app.secret_key="REMOVED"


app.register_blueprint(auth)
app.register_blueprint(product)
app.register_blueprint(customer)
app.register_blueprint(order)

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login") 
       
    return render_template("dashboard.html")


if __name__=="__main__":
    app.run(debug=True)