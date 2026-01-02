from flask import Flask, render_template, request, redirect
from db import init_pool
from models.product import (
    get_all_products,
    get_product_by_id,
    add_product,
    update_product,
    delete_product
)
from models.category import (
    get_all_categories,
    get_category_by_id,
    add_category,
    update_category,
    delete_category
)
from models.customer import (
    get_all_customers,
    get_customer_by_id,
    add_customer,
    update_customer,
    delete_customer
)
from models.employee import (
    get_all_employees,
    get_employee_by_id,
    add_employee,
    update_employee,
    delete_employee
)
from models.shipping import (
    get_all_shipping,
    get_shipping_by_id,
    add_shipping,
    update_shipping,
    delete_shipping
)
from models.stock import (
    get_all_stock_movements,
    get_stock_movement_by_id,
    add_stock_movement,
    update_stock_movement,
    delete_stock_movement
)
from models.review import (
    get_all_reviews,
    get_review_by_id,
    add_review,
    update_review,
    delete_review
)
from models.order import (
    get_all_orders,
    create_order_with_items,
    get_order,
    delete_order
)
from models.payment import (
    get_all_payments,
    get_payment_by_id,
    add_payment,
    update_payment,
    delete_payment,
    get_unpaid_orders
)

app = Flask(__name__)

# ===========================
# HOME-PAGE
# ===========================
@app.route("/")
def index():
    return render_template("dashboard.html")

# ===========================
# LIST ALL PRODUCTS
# ===========================
@app.route("/products")
def products():
    items = get_all_products()
    return render_template("products/list.html", products=items)

# ===========================
# ADD PRODUCT
# ===========================
@app.route("/products/add", methods=["GET", "POST"])
def product_add():
    if request.method == "POST":
        name = request.form["name"]
        desc = request.form["description"]
        price = request.form["price"]
        qty = request.form["stock_quantity"]
        category_id = request.form["category_id"]

        add_product(name, desc, price, qty, category_id)
        return redirect("/products")

    return render_template("products/add.html")

# ===========================
# EDIT PRODUCT
# ===========================
@app.route("/products/edit/<int:product_id>", methods=["GET", "POST"])
def product_edit(product_id):
    product = get_product_by_id(product_id)

    if request.method == "POST":
        update_product(
            product_id,
            request.form["name"],
            request.form["description"],
            request.form["price"],
            request.form["stock_quantity"]
        )
        return redirect("/products")

    return render_template("products/edit.html", product=product)

# ===========================
# DELETE PRODUCT
# ===========================
@app.route("/products/delete/<int:product_id>")
def product_delete(product_id):
    delete_product(product_id)
    return redirect("/products")


# ======================================
# LIST CATEGORIES
# ======================================
@app.route("/categories")
def categories():
    items = get_all_categories()
    return render_template("categories/list.html", categories=items)

# ======================================
# ADD CATEGORY
# ======================================
@app.route("/categories/add", methods=["GET", "POST"])
def category_add():
    if request.method == "POST":
        name = request.form["name"]
        add_category(name)
        return redirect("/categories")
    return render_template("categories/add.html")

# ======================================
# EDIT CATEGORY
# ======================================
@app.route("/categories/edit/<int:category_id>", methods=["GET", "POST"])
def category_edit(category_id):
    category = get_category_by_id(category_id)

    if request.method == "POST":
        new_name = request.form["name"]
        update_category(category_id, new_name)
        return redirect("/categories")

    return render_template("categories/edit.html", category=category)

# ======================================
# DELETE CATEGORY
# ======================================
@app.route("/categories/delete/<int:category_id>")
def category_delete(category_id):
    delete_category(category_id)
    return redirect("/categories")


# ==========================================
# LIST CUSTOMERS
# ==========================================
@app.route("/customers")
def customers():
    all_customers = get_all_customers()
    return render_template("customers/list.html", customers=all_customers)

# ==========================================
# ADD CUSTOMER
# ==========================================
@app.route("/customers/add", methods=["GET", "POST"])
def customer_add():
    if request.method == "POST":
        add_customer(
            request.form["first_name"],
            request.form["last_name"],
            request.form["email"],
            request.form.get("phone"),
            request.form.get("address")
        )
        return redirect("/customers")

    return render_template("customers/add.html")

# ==========================================
# EDIT CUSTOMER
# ==========================================
@app.route("/customers/edit/<int:customer_id>", methods=["GET", "POST"])
def customer_edit(customer_id):
    customer = get_customer_by_id(customer_id)

    if request.method == "POST":
        update_customer(
            customer_id,
            request.form["first_name"],
            request.form["last_name"],
            request.form["email"],
            request.form.get("phone"),
            request.form.get("address")
        )
        return redirect("/customers")

    return render_template("customers/edit.html", customer=customer)

# ==========================================
# DELETE CUSTOMER
# ==========================================
@app.route("/customers/delete/<int:customer_id>")
def customer_delete(customer_id):
    try:
        delete_customer(customer_id)
    except Exception:
        # optional: show a friendly error
        print("Cannot delete customer — existing orders.")
    return redirect("/customers")

# ==========================================
# LIST EMPLOYEES
# ==========================================
@app.route("/employees")
def employees():
    items = get_all_employees()
    return render_template("employees/list.html", employees=items)

# ==========================================
# ADD EMPLOYEE
# ==========================================
@app.route("/employees/add", methods=["GET", "POST"])
def employee_add():
    if request.method == "POST":
        add_employee(
            request.form["first_name"],
            request.form["last_name"],
            request.form.get("role")
        )
        return redirect("/employees")

    return render_template("employees/add.html")

# ==========================================
# EDIT EMPLOYEE
# ==========================================
@app.route("/employees/edit/<int:employee_id>", methods=["GET", "POST"])
def employee_edit(employee_id):
    emp = get_employee_by_id(employee_id)

    if request.method == "POST":
        update_employee(
            employee_id,
            request.form["first_name"],
            request.form["last_name"],
            request.form.get("role")
        )
        return redirect("/employees")

    return render_template("employees/edit.html", employee=emp)

# ==========================================
# DELETE EMPLOYEE
# ==========================================
@app.route("/employees/delete/<int:employee_id>")
def employee_delete(employee_id):
    delete_employee(employee_id)
    return redirect("/employees")

# ==========================================
# LIST SHIPPING ENTRIES
# ==========================================
@app.route("/shipping")
def shipping():
    items = get_all_shipping()
    return render_template("shipping/list.html", shipping=items)

# ==========================================
# ADD SHIPPING
# ==========================================
@app.route("/shipping/add", methods=["GET", "POST"])
def shipping_add():
    employees = get_all_employees()
    orders = get_all_orders()     # minimal order list

    if request.method == "POST":
        add_shipping(
            request.form["order_id"],
            request.form["employee_id"],
            request.form.get("shipped_at"),
            request.form.get("delivery_date"),
            request.form.get("tracking_code")
        )
        return redirect("/shipping")

    return render_template("shipping/add.html", employees=employees, orders=orders)

# ==========================================
# EDIT SHIPPING ENTRY
# ==========================================
@app.route("/shipping/edit/<int:shipping_id>", methods=["GET", "POST"])
def shipping_edit(shipping_id):
    entry = get_shipping_by_id(shipping_id)
    employees = get_all_employees()
    orders = get_all_orders()

    if request.method == "POST":
        update_shipping(
            shipping_id,
            request.form["order_id"],
            request.form["employee_id"],
            request.form.get("shipped_at"),
            request.form.get("delivery_date"),
            request.form.get("tracking_code")
        )
        return redirect("/shipping")

    return render_template("shipping/edit.html", shipping=entry, employees=employees, orders=orders)

# ==========================================
# DELETE SHIPPING ENTRY
# ==========================================
@app.route("/shipping/delete/<int:shipping_id>")
def shipping_delete(shipping_id):
    delete_shipping(shipping_id)
    return redirect("/shipping")


# ==========================================
# LIST STOCK MOVEMENTS
# ==========================================
@app.route("/stock")
def stock():
    items = get_all_stock_movements()
    return render_template("stock/list.html", movements=items)

# ==========================================
# ADD STOCK MOVEMENT
# ==========================================
@app.route("/stock/add", methods=["GET", "POST"])
def stock_add():
    products = get_all_products()
    employees = get_all_employees()

    if request.method == "POST":
        add_stock_movement(
            request.form["product_id"],
            request.form["employee_id"],
            request.form["quantity"],
            request.form.get("reason")
        )
        return redirect("/stock")

    return render_template("stock/add.html", products=products, employees=employees)

# ==========================================
# EDIT STOCK MOVEMENT
# ==========================================
@app.route("/stock/edit/<int:movement_id>", methods=["GET", "POST"])
def stock_edit(movement_id):
    movement = get_stock_movement_by_id(movement_id)
    products = get_all_products()
    employees = get_all_employees()

    if request.method == "POST":
        update_stock_movement(
            movement_id,
            request.form["product_id"],
            request.form["employee_id"],
            request.form["quantity"],
            request.form.get("reason")
        )
        return redirect("/stock")

    return render_template(
        "stock/edit.html",
        movement=movement,
        products=products,
        employees=employees
    )

# ==========================================
# DELETE STOCK MOVEMENT
# ==========================================
@app.route("/stock/delete/<int:movement_id>")
def stock_delete(movement_id):
    delete_stock_movement(movement_id)
    return redirect("/stock")


# ==========================================
# LIST REVIEWS
# ==========================================
@app.route("/reviews")
def reviews():
    items = get_all_reviews()
    return render_template("reviews/list.html", reviews=items)

# ==========================================
# ADD REVIEW
# ==========================================
@app.route("/reviews/add", methods=["GET", "POST"])
def review_add():
    products = get_all_products()
    customers = get_all_customers()

    if request.method == "POST":
        add_review(
            request.form["product_id"],
            request.form["customer_id"],
            request.form["rating"],
            request.form.get("comment")
        )
        return redirect("/reviews")

    return render_template("reviews/add.html", products=products, customers=customers)

# ==========================================
# EDIT REVIEW
# ==========================================
@app.route("/reviews/edit/<int:review_id>", methods=["GET", "POST"])
def review_edit(review_id):
    r = get_review_by_id(review_id)
    products = get_all_products()
    customers = get_all_customers()

    if request.method == "POST":
        update_review(
            review_id,
            request.form["product_id"],
            request.form["customer_id"],
            request.form["rating"],
            request.form.get("comment")
        )
        return redirect("/reviews")

    return render_template("reviews/edit.html", review=r, products=products, customers=customers)

# ==========================================
# DELETE REVIEW
# ==========================================
@app.route("/reviews/delete/<int:review_id>")
def review_delete(review_id):
    delete_review(review_id)
    return redirect("/reviews")


# ==========================================
# LIST ORDER
# ==========================================
@app.route("/orders")
def orders():
    items = get_all_orders()
    return render_template("orders/list.html", orders=items)


# ==========================================
# ADD ORDER
# ==========================================
@app.route("/orders/add", methods=["GET", "POST"])
def orders_add():
    products = get_all_products()
    customers = get_all_customers()

    if request.method == "POST":
        customer_id = int(request.form["customer_id"])
        product_ids = request.form.getlist("product_id[]")
        quantities = request.form.getlist("quantity[]")
        prices = request.form.getlist("price[]")

        if not product_ids:
            return "No order items submitted. Click 'Add Item' first.", 400

        items = []
        for pid, qty, price in zip(product_ids, quantities, prices):
            if isinstance(pid, list): pid = pid[0]
            if isinstance(qty, list): qty = qty[0]
            if isinstance(price, list): price = price[0]

            items.append({
                "product_id": int(pid),
                "quantity": int(qty),
                "unit_price": float(price)
            })

        order_id = create_order_with_items(customer_id, items)
        return redirect(f"/orders/{order_id}")

    return render_template("orders/add.html", products=products, customers=customers)


# ==========================================
# DETAIL ORDER
# ==========================================
@app.route("/orders/<int:order_id>")
def order_detail(order_id):
    order = get_order(order_id)
    return render_template("orders/detail.html", order=order)

# ==========================================
# DELETE ORDER
# ==========================================
@app.route("/orders/delete/<int:order_id>")
def order_delete(order_id):
    delete_order(order_id)
    return redirect("/orders")

# ==========================================
# LIST PAYMENTS
# ==========================================
@app.route("/payments")
def payments():
    items = get_all_payments()
    return render_template("payments/list.html", payments=items)

# ==========================================
# ADD PAYMENT
# ==========================================
@app.route("/payments/add", methods=["GET", "POST"])
def payment_add():
    unpaid_orders = get_unpaid_orders()

    if request.method == "POST":
        add_payment(
            request.form["order_id"],
            request.form["amount"],
            request.form["method"]
        )
        return redirect("/payments")

    return render_template("payments/add.html", unpaid_orders=unpaid_orders)

# ==========================================
# EDIT PAYMENT
# ==========================================
@app.route("/payments/edit/<int:payment_id>", methods=["GET", "POST"])
def payment_edit(payment_id):
    pay = get_payment_by_id(payment_id)

    if request.method == "POST":
        update_payment(
            payment_id,
            request.form["amount"],
            request.form["method"]
        )
        return redirect("/payments")

    return render_template("payments/edit.html", payment=pay)

# ==========================================
# DELETE PAYMENT
# ==========================================
@app.route("/payments/delete/<int:payment_id>")
def payment_delete(payment_id):
    delete_payment(payment_id)
    return redirect("/payments")



if __name__ == "__main__":
    init_pool()
    app.run(debug=True, use_reloader=False)
