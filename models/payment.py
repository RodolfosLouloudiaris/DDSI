from db import get_connection

# =============================
# GET ALL PAYMENTS
# =============================
def get_all_payments():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT payment_id, order_id, amount, method, paid_at
        FROM Payment
        ORDER BY payment_id DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "payment_id": r[0],
            "order_id": r[1],
            "amount": float(r[2]) if r[2] is not None else None,
            "method": r[3],
            "paid_at": r[4],
        }
        for r in rows
    ]


# =============================
# GET ONE PAYMENT
# =============================
def get_payment_by_id(payment_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT payment_id, order_id, amount, method, paid_at
        FROM Payment
        WHERE payment_id = :id
    """, {"id": payment_id})
    r = cur.fetchone()
    cur.close()
    conn.close()

    if not r:
        return None

    return {
        "payment_id": r[0],
        "order_id": r[1],
        "amount": float(r[2]) if r[2] is not None else None,
        "method": r[3],
        "paid_at": r[4],
    }


# =============================
# ADD PAYMENT
# =============================
def add_payment(order_id, amount, method):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Payment (order_id, amount, method)
        VALUES (:oid, :amount, :method)
    """, {
        "oid": int(order_id),
        "amount": float(amount),
        "method": method
    })
    conn.commit()
    cur.close()
    conn.close()


# =============================
# UPDATE PAYMENT
# =============================
def update_payment(payment_id, amount, method):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Payment
        SET amount = :amount,
            method = :method
        WHERE payment_id = :id
    """, {
        "id": int(payment_id),
        "amount": float(amount),
        "method": method
    })
    conn.commit()
    cur.close()
    conn.close()


# =============================
# DELETE PAYMENT
# =============================
def delete_payment(payment_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Payment WHERE payment_id = :id", {"id": int(payment_id)})
    conn.commit()
    cur.close()
    conn.close()


# =============================
# ORDERS THAT DON'T HAVE PAYMENT YET
# =============================
def get_unpaid_orders():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT o.order_id
        FROM CustomerOrder o
        LEFT JOIN Payment p ON p.order_id = o.order_id
        WHERE p.order_id IS NULL
        ORDER BY o.order_id DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"order_id": r[0]} for r in rows]
