
from flask import Blueprint, render_template, request, redirect
from models.employee import (
    get_all_employees,
    get_employee_by_id,
    add_employee,
    update_employee,
    delete_employee
)


humanResources_bp = Blueprint("humanResources", __name__)



@humanResources_bp.route("/add_employee")
def add_employee_route():
    if request.method == "POST":
        add_employee(
            request.form["first_name"],
            request.form["last_name"],
            request.form.get("role")
        )
        return redirect("/humanResources/list_employees")

    return render_template("humanResources/add_employee.html")


##change the name from employees to list_employees
@humanResources_bp.route("/list_employees")
def list_employees():
    items = get_all_employees()
    return render_template("/humanResources/list_employees.html", employees=items)

@humanResources_bp.route("/delete_employee/<int:employee_id>")
def employee_delete(employee_id):
    delete_employee(employee_id)
    return redirect("/humanResources/list_employees")

@humanResources_bp.route("/edit_employees/<int:employee_id>", methods=["GET", "POST"])
def employee_edit(employee_id):
    emp = get_employee_by_id(employee_id)

    if request.method == "POST":
        update_employee(
            employee_id,
            request.form["first_name"],
            request.form["last_name"],
            request.form.get("role")
        )
        return redirect("/humanResources/list_employees")

    return render_template("humanResources/edit_employee.html", employee=emp)


#these need new tables and sql stufff
@humanResources_bp.route("/list_complaints")
def list_complaints():
    return render_template("humanResources/list_complaints.html")

