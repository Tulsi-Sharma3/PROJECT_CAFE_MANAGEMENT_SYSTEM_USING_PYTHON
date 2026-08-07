from flask import Blueprint, render_template, request, redirect, session
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

    if "cart" not in session:
        session["cart"] = []

    if request.method == "POST":

        customer_id = int(request.form["customer_id"])

        # Save customer when first item is added
        # if "customer_id" not in session:
        #     session["customer_id"] = customer_id

        if not session["cart"]:
            session["customer_id"] = customer_id
            
        # Don't allow changing customer
        if session["customer_id"] != customer_id:
            return "Finish the current order first."

        product_id = int(request.form["product_id"])
        quantity = int(request.form["quantity"])

        cursor.execute(
            "SELECT * FROM products WHERE id=%s",
            (product_id,)
        )

        product = cursor.fetchone()

        subtotal = float(product["price"]) * quantity

        cart = session["cart"]

        cart.append({
            "product_id": product["id"],
            "product_name": product["product_name"],
            "price": float(product["price"]),
            "quantity": quantity,
            "subtotal": subtotal
        })

        session["cart"] = cart

        return redirect("/add-order")

    grand_total = sum(item["subtotal"] for item in session["cart"])
    cursor.close()
    connection.close()

    return render_template(
        "add_order.html",
        customers=customers,
        products=products,
        grand_total=grand_total
    )

@order.route("/place-order")
def place_order():

    if "cart" not in session or len(session["cart"]) == 0:
        return redirect("/add-order")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    customer_id = session["customer_id"]

    grand_total = sum(item["subtotal"] for item in session["cart"])

    invoice_no = "INV-" + str(customer_id) + str(len(session["cart"]))

    # Save order
    cursor.execute("""
        INSERT INTO orders
        (customer_id, invoice_no, total_amount)
        VALUES (%s, %s, %s)
    """, (
        customer_id,
        invoice_no,
        grand_total
    ))

    order_id = cursor.lastrowid

    for item in session["cart"]:

        cursor.execute("""
            INSERT INTO order_items
            (order_id, product_id, quantity, price, subtotal)
            VALUES (%s,%s,%s,%s,%s)
        """, (
            order_id,
            item["product_id"],
            item["quantity"],
            item["price"],
            item["subtotal"]
        ))

        # Automatically reduce stock
        cursor.execute("""
            UPDATE products
            SET stock = stock - %s
            WHERE id = %s
        """, (
            item["quantity"],
            item["product_id"]
        ))

    connection.commit()

    cursor.close()
    connection.close()

    # Clear session
    session.pop("cart", None)
    session.pop("customer_id", None)

    # return "Order Saved Successfully"

    return redirect("/orders")