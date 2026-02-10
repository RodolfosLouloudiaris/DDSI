from flask import Flask, render_template, request, redirect, session
from db import init_pool

from routes.customer_routes import customer_bp
from routes.hr_routes import humanResources_bp
from routes.inventory_routes import shippingAndStockManagement_bp
from routes.accounting_routes import accounting_bp
from routes.cr_routes import customer_srvc_bp

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

app = Flask(__name__)

app.secret_key = "dev-secret-change-me"




##check the prefixes if they are correct
#Registering the bluepritns
app.register_blueprint(customer_bp, url_prefix="/customer")
app.register_blueprint(humanResources_bp, url_prefix="/humanResources")
app.register_blueprint(shippingAndStockManagement_bp, url_prefix="/shippingAndStockManagement")
app.register_blueprint(accounting_bp, url_prefix="/accounting")
app.register_blueprint(customer_srvc_bp, url_prefix="/customerService")




# ===========================
# HOME-PAGE
# ===========================
@app.route("/")
def index():
    return render_template("base.html")

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

##remove all except list categories


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
        return redirect("/customerService/list_clients")

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
        return redirect("/customerService/list_clients")

    return render_template("customerService/list_clients.html", customer=customer)

# ==========================================
# DELETE CUSTOMER
# ==========================================
@app.route("/customers/delete/<int:customer_id>")
def customer_delete(customer_id):
    try:
        delete_customer(customer_id)
    except Exception:
        print("Cannot delete customer — existing orders.")
    return redirect("/customerService/list_clients")






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



if __name__ == "__main__":
    init_pool()
    app.run(debug=True, use_reloader=False)
