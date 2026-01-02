from db import get_connection

# =============================
# GET ALL SHIPPING RECORDS
# =============================
def get_all_shipping():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT shipping_id, order_id, employee_id, shipped_at, delivery_date, tracking_code
        FROM Shipping
        ORDER BY shipping_id
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "shipping_id": r[0],
            "order_id": r[1],
            "employee_id": r[2],
            "shipped_at": r[3],
            "delivery_date": r[4],
            "tracking_code": r[5],
        }
        for r in rows
    ]

# =============================
# GET ONE SHIPPING ENTRY
# =============================
def get_shipping_by_id(shipping_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT shipping_id, order_id, employee_id, shipped_at, delivery_date, tracking_code
        FROM Shipping
        WHERE shipping_id = :id
    """, {"id": shipping_id})

    r = cur.fetchone()
    cur.close()
    conn.close()

    if not r:
        return None

    return {
        "shipping_id": r[0],
        "order_id": r[1],
        "employee_id": r[2],
        "shipped_at": r[3],
        "delivery_date": r[4],
        "tracking_code": r[5],
    }

# =============================
# ADD SHIPPING ENTRY
# =============================
def add_shipping(order_id, employee_id, shipped_at, delivery_date, tracking_code):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO Shipping (order_id, employee_id, shipped_at, delivery_date, tracking_code)
        VALUES (:order_id, :employee_id, :shipped_at, :delivery_date, :tracking_code)
    """, {
        "order_id": order_id,
        "employee_id": employee_id,
        "shipped_at": shipped_at,
        "delivery_date": delivery_date,
        "tracking_code": tracking_code,
    })

    conn.commit()
    cur.close()
    conn.close()

# =============================
# UPDATE SHIPPING ENTRY
# =============================
def update_shipping(shipping_id, order_id, employee_id, shipped_at, delivery_date, tracking_code):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE Shipping
        SET order_id = :order_id,
            employee_id = :employee_id,
            shipped_at = :shipped_at,
            delivery_date = :delivery_date,
            tracking_code = :tracking_code
        WHERE shipping_id = :id
    """, {
        "id": shipping_id,
        "order_id": order_id,
        "employee_id": employee_id,
        "shipped_at": shipped_at,
        "delivery_date": delivery_date,
        "tracking_code": tracking_code,
    })

    conn.commit()
    cur.close()
    conn.close()

# =============================
# DELETE SHIPPING ENTRY
# =============================
def delete_shipping(shipping_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM Shipping WHERE shipping_id = :id", {"id": shipping_id})

    conn.commit()
    cur.close()
    conn.close()
