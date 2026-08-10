# ☕ Smart Cafe Management System

A web-based Cafe Management System developed using **Python, Flask, MySQL, HTML, and CSS**.

The application provides a centralized platform for cafe administrators to manage products, customers, orders, billing, and inventory while monitoring important business information through an interactive dashboard.

---

## 📌 Project Overview

Managing cafe operations manually can make it difficult to maintain product records, customer information, orders, billing, and inventory.

The **Smart Cafe Management System** solves this problem by providing a simple web-based management application where an administrator can manage daily cafe operations from a centralized dashboard.

The system follows a modular architecture with Flask handling the backend logic, MySQL managing persistent data, and HTML/CSS providing the user interface.

---

## ✨ Key Features

### 🔐 Authentication
- Admin login system
- Session-based authentication
- Secure password hashing using Werkzeug

### 📊 Dashboard
- Total products
- Total customers
- Total orders
- Total revenue
- Recent orders
- Low-stock product alerts
- Quick navigation actions

### 📦 Product Management
- Add products
- View products
- Edit product information
- Delete products
- Track product prices and stock

### 👥 Customer Management
- Add customers
- View customer records
- Edit customer information
- Delete customers
- Store customer contact details

### 🛒 Order Management
- Create new customer orders
- Add multiple products to an order
- Calculate product subtotals
- Calculate order grand total
- Store order and order-item details
- Prevent changing the customer during an active order

### 🧾 Billing & Invoice
- Generate invoice after placing an order
- Display customer and order information
- Display ordered products, quantity, price, and subtotal
- Calculate total bill amount
- Printable invoice

### 📦 Inventory Monitoring
- Track product stock
- Identify products with low stock
- Display low-stock alerts on the dashboard

### 🎨 User Interface
- Responsive dashboard layout
- Sidebar navigation
- Cafe branding and logo
- Clean tables and cards
- Consistent cafe-themed styling

---

## 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| Backend Framework | Flask |
| Frontend | HTML5, CSS3 |
| Database | MySQL |
| Database Connector | MySQL Connector/Python |
| Template Engine | Jinja2 |
| Authentication & Security | Werkzeug |
| Development Environment | VS Code |
| Version Control | Git & GitHub |

---

## 🏗️ Application Architecture

The project is organized into separate modules for better maintainability.


Smart-Cafe-Management-System/
│
├── app.py
├── config.py
├── create_admin.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── config/
│
├── database/
│   ├── db.py
│   ├── schema.sql
│   └── seed.sql
│
├── models/
│
├── routes/
│   ├── auth.py
│   ├── customer.py
│   ├── order.py
│   ├── product.py
│   └── ...
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── images/
│       └── logo.png
│
└── templates/
    ├── base.html
    ├── login.html
    ├── dashboard.html
    ├── products.html
    ├── customers.html
    ├── orders.html
    ├── add_order.html
    ├── add_product.html
    └── invoice.html