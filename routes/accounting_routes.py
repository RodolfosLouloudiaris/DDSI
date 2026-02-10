#this is the accounting routes file


# ==========================================
# LIST PAYMENTS
# ==========================================

from flask import Blueprint, redirect, render_template, request
from models.payment import *


accounting_bp = Blueprint("accounting", __name__)


@accounting_bp.route('/')
def index():
    return render_template("accounting.html")


@accounting_bp.route("/list_payments")
def payments():
    items = get_all_payments()
    return render_template("accounting/list_payments.html", payments=items)

# ==========================================
# ADD PAYMENT
# ==========================================
@accounting_bp.route("/add_payment", methods=["GET", "POST"])
def payment_add():
    unpaid_orders = get_unpaid_orders()

    if request.method == "POST":
        add_payment(
            request.form["order_id"],
            request.form["amount"],
            request.form["method"]
        )


        return redirect("/accounting/list_payments")

    return render_template("accounting/add_payment.html", unpaid_orders=unpaid_orders)

# ==========================================
# EDIT PAYMENT
# ==========================================
@accounting_bp.route("/edit_payment/<int:payment_id>", methods=["GET", "POST"])
def payment_edit(payment_id):
    pay = get_payment_by_id(payment_id)

    if request.method == "POST":
        update_payment(
            payment_id,
            request.form["amount"],
            request.form["method"]
        )
        return redirect("/accounting/list_payments")

    return render_template("accounting/edit_payment.html", payment=pay)

# ==========================================
# DELETE PAYMENT
# ==========================================
@accounting_bp.route("/delete_payment<int:payment_id>")
def payment_delete(payment_id):
    delete_payment(payment_id)
    return redirect("/accounting/list_payments")