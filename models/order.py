from db import get_connection
import oracledb


def create_order_checkout(customer_id, cart_items, status="pending", create_payment=False, payment_method="card"):
    """
    cart_items: list of dicts: [{"product_id": int, "quantity": int}, ...]
    - Fetches product prices from DB (prevents tampering)
    - Inserts order + items
    - Decreases stock
    - Creates shipping row
    - Optionally creates payment row
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        # 1) Create order and get id
        oid = cur.var(oracledb.NUMBER, arraysize=1)
        cur.execute("""
            INSERT INTO CustomerOrder (customer_id, status)
            VALUES (:cid, :status)
            RETURNING order_id INTO :oid
        """, {"cid": int(customer_id), "status": status, "oid": oid})

        order_id = oid.getvalue()
        if isinstance(order_id, list):
            order_id = order_id[0]
        order_id = int(order_id)

        # 2) For each item: validate stock + get current price from DB
        order_items = []
        total = 0.0

        for it in cart_items:
            pid = int(it["product_id"])
            qty = int(it["quantity"])

            # lock row to prevent overselling in concurrent sessions
            cur.execute("""
                SELECT price, stock_quantity
                FROM Product
                WHERE product_id = :pid
                FOR UPDATE
            """, {"pid": pid})

            row = cur.fetchone()
            if not row:
                raise ValueError(f"Product {pid} not found")

            price, stock_qty = float(row[0]), int(row[1])

            if qty <= 0:
                raise ValueError("Quantity must be > 0")

            if stock_qty < qty:
                raise ValueError(f"Not enough stock for product {pid}. Have {stock_qty}, need {qty}.")

            order_items.append({
                "oid": order_id,
                "pid": pid,
                "qty": qty,
                "price": price
            })

            total += price * qty

            # reduce stock
            cur.execute("""
                UPDATE Product
                SET stock_quantity = stock_quantity - :qty
                WHERE product_id = :pid
            """, {"qty": qty, "pid": pid})

        # 3) Insert order items
        cur.executemany("""
            INSERT INTO OrderItem (order_id, product_id, quantity, unit_price)
            VALUES (:oid, :pid, :qty, :price)
        """, order_items)

        # 4) Create shipping row (needs employee_id in your schema -> assign a default employee)
        # Make sure employee_id=1 exists (create a "System" employee in admin if needed)
        cur.execute("""
            INSERT INTO Shipping (order_id, employee_id)
            VALUES (:oid, :eid)
        """, {"oid": order_id, "eid": 1})

        # 5) Optional: create payment (1:1)
        if create_payment:
            cur.execute("""
                INSERT INTO Payment (order_id, amount, method)
                VALUES (:oid, :amount, :method)
            """, {"oid": order_id, "amount": total, "method": payment_method})

            # also update order status
            cur.execute("""
                UPDATE CustomerOrder
                SET status = 'paid'
                WHERE order_id = :oid
            """, {"oid": order_id})

        conn.commit()
        return order_id

    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

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
