from flask import Flask, render_template, request, redirect
from db import init_pool
from models.product import (
    get_all_products,
    get_product_by_id,
    add_product,
    update_product,
    delete_product
)

app = Flask(__name__)

# ===========================
# HOME-PAGE
# ===========================
@app.route("/")
def index():
    return render_template("index.html")

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


if __name__ == "__main__":
    init_pool()
    app.run(debug=True)
