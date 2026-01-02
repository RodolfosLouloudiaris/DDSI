------------------------------------------------------------
-- CLEAN START (optional)
------------------------------------------------------------
-- REMOVE ALL DATA IN CORRECT FK ORDER
DELETE FROM Review;
DELETE FROM StockMovement;
DELETE FROM Shipping;
DELETE FROM Payment;
DELETE FROM OrderItem;
DELETE FROM CustomerOrder;
DELETE FROM Product;
DELETE FROM Category;
DELETE FROM Customer;
DELETE FROM Employee;

------------------------------------------------------------
-- CATEGORY
------------------------------------------------------------
INSERT INTO Category (name) VALUES ('Electronics');
INSERT INTO Category (name) VALUES ('Clothing');
INSERT INTO Category (name) VALUES ('Home & Kitchen');

------------------------------------------------------------
-- PRODUCT
------------------------------------------------------------
INSERT INTO Product (name, description, price, category_id, stock_quantity)
VALUES ('Smartphone X10', 'High-end smartphone with OLED display', 799.99, 1, 50);

INSERT INTO Product (name, description, price, category_id, stock_quantity)
VALUES ('Wireless Headphones', 'Noise-cancelling over-ear headphones', 199.99, 1, 80);

INSERT INTO Product (name, description, price, category_id, stock_quantity)
VALUES ('T-Shirt Basic', 'Cotton T-shirt', 19.99, 2, 200);

INSERT INTO Product (name, description, price, category_id, stock_quantity)
VALUES ('Winter Jacket', 'Warm jacket for cold weather', 129.99, 2, 60);

INSERT INTO Product (name, description, price, category_id, stock_quantity)
VALUES ('Blender Pro', 'Multi-speed kitchen blender', 89.99, 3, 40);

------------------------------------------------------------
-- CUSTOMER
------------------------------------------------------------
INSERT INTO Customer (first_name, last_name, email, phone, address)
VALUES ('Alice', 'Miller', 'alice@example.com', '555-1111', '123 Main St');

INSERT INTO Customer (first_name, last_name, email, phone, address)
VALUES ('Bob', 'Johnson', 'bob@example.com', '555-2222', '456 Market St');

INSERT INTO Customer (first_name, last_name, email, phone, address)
VALUES ('Clara', 'Smith', 'clara@example.com', '555-3333', '789 Sunset Blvd');

------------------------------------------------------------
-- EMPLOYEE
------------------------------------------------------------
INSERT INTO Employee (first_name, last_name, role)
VALUES ('Daniel', 'Hughes', 'Warehouse Worker');

INSERT INTO Employee (first_name, last_name, role)
VALUES ('Eva', 'Lopez', 'Delivery Driver');

INSERT INTO Employee (first_name, last_name, role)
VALUES ('Frank', 'Nguyen', 'Inventory Manager');

------------------------------------------------------------
-- ORDERS
------------------------------------------------------------
-- Alice
INSERT INTO CustomerOrder (customer_id, status)
VALUES (1, 'pending');

-- Bob
INSERT INTO CustomerOrder (customer_id, status)
VALUES (2, 'completed');

-- Clara
INSERT INTO CustomerOrder (customer_id, status)
VALUES (3, 'shipped');

------------------------------------------------------------
-- ORDER ITEMS
------------------------------------------------------------
-- Order 1 (Alice)
INSERT INTO OrderItem (order_id, product_id, quantity, unit_price)
VALUES (1, 1, 1, 799.99);   -- Smartphone

INSERT INTO OrderItem (order_id, product_id, quantity, unit_price)
VALUES (1, 3, 2, 19.99);    -- T-shirts

-- Order 2 (Bob)
INSERT INTO OrderItem (order_id, product_id, quantity, unit_price)
VALUES (2, 2, 1, 199.99);   -- Headphones

-- Order 3 (Clara)
INSERT INTO OrderItem (order_id, product_id, quantity, unit_price)
VALUES (3, 4, 1, 129.99);   -- Jacket

------------------------------------------------------------
-- PAYMENT (1:1 with order)
------------------------------------------------------------
INSERT INTO Payment (order_id, amount, method)
VALUES (2, 199.99, 'Credit Card');  -- Bob paid

INSERT INTO Payment (order_id, amount, method)
VALUES (3, 129.99, 'PayPal');       -- Clara paid

------------------------------------------------------------
-- SHIPPING (0..1 per order)
------------------------------------------------------------
INSERT INTO Shipping (order_id, employee_id, shipped_at, delivery_date, tracking_code)
VALUES (3, 2, SYSTIMESTAMP - 2, SYSTIMESTAMP + 3, 'TRACK12345');

------------------------------------------------------------
-- STOCK MOVEMENT
------------------------------------------------------------
-- Smartphone restock
INSERT INTO StockMovement (product_id, employee_id, quantity, reason)
VALUES (1, 3, 20, 'Restocked from supplier');

-- Jacket sold
INSERT INTO StockMovement (product_id, employee_id, quantity, reason)
VALUES (4, 1, -1, 'Sold to customer Clara');

-- Blender damaged
INSERT INTO StockMovement (product_id, employee_id, quantity, reason)
VALUES (5, 3, -2, 'Damaged during transport');

------------------------------------------------------------
-- REVIEW
------------------------------------------------------------
INSERT INTO Review (product_id, customer_id, rating, review_comment)
VALUES (1, 1, 5, 'Amazing smartphone! Very fast and great display.');

INSERT INTO Review (product_id, customer_id, rating, review_comment)
VALUES (3, 1, 4, 'Good quality T-shirts, nice fit.');

INSERT INTO Review (product_id, customer_id, rating, review_comment)
VALUES (2, 2, 3, 'Sound quality is good, but battery life could be better.');

INSERT INTO Review (product_id, customer_id, rating, review_comment)
VALUES (4, 3, 5, 'Super warm jacket, perfect for winter!');