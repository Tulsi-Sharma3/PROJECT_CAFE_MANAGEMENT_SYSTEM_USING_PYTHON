from flask import Flask, render_template, session, redirect

from routes.auth import auth
from routes.product import product
from routes.customer import customer
from routes.order import order

from database.db import get_connection


app = Flask(__name__)

app.secret_key = "REMOVED"


# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(product)
app.register_blueprint(customer)
app.register_blueprint(order)


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)


    # =========================
    # TOTAL PRODUCTS
    # =========================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM products
    """)

    total_products = cursor.fetchone()["total"]


    # =========================
    # TOTAL CUSTOMERS
    # =========================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM customers
    """)

    total_customers = cursor.fetchone()["total"]


    # =========================
    # TOTAL ORDERS
    # =========================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM orders
    """)

    total_orders = cursor.fetchone()["total"]


    # =========================
    # TOTAL REVENUE
    # =========================

    cursor.execute("""
        SELECT IFNULL(SUM(total_amount), 0) AS revenue
        FROM orders
    """)

    total_revenue = cursor.fetchone()["revenue"]


    # =========================
    # RECENT ORDERS
    # =========================

    cursor.execute("""
        SELECT
            orders.invoice_no,
            customers.customer_name,
            orders.total_amount
        FROM orders
        JOIN customers
        ON orders.customer_id = customers.id
        ORDER BY orders.id DESC
        LIMIT 5
    """)

    recent_orders = cursor.fetchall()


    # =========================
    # LOW STOCK PRODUCTS
    # =========================

    cursor.execute("""
        SELECT
            id,
            product_name,
            stock
        FROM products
        WHERE stock < 5
        ORDER BY stock ASC
    """)

    low_stock_products = cursor.fetchall()


    cursor.close()
    connection.close()


    return render_template(
        "dashboard.html",
        total_products=total_products,
        total_customers=total_customers,
        total_orders=total_orders,
        total_revenue=total_revenue,
        recent_orders=recent_orders,
        low_stock_products=low_stock_products
    )

if __name__ == "__main__":
    app.run(debug=True)

