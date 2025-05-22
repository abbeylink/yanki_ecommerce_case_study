CREATE SCHEMA IF NOT EXISTS yanki;

DROP TABLE IF EXISTS yanki.customer CASCADE;
DROP TABLE IF EXISTS yanki.product CASCADE;
DROP TABLE IF EXISTS yanki.order CASCADE;
DROP TABLE IF EXISTS yanki.payment_method CASCADE;
DROP TABLE IF EXISTS yanki.shipping_address CASCADE;

-- Create Customer table --
CREATE TABLE yanki.customer (
    Customer_ID UUID PRIMARY KEY,
    Customer_Name TEXT,
    Email TEXT,
    Phone_Number TEXT
);


-- Create Product table --
CREATE TABLE yanki.product (
    Product_ID UUID PRIMARY KEY,
    Product_Name TEXT,
    Brand TEXT,
    Category TEXT,
    Price TEXT
);

-- Create Payment Method table --
CREATE TABLE yanki.shipping_address (
    Shipping_ID SERIAL PRIMARY KEY,
    Customer_ID UUID,
    Shipping_Address TEXT,
    City TEXT,
    State TEXT,
    Country TEXT,
    Postal_Code TEXT,
    CONSTRAINT fk_shipping_address_customer FOREIGN KEY (Customer_ID) REFERENCES yanki.customer(Customer_ID)
);

-- Create Order table --
CREATE TABLE yanki.orders (
    Order_ID UUID PRIMARY KEY,
    Customer_ID UUID,
    Product_ID UUID,
    Quantity INTEGER,
    Total_Price FLOAT,
    CONSTRAINT fk_order_customer FOREIGN KEY (Customer_ID) REFERENCES yanki.customer(Customer_ID),  
    CONSTRAINT fk_order_product FOREIGN KEY (Product_ID) REFERENCES yanki.product(Product_ID)   
);

-- Create Payment Method table --
CREATE TABLE yanki.payment_method (
    Order_ID UUID PRIMARY KEY,
    Payment_Method TEXT,
    Transaction_Status TEXT,
    CONSTRAINT fk_payment_method_order FOREIGN KEY (Order_ID) REFERENCES yanki.orders(Order_ID)
);


