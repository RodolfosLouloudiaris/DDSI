#this is the customer service routes file
from flask import Blueprint, redirect, render_template
from models.customer import get_all_customers
from models.review import delete_review, get_all_reviews


customer_srvc_bp = Blueprint("customerService", __name__)


@customer_srvc_bp.route("/")
def index():
    return render_template("customerService.html")

#LIST CUSTOMERS
@customer_srvc_bp.route("/list_clients")
def customers():
    all_customers = get_all_customers()
    return render_template("/customerService/list_clients.html", customers=all_customers)


#need to make a complaint table for sure
#LIST CLIENT COMPLAINTS




#LIST REVIEWS
@customer_srvc_bp.route("/list_reviews")
def reviews():
    items = get_all_reviews()
    return render_template("/customerService/list_reviews.html", reviews=items)


@customer_srvc_bp.route("/delete_review/<int:review_id>")
def review_delete(review_id):
    delete_review(review_id)
    return redirect("/customerService/list_reviews")


#make tables like chat logs
#READ CHAT LOGS
