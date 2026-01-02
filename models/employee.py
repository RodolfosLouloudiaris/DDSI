from db import get_connection

# =============================
# GET ALL EMPLOYEES
# =============================
def get_all_employees():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT employee_id, first_name, last_name, role
        FROM Employee
        ORDER BY employee_id
    """)
    employees = [
        {
            "employee_id": r[0],
            "first_name": r[1],
            "last_name": r[2],
            "role": r[3],
        }
        for r in cur.fetchall()
    ]
    cur.close()
    conn.close()
    return employees

# =============================
# GET ONE EMPLOYEE
# =============================
def get_employee_by_id(employee_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT employee_id, first_name, last_name, role
        FROM Employee
        WHERE employee_id = :id
    """, {"id": employee_id})
    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return {
            "employee_id": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "role": row[3],
        }

    return None

# =============================
# ADD EMPLOYEE
# =============================
def add_employee(first_name, last_name, role):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO Employee (first_name, last_name, role)
        VALUES (:f, :l, :r)
    """, {
        "f": first_name,
        "l": last_name,
        "r": role
    })

    conn.commit()
    cur.close()
    conn.close()

# =============================
# UPDATE EMPLOYEE
# =============================
def update_employee(employee_id, first_name, last_name, role):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE Employee
        SET first_name = :f,
            last_name = :l,
            role = :r
        WHERE employee_id = :id
    """, {
        "id": employee_id,
        "f": first_name,
        "l": last_name,
        "r": role
    })

    conn.commit()
    cur.close()
    conn.close()

# =============================
# DELETE EMPLOYEE
# =============================
def delete_employee(employee_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM Employee WHERE employee_id = :id", {"id": employee_id})

    conn.commit()
    cur.close()
    conn.close()
