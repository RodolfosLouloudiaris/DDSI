from db import get_connection

# =============================
# GET ALL REVIEWS
# =============================
def get_all_reviews():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT review_id, product_id, customer_id, rating, review_comment, created_at
        FROM Review
        ORDER BY review_id
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "review_id": r[0],
            "product_id": r[1],
            "customer_id": r[2],
            "rating": r[3],
            "comment": r[4],
            "created_at": r[5],
        }
        for r in rows
    ]

# =============================
# GET REVIEW BY ID
# =============================
def get_review_by_id(review_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT review_id, product_id, customer_id, rating, review_comment, created_at
        FROM Review
        WHERE review_id = :id
    """, {"id": review_id})

    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return {
            "review_id": row[0],
            "product_id": row[1],
            "customer_id": row[2],
            "rating": row[3],
            "comment": row[4],
            "created_at": row[5],
        }
    return None

# =============================
# ADD REVIEW
# =============================
def add_review(product_id, customer_id, rating, comment):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO Review (product_id, customer_id, rating, review_comment)
        VALUES (:product_id, :customer_id, :rating, :comment)
    """, {
        "product_id": product_id,
        "customer_id": customer_id,
        "rating": rating,
        "comment": comment,
    })

    conn.commit()
    cur.close()
    conn.close()

# =============================
# UPDATE REVIEW
# =============================
def update_review(review_id, product_id, customer_id, rating, comment):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE Review
        SET product_id = :product_id,
            customer_id = :customer_id,
            rating = :rating,
            review_comment = :comment
        WHERE review_id = :id
    """, {
        "id": review_id,
        "product_id": product_id,
        "customer_id": customer_id,
        "rating": rating,
        "comment": comment,
    })

    conn.commit()
    cur.close()
    conn.close()

# =============================
# DELETE REVIEW
# =============================
def delete_review(review_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM Review WHERE review_id = :id", {"id": review_id})

    conn.commit()
    cur.close()
    conn.close()
