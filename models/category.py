from db import get_connection

# =============================
# GET ALL CATEGORIES
# =============================
def get_all_categories():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT category_id, name FROM Category ORDER BY category_id")
    result = [
        {"category_id": r[0], "name": r[1]}
        for r in cur.fetchall()
    ]
    cur.close()
    conn.close()
    return result

# =============================
# GET ONE CATEGORY
# =============================
def get_category_by_id(category_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT category_id, name FROM Category WHERE category_id = :id", {"id": category_id})
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return {"category_id": row[0], "name": row[1]}
    return None

# =============================
# ADD CATEGORY
# =============================
def add_category(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO Category (name) VALUES (:name)", {"name": name})
    conn.commit()
    cur.close()
    conn.close()

# =============================
# UPDATE CATEGORY
# =============================
def update_category(category_id, name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Category 
        SET name = :name 
        WHERE category_id = :id
    """, {"id": category_id, "name": name})
    conn.commit()
    cur.close()
    conn.close()

# =============================
# DELETE CATEGORY
# =============================
def delete_category(category_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Category WHERE category_id = :id", {"id": category_id})
    conn.commit()
    cur.close()
    conn.close()
