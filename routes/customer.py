from flask import Blueprint, render_template, request, redirect
from database.db import get_connection

customer = Blueprint("customer", __name__)


@customer.route("/customers")
def customers():

    search = request.args.get("search")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if search:
        cursor.execute(
            "SELECT * FROM customers WHERE customer_name LIKE %s",
            ("%" + search + "%",)
        )
    else:
        cursor.execute("SELECT * FROM customers")

    customers = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "customers.html",
        customers=customers,
        search=search
    )


@customer.route("/add-customer", methods=["GET", "POST"])
def add_customer():

    if request.method == "POST":

        customer_name = request.form["customer_name"]
        phone = request.form["phone"]
        email = request.form["email"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO customers(customer_name, phone, email)
            VALUES(%s,%s,%s)
        """, (customer_name, phone, email))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/customers")

    return render_template("add_customer.html")


@customer.route("/edit-customer/<int:id>", methods=["GET", "POST"])
def edit_customer(id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # Get customer
    cursor.execute(
        "SELECT * FROM customers WHERE id=%s",
        (id,)
    )

    customer_data = cursor.fetchone()

    if not customer_data:
        cursor.close()
        connection.close()
        return "Customer not found"

    # Update customer
    if request.method == "POST":

        customer_name = request.form["customer_name"]
        phone = request.form["phone"]
        email = request.form["email"]

        cursor.execute("""
            UPDATE customers
            SET customer_name=%s,
                phone=%s,
                email=%s
            WHERE id=%s
        """, (
            customer_name,
            phone,
            email,
            id
        ))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/customers")

    cursor.close()
    connection.close()

    return render_template(
        "edit_customer.html",
        customer=customer_data
    )

@customer.route("/delete-customer/<int:id>")

@customer.route("/delete-customer/<int:id>")
def delete_customer(id):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Check whether customer has existing orders
        cursor.execute(
            "SELECT COUNT(*) FROM orders WHERE customer_id=%s",
            (id,)
        )

        order_count = cursor.fetchone()[0]

        if order_count > 0:
            return (
                "Customer cannot be deleted because orders "
                "are linked to this customer. Please preserve "
                "the customer record to maintain order history."
            ), 400

        # Delete customer if no orders exist
        cursor.execute(
            "DELETE FROM customers WHERE id=%s",
            (id,)
        )

        connection.commit()

        return redirect("/customers")

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()
# def delete_customer(id):

#     connection = get_connection()
#     cursor = connection.cursor()

#     cursor.execute("DELETE FROM customers WHERE id=%s", (id,))

#     connection.commit()

#     cursor.close()
#     connection.close()

#     return redirect("/customers")