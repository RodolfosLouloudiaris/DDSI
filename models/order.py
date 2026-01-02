from db import get_connection
import oracledb

# ============================
# GET ALL ORDERS
# ============================
def get_all_orders():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT order_id, customer_id, order_date, status
        FROM CustomerOrder
        ORDER BY order_id DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "order_id": r[0],
            "customer_id": r[1],
            "order_date": r[2],
            "status": r[3],
        }
        for r in rows
    ]

def create_order_with_items(customer_id, items, status="pending"):
    conn = get_connection()
    cur = conn.cursor()

    # IMPORTANT: arraysize=1 so getvalue() returns a scalar (or a 1-element list)
    oid = cur.var(oracledb.NUMBER, arraysize=1)

    cur.execute("""
        INSERT INTO CustomerOrder (customer_id, status)
        VALUES (:cid, :status)
        RETURNING order_id INTO :oid
    """, {"cid": int(customer_id), "status": status, "oid": oid})

    order_id = oid.getvalue()
    # If python-oracledb still returns [id], flatten it
    if isinstance(order_id, list):
        order_id = order_id[0]
    order_id = int(order_id)

    cur.executemany("""
        INSERT INTO OrderItem (order_id, product_id, quantity, unit_price)
        VALUES (:oid, :pid, :qty, :price)
    """, [
        {
            "oid": order_id,
            "pid": int(it["product_id"]),
            "qty": int(it["quantity"]),
            "price": float(it["unit_price"]),
        }
        for it in items
    ])

    conn.commit()
    cur.close()
    conn.close()
    return order_id

# ============================
# GET ORDER DETAILS
# ============================
def get_order(order_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT order_id, customer_id, order_date, status
        FROM CustomerOrder
        WHERE order_id = :id
    """, {"id": order_id})
    header = cur.fetchone()

    cur.execute("""
        SELECT product_id, quantity, unit_price
        FROM OrderItem
        WHERE order_id = :id
    """, {"id": order_id})
    items = cur.fetchall()

    cur.close()
    conn.close()

    return {
        "order_id": header[0],
        "customer_id": header[1],
        "order_date": header[2],
        "status": header[3],
        "order_items": [
            {"product_id": i[0], "quantity": i[1], "unit_price": i[2]}
            for i in items
        ]
    }

# ============================
# DELETE ORDER
# ============================
def delete_order(order_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM OrderItem WHERE order_id = :id", {"id": order_id})
    cur.execute("DELETE FROM CustomerOrder WHERE order_id = :id", {"id": order_id})

    conn.commit()
    cur.close()
    conn.close()
