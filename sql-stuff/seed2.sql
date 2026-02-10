------------------------------------------------------------
-- CLEAN START
------------------------------------------------------------
-- REMOVE ALL DATA IN CORRECT FK ORDER TO PREVENT ERRORS
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
-- CATEGORY (5 Rows)
------------------------------------------------------------
INSERT INTO Category (name) VALUES ('Men''s Fashion');     -- ID: 1
INSERT INTO Category (name) VALUES ('Women''s Fashion');   -- ID: 2
INSERT INTO Category (name) VALUES ('Footwear');          -- ID: 3
INSERT INTO Category (name) VALUES ('Accessories');       -- ID: 4
INSERT INTO Category (name) VALUES ('Sportswear');        -- ID: 5

------------------------------------------------------------
-- PRODUCT (5 Rows)
------------------------------------------------------------
INSERT INTO Product (name, description, price, category_id, stock_quantity)
VALUES ('Classic Cotton T-Shirt', 'Breathable 100% cotton t-shirt in white.', 19.99, 1, 100); -- ID: 1

INSERT INTO Product (name, description, price, category_id, stock_quantity)
VALUES ('Floral Summer Dress', 'Lightweight floral dress perfect for warm weather.', 49.99, 2, 50); -- ID: 2

INSERT INTO Product (name, description, price, category_id, stock_quantity)
VALUES ('Leather Ankle Boots', 'Durable leather boots with non-slip soles.', 89.99, 3, 30); -- ID: 3

INSERT INTO Product (name, description, price, category_id, stock_quantity)
VALUES ('Silk Scarf', 'Elegant silk scarf with paisley pattern.', 25.50, 4, 75); -- ID: 4

INSERT INTO Product (name, description, price, category_id, stock_quantity)
VALUES ('Performance Running Shorts', 'Quick-dry fabric shorts for running.', 29.99, 5, 60); -- ID: 5

------------------------------------------------------------
-- CUSTOMER (5 Rows)
------------------------------------------------------------
INSERT INTO Customer (first_name, last_name, email, phone, address)
VALUES ('Elena', 'Gomez', 'elena.g@example.com', '555-0101', '101 Fashion Ave, Madrid');

INSERT INTO Customer (first_name, last_name, email, phone, address)
VALUES ('Marcus', 'Schmidt', 'marcus.s@example.com', '555-0102', '202 Designer Blvd, Berlin');

INSERT INTO Customer (first_name, last_name, email, phone, address)
VALUES ('Sophie', 'Dubois', 'sophie.d@example.com', '555-0103', '303 Couture Ln, Paris');

INSERT INTO Customer (first_name, last_name, email, phone, address)
VALUES ('Liam', 'O''Connor', 'liam.o@example.com', '555-0104', '404 High St, Dublin');

INSERT INTO Customer (first_name, last_name, email, phone, address)
VALUES ('Yuki', 'Tanaka', 'yuki.t@example.com', '555-0105', '505 Shibuya Crossing, Tokyo');

------------------------------------------------------------
-- EMPLOYEE (5 Rows)
------------------------------------------------------------
INSERT INTO Employee (first_name, last_name, role)
VALUES ('John', 'Doe', 'Warehouse Manager'); -- ID: 1

INSERT INTO Employee (first_name, last_name, role)
VALUES ('Jane', 'Smith', 'Logistics Coordinator'); -- ID: 2

INSERT INTO Employee (first_name, last_name, role)
VALUES ('Mike', 'Ross', 'Delivery Driver'); -- ID: 3

INSERT INTO Employee (first_name, last_name, role)
VALUES ('Rachel', 'Green', 'Sales Associate'); -- ID: 4

INSERT INTO Employee (first_name, last_name, role)
VALUES ('Harvey', 'Specter', 'Store Manager'); -- ID: 5

------------------------------------------------------------
-- CUSTOMER ORDER (5 Rows)
------------------------------------------------------------
-- Order 1: Pending (Elena)
INSERT INTO CustomerOrder (customer_id, status) VALUES (1, 'pending');

-- Order 2: Completed (Marcus)
INSERT INTO CustomerOrder (customer_id, status) VALUES (2, 'completed');

-- Order 3: Shipped (Sophie)
INSERT INTO CustomerOrder (customer_id, status) VALUES (3, 'shipped');

-- Order 4: Completed (Liam)
INSERT INTO CustomerOrder (customer_id, status) VALUES (4, 'completed');

-- Order 5: Cancelled (Yuki)
INSERT INTO CustomerOrder (customer_id, status) VALUES (5, 'cancelled');

------------------------------------------------------------
-- ORDER ITEM (At least 1 per order)
------------------------------------------------------------
-- Order 1 (Elena bought a Dress)
INSERT INTO OrderItem (order_id, product_id, quantity, unit_price)
VALUES (1, 2, 1, 49.99);

-- Order 2 (Marcus bought Boots and T-Shirt)
INSERT INTO OrderItem (order_id, product_id, quantity, unit_price)
VALUES (2, 3, 1, 89.99);
INSERT INTO OrderItem (order_id, product_id, quantity, unit_price)
VALUES (2, 1, 2, 19.99);

-- Order 3 (Sophie bought a Scarf)
INSERT INTO OrderItem (order_id, product_id, quantity, unit_price)
VALUES (3, 4, 2, 25.50);

-- Order 4 (Liam bought Shorts)
INSERT INTO OrderItem (order_id, product_id, quantity, unit_price)
VALUES (4, 5, 3, 29.99);

-- Order 5 (Yuki tried to buy Boots but cancelled)
INSERT INTO OrderItem (order_id, product_id, quantity, unit_price)
VALUES (5, 3, 1, 89.99);

------------------------------------------------------------
-- PAYMENT (Linked to Orders 2, 3, 4)
------------------------------------------------------------
-- Payment for Order 2
INSERT INTO Payment (order_id, amount, method)
VALUES (2, 129.97, 'Credit Card');

-- Payment for Order 3
INSERT INTO Payment (order_id, amount, method)
VALUES (3, 51.00, 'PayPal');

-- Payment for Order 4
INSERT INTO Payment (order_id, amount, method)
VALUES (4, 89.97, 'Debit Card');

-- Payment for Order 5 (Refunded/Failed - hypothetical context, but row exists)
INSERT INTO Payment (order_id, amount, method)
VALUES (5, 89.99, 'Credit Card');

------------------------------------------------------------
-- SHIPPING (Linked to Orders 2, 3, 4)
------------------------------------------------------------
-- Shipping for Order 2
INSERT INTO Shipping (order_id, employee_id, shipped_at, delivery_date, tracking_code)
VALUES (2, 3, SYSTIMESTAMP - 5, SYSTIMESTAMP - 2, 'DHL-998877');

-- Shipping for Order 3
INSERT INTO Shipping (order_id, employee_id, shipped_at, delivery_date, tracking_code)
VALUES (3, 2, SYSTIMESTAMP - 1, NULL, 'UPS-112233');

-- Shipping for Order 4
INSERT INTO Shipping (order_id, employee_id, shipped_at, delivery_date, tracking_code)
VALUES (4, 3, SYSTIMESTAMP - 10, SYSTIMESTAMP - 8, 'FEDEX-445566');

------------------------------------------------------------
-- STOCK MOVEMENT (5 Rows)
------------------------------------------------------------
-- Initial stock intake for T-Shirts
INSERT INTO StockMovement (product_id, employee_id, quantity, reason)
VALUES (1, 1, 100, 'Initial Inventory Stock');

-- Restocking Dresses
INSERT INTO StockMovement (product_id, employee_id, quantity, reason)
VALUES (2, 1, 20, 'Seasonal Restock');

-- Sold Boots (Order 2)
INSERT INTO StockMovement (product_id, employee_id, quantity, reason)
VALUES (3, 5, -1, 'Sold Order #2');

-- Damaged Scarf found in warehouse
INSERT INTO StockMovement (product_id, employee_id, quantity, reason)
VALUES (4, 2, -1, 'Damaged in storage');

-- Returned Shorts (hypothetical return)
INSERT INTO StockMovement (product_id, employee_id, quantity, reason)
VALUES (5, 4, 1, 'Customer Return');

------------------------------------------------------------
-- REVIEW (5 Rows)
------------------------------------------------------------
INSERT INTO Review (product_id, customer_id, rating, review_comment)
VALUES (1, 2, 5, 'Great fit and very comfortable material.');

INSERT INTO Review (product_id, customer_id, rating, review_comment)
VALUES (2, 1, 4, 'Lovely pattern, but runs a bit small.');

INSERT INTO Review (product_id, customer_id, rating, review_comment)
VALUES (3, 5, 5, 'Best boots I have ever owned. Very sturdy.');

INSERT INTO Review (product_id, customer_id, rating, review_comment)
VALUES (4, 3, 3, 'Fabric is nice but color looks different in person.');

INSERT INTO Review (product_id, customer_id, rating, review_comment)
VALUES (5, 4, 5, 'Perfect for marathon training!');