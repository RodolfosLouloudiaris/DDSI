# DDSI-OnlineShop Management System (Flask + Oracle)

This project is a **full-stack online shop management system** built with **Python (Flask)** and an **Oracle relational database**.
It demonstrates how a normalized relational schema with **foreign keys, constraints, and transactions** can be used in a real-world web application.

The system provides:

* an **Admin Dashboard** for full CRUD management
* a **Shop / Order Management interface** simulating a real online store
* automatic propagation of changes across related tables (orders, stock, shipping, payments)

---

## 📌 Features Overview

### 🔧 Admin Dashboard (Back Office)

The admin interface allows full management of all database entities:

* **Categories** – add, edit, delete product categories
* **Products** – manage product details and stock
* **Customers** – manage customer data
* **Orders** – view, delete, and track orders
* **Order Items** – linked automatically to orders
* **Payments** – manage payments (1:1 with orders)
* **Shipping** – manage shipping state (0..1 per order)
* **Employees** – manage staff
* **Stock Movements** – track inventory changes
* **Reviews** – manage customer reviews

All admin pages support:

* List view
* Create
* Edit
* Delete

---

### 🛍 Shop / Order Management (Front Office)

A separate **shop interface** simulates a real online store:

* Browse products
* Filter products by category
* Add products to cart
* Update cart quantities
* Checkout as an existing customer
* Create an order that automatically:

  * inserts `CustomerOrder`
  * inserts multiple `OrderItem`s
  * reduces product stock
  * creates a `Shipping` record
  * optionally creates a `Payment` record

All these operations are executed **inside a single database transaction**, ensuring data consistency.

---

## 🧠 Database Design Highlights

* Fully normalized schema
* Strong use of **foreign keys**
* One-to-many and one-to-one relationships
* Integrity enforced at database level
* Transaction-safe multi-table updates

### Core Relationships

* Category 1 → N Product
* Customer 1 → N CustomerOrder
* CustomerOrder 1 → N OrderItem
* Product 1 → N OrderItem
* CustomerOrder 1 → 1 Payment
* CustomerOrder 0 → 1 Shipping
* Product 1 → N StockMovement
* Employee 1 → N StockMovement
* Product 1 → N Review
* Customer 1 → N Review

---

## ⚙️ Technology Stack

* **Backend:** Python, Flask
* **Database:** Oracle Database
* **Frontend:** HTML, Jinja2, CSS, JavaScript
* **Sessions:** Flask sessions (cart handling)
* **DB Access:** python-oracledb

---

## 📂 Project Structure

DDSI-OnlineShop/

* app.py
* db.py
* schema.sql

models/

* product.py
* category.py
* customer.py
* order.py
* payment.py
* shipping.py
* employee.py
* stock_movement.py
* review.py

templates/

* base.html
* dashboard.html
* products/
* categories/
* customers/
* orders/
* payments/
* shop/

static/

---

## 🧪 Transaction Management

Critical operations (such as checkout) are handled using **explicit database transactions**:

* Stock is locked using `SELECT ... FOR UPDATE`
* All related inserts/updates are committed together
* On error, the transaction is rolled back

This prevents:

* overselling products
* inconsistent orders
* orphaned records

---

## 🚀 How to Run

1. Create Oracle tables using `schema.sql`
2. Configure the database connection in `db.py`
3. Install dependencies:

   * flask
   * oracledb
4. Initialize the database using `python init_database.py` for the inital seeds
5. Run the application using `python app.py`
6. Open the application at `http://127.0.0.1:5000/`

---

## 📜 License

Educational project — free to use for learning and academic purposes.
