from flask import Blueprint, Flask, render_template, request, redirect, session
from db import init_pool
from models.product import (
    get_all_products,
)
from models.customer import (
    get_all_customers,
    
)
from models.order import (
 
    create_order_checkout
)

from models.category import  get_all_categories

##removed code had written twice. This might be a

#it should be running. If not check if the routes are correct and serve the correct purpose
customer_bp = Blueprint("customer", __name__)

def get_cart():
    return session.get("cart", {})  # {product_id(str): quantity(int)}

def save_cart(cart):
    session["cart"] = cart
    session.modified = True


#SHOP

@customer_bp.route("/shop")
def shop():
    categories = get_all_categories()
    products = get_all_products()

    # optional filter: /shop?category_id=2
    category_id = request.args.get("category_id")
    if category_id:
        products = [p for p in products if str(p["category_id"]) == str(category_id)]

    return render_template("/customer/shop.html", categories=categories, products=products)

#changed the route from cart to customer cart lets see if this breaks anything

    
@customer_bp.route("/cart")
def cart_view():
    cart = get_cart()
    products = get_all_products()
    product_map = {str(p["product_id"]): p for p in products}

    items = []
    total = 0.0

    for pid, qty in cart.items():
        p = product_map.get(str(pid))
        if not p:
            continue
        subtotal = float(p["price"]) * int(qty)
        total += subtotal
        items.append({"product": p, "qty": int(qty), "subtotal": subtotal})

    return render_template("/customer/cart.html", items=items, total=total)


@customer_bp.route("/cart/add/<int:product_id>", methods=["POST"])
def cart_add(product_id):
    cart = get_cart()
    pid = str(product_id)
    cart[pid] = int(cart.get(pid, 0)) + 1
    save_cart(cart)
    return redirect("/customer/cart")


@customer_bp.route("/cart/update", methods=["POST"])
def cart_update():
    cart = {}
    for key, value in request.form.items():
        # keys like qty_5
        if key.startswith("qty_"):
            pid = key.replace("qty_", "")
            qty = int(value)
            if qty > 0:
                cart[pid] = qty
    save_cart(cart)
    return redirect("/customer/cart")


@customer_bp.route("/cart/clear", methods=["POST"])
def cart_clear():
    save_cart({})
    return redirect("/customer/cart")


@customer_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = get_cart()
    if not cart:
        return redirect("/customer/shop")

    customers = get_all_customers()

    # Build cart_items for checkout function
    cart_items = [{"product_id": int(pid), "quantity": int(qty)} for pid, qty in cart.items()]

    if request.method == "POST":
        customer_id = int(request.form["customer_id"])
        pay_now = request.form.get("pay_now") == "on"
        method = request.form.get("method") or "card"

        order_id = create_order_checkout(
            customer_id=customer_id,
            cart_items=cart_items,
            status="pending",
            create_payment=pay_now,
            payment_method=method
        )

        save_cart({})
        
        return redirect(f"/customer/shop/{order_id}")  # reuse your admin order detail page

#===========================================
#TILL HERE i changed the routes from "/checkout" to /customer/checkout
# the endpoints are also changed in the html files

    # show checkout summary
    products = get_all_products()
    product_map = {str(p["product_id"]): p for p in products}
    summary = []
    total = 0.0
    for pid, qty in cart.items():
        p = product_map.get(str(pid))
        if not p:
            continue
        subtotal = float(p["price"]) * int(qty)
        total += subtotal
        summary.append({"product": p, "qty": int(qty), "subtotal": subtotal})
#changed shop/checkout to customer/checkout
    return render_template("/customer/checkout.html", customers=customers, summary=summary, total=total)



## added the add review route here
    
@customer_bp.route("/reviews/add/<int:product_id>", methods=["GET", "POST"])
def add_review(product_id):
    if request.method == "POST":
        rating = int(request.form["rating"])
        comment = request.form["comment"]
        add_review(product_id, rating, comment)
        return redirect(f"/customer/shop/{product_id}")
    return render_template("/customer/add_review.html", product_id=product_id)
   
