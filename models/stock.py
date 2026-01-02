from db import get_connection

# =============================
# GET ALL STOCK MOVEMENTS
# =============================
def get_all_stock_movements():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT movement_id, product_id, employee_id, quantity, movement_time, reason
        FROM StockMovement
        ORDER BY movement_id
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "movement_id": r[0],
            "product_id": r[1],
            "employee_id": r[2],
            "quantity": r[3],
            "movement_time": r[4],
            "reason": r[5],
        }
        for r in rows
    ]

# =============================
# GET ONE STOCK MOVEMENT
# =============================
def get_stock_movement_by_id(movement_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT movement_id, product_id, employee_id, quantity, movement_time, reason
        FROM StockMovement
        WHERE movement_id = :id
    """, {"id": movement_id})

    r = cur.fetchone()
    cur.close()
    conn.close()

    if not r:
        return None

    return {
        "movement_id": r[0],
        "product_id": r[1],
        "employee_id": r[2],
        "quantity": r[3],
        "movement_time": r[4],
        "reason": r[5],
    }

# =============================
# ADD STOCK MOVEMENT
# =============================
def add_stock_movement(product_id, employee_id, quantity, reason):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO StockMovement (product_id, employee_id, quantity, reason)
        VALUES (:product_id, :employee_id, :quantity, :reason)
    """, {
        "product_id": product_id,
        "employee_id": employee_id,
        "quantity": quantity,
        "reason": reason,
    })

    conn.commit()
    cur.close()
    conn.close()

# =============================
# UPDATE STOCK MOVEMENT
# =============================
def update_stock_movement(movement_id, product_id, employee_id, quantity, reason):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE StockMovement
        SET product_id = :product_id,
            employee_id = :employee_id,
            quantity = :quantity,
            reason = :reason
        WHERE movement_id = :id
    """, {
        "id": movement_id,
        "product_id": product_id,
        "employee_id": employee_id,
        "quantity": quantity,
        "reason": reason,
    })

    conn.commit()
    cur.close()
    conn.close()

# =============================
# DELETE STOCK MOVEMENT
# =============================
def delete_stock_movement(movement_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM StockMovement WHERE movement_id = :id", {"id": movement_id})

    conn.commit()
    cur.close()
    conn.close()
