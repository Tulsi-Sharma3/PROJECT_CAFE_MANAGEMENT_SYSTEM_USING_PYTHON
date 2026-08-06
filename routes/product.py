# FOR LOGIN SYSTEM:
# from flask import Blueprint, render_template

# product = Blueprint("product", __name__)


# @product.route("/products")
# def products():
#     return render_template("products.html")

from flask import Blueprint, render_template, request, redirect
from database.db import get_connection

product = Blueprint("product", __name__)

@product.route("/products")
def products():

    search = request.args.get("search")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if search:
        cursor.execute(
            """
            SELECT * FROM products
            WHERE product_name LIKE %s
            """,
            ("%" + search + "%",)
        )
    else:
        cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "products.html",
        products=products,
        search=search
    )
    # connection = get_connection()
    # cursor = connection.cursor(dictionary=True)

    # cursor.execute("SELECT * FROM products")

    # products = cursor.fetchall()

    # cursor.close()
    # connection.close()

    # return render_template("products.html", products=products)


@product.route("/add-product", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":

        product_name = request.form["product_name"]
        category = request.form["category"]
        price = request.form["price"]
        stock = request.form["stock"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO products
            (product_name, category, price, stock)
            VALUES (%s,%s,%s,%s)
        """, (product_name, category, price, stock))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/products")

    return render_template("add_product.html")

@product.route("/delete-product/<int:id>")
def delete_product(id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM products WHERE id=%s",
        (id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/products")

@product.route("/edit-product/<int:id>", methods=["GET", "POST"])
def edit_product(id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        product_name = request.form["product_name"]
        category = request.form["category"]
        price = request.form["price"]
        stock = request.form["stock"]

        cursor.execute("""
            UPDATE products
            SET product_name=%s,
                category=%s,
                price=%s,
                stock=%s
            WHERE id=%s
        """, (product_name, category, price, stock, id))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/products")

    cursor.execute("SELECT * FROM products WHERE id=%s", (id,))
    product_data = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template("edit_product.html", product=product_data)