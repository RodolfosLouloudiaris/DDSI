# here we have all the app.routes for  the shipping and stock management (inventory)

# i am confused about the list_.py files because in some of them he calls them add
#will check this later

#i think there are issues with the redirects or the urls in the templates or generally in the way they are connected

from flask import Blueprint, app, redirect, render_template, request

from models.shipping import (
    delete_shipping,
    get_all_employees,
    get_all_orders,
    add_shipping,
    get_all_shipping,
    get_shipping_by_id,
    update_shipping
)

from models.stock import (
    delete_stock_movement,
    get_all_products,
    add_stock_movement,
    get_all_stock_movements,
    get_stock_movement_by_id,
    update_stock_movement
)

shippingAndStockManagement_bp = Blueprint("shippingAndStockManagement", __name__)



#SHIPPING

@shippingAndStockManagement_bp.route("/add_shipping", methods=["GET", "POST"])
def add_shipping():
    employees = get_all_employees()
    orders = get_all_orders()     

    if request.method == "POST":
        add_shipping(
            request.form["order_id"],
            request.form["employee_id"],
            request.form.get("shipped_at"),
            request.form.get("delivery_date"),
            request.form.get("tracking_code")
        )
        return redirect("/list_shipping")

    return render_template("/shippingAndStockManagement/add_shipping.html", employees=employees, orders=orders)



@shippingAndStockManagement_bp.route("/edit_shipping/<int:shipping_id>", methods=["GET", "POST"])
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
        return redirect("/list_shipping")

    return render_template("/shippingAndStockManagement/edit_shipping.html", shipping=entry, employees=employees, orders=orders)


@shippingAndStockManagement_bp.route("/delete_shipping/<int:shipping_id>", methods=["POST"])
def shipping_delete(shipping_id):
    delete_shipping(shipping_id)
    return redirect("/list_shipping")


@shippingAndStockManagement_bp.route("/list_shipping")
def shipping():
    items = get_all_shipping()
    return render_template("shippingAndStockManagement/list_shipping.html", shipping=items)


#STOCK

@shippingAndStockManagement_bp.route("/add_stock", methods=["GET", "POST"])
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
        return redirect("/shippingAndStockManagement/list_stock")

    return render_template("shippingAndStockManagement/add_stock.html", products=products, employees=employees)


@shippingAndStockManagement_bp.route("/delete_stock/<int:movement_id>")
def stock_delete(movement_id):
    delete_stock_movement(movement_id)
    return redirect("/shippingAndStockManagement/list_stock")


@shippingAndStockManagement_bp.route("/edit_stock/<int:movement_id>", methods=["GET", "POST"])
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
        "shippingAndStockManagement/edit_stock.html",
        movement=movement,
        products=products,
        employees=employees
    )


@shippingAndStockManagement_bp.route("/list_stock")
def stock():
    items = get_all_stock_movements()
    return render_template("shippingAndStockManagement/list_stock.html", movements=items)

