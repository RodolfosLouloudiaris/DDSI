from db import get_connection

# ----------------------------
# GET ALL PRODUCTS
# ----------------------------
def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT product_id, name, description, price, stock_quantity 
        FROM Product
        ORDER BY product_id
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {
            "product_id": r[0],
            "name": r[1],
            "description": r[2],
            "price": float(r[3]),
            "stock_quantity": r[4],
        }
        for r in rows
    ]

# ----------------------------
# GET ONE PRODUCT BY ID
# ----------------------------
def get_product_by_id(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT product_id, name, description, price, stock_quantity
        FROM Product WHERE product_id = :id
    """, {"id": product_id})
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        return {
            "product_id": row[0],
            "name": row[1],
            "description": row[2],
            "price": float(row[3]),
            "stock_quantity": row[4],
        }
    return None

# ----------------------------
# ADD PRODUCT
# ----------------------------
def add_product(name, description, price, stock_quantity, category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Product (name, description, price, stock_quantity, category_id)
        VALUES (:name, :description, :price, :stock_quantity, :category_id)
    """, {
        "name": name,
        "description": description,
        "price": price,
        "stock_quantity": stock_quantity,
        "category_id": category_id,
    })
    conn.commit()
    cursor.close()
    conn.close()

# ----------------------------
# UPDATE PRODUCT
# ----------------------------
def update_product(product_id, name, description, price, stock_quantity):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Product
        SET name = :name,
            description = :description,
            price = :price,
            stock_quantity = :stock_quantity
        WHERE product_id = :product_id
    """, {
        "product_id": product_id,
        "name": name,
        "description": description,
        "price": price,
        "stock_quantity": stock_quantity,
    })
    conn.commit()
    cursor.close()
    conn.close()

# ----------------------------
# DELETE PRODUCT
# ----------------------------
def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Product WHERE product_id = :id", {"id": product_id})
    conn.commit()
    cursor.close()
    conn.close()
