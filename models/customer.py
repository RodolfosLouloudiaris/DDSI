from db import get_connection

# =============================
# GET ALL CUSTOMERS
# =============================
def get_all_customers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT customer_id, first_name, last_name, email, phone, address
        FROM Customer
        ORDER BY customer_id
    """)

    customers = [
        {
            "customer_id": r[0],
            "first_name": r[1],
            "last_name": r[2],
            "email": r[3],
            "phone": r[4],
            "address": r[5],
        }
        for r in cur.fetchall()
    ]

    cur.close()
    conn.close()
    return customers

# =============================
# GET ONE CUSTOMER
# =============================
def get_customer_by_id(customer_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT customer_id, first_name, last_name, email, phone, address
        FROM Customer
        WHERE customer_id = :id
    """, {"id": customer_id})

    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return {
            "customer_id": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "email": row[3],
            "phone": row[4],
            "address": row[5],
        }
    return None

# =============================
# ADD CUSTOMER
# =============================
def add_customer(first_name, last_name, email, phone, address):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO Customer (first_name, last_name, email, phone, address)
        VALUES (:first, :last, :email, :phone, :address)
    """, {
        "first": first_name,
        "last": last_name,
        "email": email,
        "phone": phone,
        "address": address,
    })

    conn.commit()
    cur.close()
    conn.close()

# =============================
# UPDATE CUSTOMER
# =============================
def update_customer(customer_id, first_name, last_name, email, phone, address):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE Customer
        SET first_name = :first,
            last_name = :last,
            email = :email,
            phone = :phone,
            address = :address
        WHERE customer_id = :id
    """, {
        "id": customer_id,
        "first": first_name,
        "last": last_name,
        "email": email,
        "phone": phone,
        "address": address,
    })

    conn.commit()
    cur.close()
    conn.close()

# =============================
# DELETE CUSTOMER
# (NOTE: will fail if customer has orders)
# =============================
def delete_customer(customer_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM Customer WHERE customer_id = :id", {"id": customer_id})

    conn.commit()
    cur.close()
    conn.close()
