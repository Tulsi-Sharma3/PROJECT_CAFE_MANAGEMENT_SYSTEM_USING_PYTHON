from flask import Blueprint, render_template, request, redirect
from database.db import get_connection

order = Blueprint("order", __name__)


@order.route("/orders")
def orders():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT orders.id,
               customers.customer_name,
               orders.order_date,
               orders.total_amount
        FROM orders
        JOIN customers
        ON orders.customer_id = customers.id
        ORDER BY orders.id DESC
    """)

    orders = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("orders.html", orders=orders)


@order.route("/add-order", methods=["GET", "POST"])
def add_order():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # Load customers
    cursor.execute("SELECT id, customer_name FROM customers")
    customers = cursor.fetchall()

    # Load products
    cursor.execute("SELECT id, product_name, price FROM products")
    products = cursor.fetchall()

    if request.method == "POST":

        customer_id = request.form["customer_id"]
        product_id = request.form["product_id"]
        quantity = int(request.form["quantity"])

        # Get selected product price
        cursor.execute(
            "SELECT price FROM products WHERE id=%s",
            (product_id,)
        )

        product = cursor.fetchone()

        price = float(product["price"])
        total = price * quantity

        # Save order
        cursor.execute(
            """
            INSERT INTO orders(customer_id, total_amount)
            VALUES(%s,%s)
            """,
            (customer_id, total)
        )

        order_id = cursor.lastrowid

        # Save order item
        cursor.execute(
            """
            INSERT INTO order_items
            (order_id, product_id, quantity, price, subtotal)
            VALUES(%s,%s,%s,%s,%s)
            """,
            (order_id, product_id, quantity, price, total)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/orders")

    cursor.close()
    connection.close()

    return render_template(
        "add_order.html",
        customers=customers,
        products=products
    )