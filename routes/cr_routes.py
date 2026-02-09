#this is the customer service routes file
from flask import Blueprint, render_template
from models.customer import get_all_customers
from models.review import get_all_reviews


customer_srvc_bp = Blueprint("customerService", __name__)




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


#make tables like chat logs
#READ CHAT LOGS
