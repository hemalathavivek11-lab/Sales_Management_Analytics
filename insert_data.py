from database import get_connection


def insert_sample_data():
    connection = get_connection()
    cursor = connection.cursor()

    customers = [
        ("Arun Kumar", "arun.kumar@gmail.com", "Chennai", "2024-01-10"),
        ("Priya Sharma", "priya.sharma@gmail.com", "Bangalore", "2024-01-16"),
        ("Rahul Verma", "rahul.verma@gmail.com", "Delhi", "2024-02-03"),
        ("Divya Nair", "divya.nair@gmail.com", "Kochi", "2024-02-15"),
        ("Karthik Iyer", "karthik.iyer@gmail.com", "Hyderabad", "2024-03-01"),
        ("Meena Devi", "meena.devi@gmail.com", "Madurai", "2024-03-06"),
        ("Vijay Kumar", "vijay.kumar@gmail.com", "Trichy", "2024-03-20"),
        ("Anitha Reddy", "anitha.reddy@gmail.com", "Pune", "2024-04-04"),
        ("Sanjay Patel", "sanjay.patel@gmail.com", "Ahmedabad", "2024-04-18"),
        ("Nisha Menon", "nisha.menon@gmail.com", "Thiruvananthapuram", "2024-05-02"),
        ("Rohan Singh", "rohan.singh@gmail.com", "Lucknow", "2024-05-10"),
        ("Swathi Rao", "swathi.rao@gmail.com", "Mysore", "2024-05-28"),
    ]

    cursor.executemany(
        "INSERT INTO customers (name, email, city, signup_date) VALUES (%s, %s, %s, %s)",
        customers,
    )

    products = [
        ("Dell Inspiron Laptop", "Electronics", 54000.00, 18),
        ("Wireless Mouse", "Accessories", 850.00, 75),
        ("Mechanical Keyboard", "Accessories", 2200.00, 40),
        ("Noise Headphones", "Electronics", 3200.00, 28),
        ("USB-C Cable", "Accessories", 450.00, 120),
        ("Dell Monitor 24 inch", "Electronics", 12800.00, 14),
        ("Webcam 4K", "Electronics", 4800.00, 22),
        ("Laptop Sleeve", "Accessories", 1600.00, 36),
        ("HP Printer", "Office", 9500.00, 12),
        ("Smartphone Stand", "Accessories", 650.00, 90),
        ("Portable SSD 1TB", "Electronics", 9800.00, 16),
        ("Wireless Charger", "Accessories", 1200.00, 48),
    ]

    cursor.executemany(
        "INSERT INTO products (product_name, category, price, stock) VALUES (%s, %s, %s, %s)",
        products,
    )

    orders = [
        (1, "2024-06-01", "COMPLETED", 54650.00),
        (2, "2024-06-03", "COMPLETED", 4200.00),
        (3, "2024-06-05", "PENDING", 9800.00),
        (4, "2024-06-07", "COMPLETED", 15800.00),
        (5, "2024-06-09", "COMPLETED", 2500.00),
        (6, "2024-06-12", "CANCELLED", 3200.00),
        (7, "2024-06-14", "COMPLETED", 12150.00),
        (8, "2024-06-16", "COMPLETED", 7400.00),
        (9, "2024-06-20", "COMPLETED", 1800.00),
        (10, "2024-06-23", "PENDING", 6000.00),
        (11, "2024-07-01", "COMPLETED", 6800.00),
        (12, "2024-07-04", "COMPLETED", 18900.00),
        (13, "2024-07-08", "COMPLETED", 4700.00),
        (14, "2024-07-11", "CANCELLED", 2200.00),
        (15, "2024-07-15", "COMPLETED", 13500.00),
        (16, "2024-07-18", "COMPLETED", 9800.00),
        (17, "2024-07-20", "PENDING", 4300.00),
        (18, "2024-08-02", "COMPLETED", 16400.00),
        (19, "2024-08-05", "COMPLETED", 3100.00),
        (20, "2024-08-08", "COMPLETED", 22850.00),
    ]

    cursor.executemany(
        "INSERT INTO orders (customer_id, order_date, status, total_amount) VALUES (%s, %s, %s, %s)",
        orders,
    )

    order_items = [
        (1, 1, 1, 54650.00),
        (1, 2, 1, 850.00),
        (2, 4, 1, 3200.00),
        (2, 3, 2, 2200.00),
        (3, 5, 1, 9800.00),
        (4, 6, 1, 12800.00),
        (4, 7, 1, 4800.00),
        (5, 8, 1, 1600.00),
        (5, 10, 1, 650.00),
        (6, 9, 1, 9500.00),
        (7, 1, 1, 54000.00),
        (8, 2, 1, 850.00),
        (8, 4, 1, 3200.00),
        (9, 3, 1, 2200.00),
        (10, 11, 1, 9800.00),
        (10, 2, 1, 850.00),
        (11, 8, 2, 3200.00),
        (12, 6, 1, 12800.00),
        (12, 12, 1, 1200.00),
        (13, 10, 1, 650.00),
        (13, 5, 1, 450.00),
        (14, 9, 1, 9500.00),
        (15, 11, 1, 9800.00),
        (15, 1, 1, 54000.00),
        (16, 2, 2, 1700.00),
        (16, 3, 1, 2200.00),
        (17, 7, 1, 4800.00),
        (17, 9, 1, 9500.00),
        (18, 6, 1, 12800.00),
        (18, 4, 1, 3200.00),
        (19, 10, 2, 1300.00),
        (20, 1, 1, 54000.00),
        (20, 11, 1, 9800.00),
    ]

    cursor.executemany(
        "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s, %s, %s, %s)",
        order_items,
    )

    payments = [
        (1, "2024-06-01", 54650.00, "PAID"),
        (2, "2024-06-03", 4200.00, "PAID"),
        (3, "2024-06-05", 9800.00, "PENDING"),
        (4, "2024-06-07", 15800.00, "PAID"),
        (5, "2024-06-09", 2500.00, "PAID"),
        (6, "2024-06-12", 3200.00, "REFUNDED"),
        (7, "2024-06-14", 12150.00, "PAID"),
        (8, "2024-06-16", 7400.00, "PAID"),
        (9, "2024-06-20", 1800.00, "PAID"),
        (10, "2024-06-23", 6000.00, "PENDING"),
        (11, "2024-07-01", 6800.00, "PAID"),
        (12, "2024-07-04", 18900.00, "PAID"),
        (13, "2024-07-08", 4700.00, "PAID"),
        (14, "2024-07-11", 2200.00, "REFUNDED"),
        (15, "2024-07-15", 13500.00, "PAID"),
        (16, "2024-07-18", 9800.00, "PAID"),
        (17, "2024-07-20", 4300.00, "PENDING"),
        (18, "2024-08-02", 16400.00, "PAID"),
        (19, "2024-08-05", 3100.00, "PAID"),
        (20, "2024-08-08", 22850.00, "PAID"),
    ]

    cursor.executemany(
        "INSERT INTO payments (order_id, payment_date, amount, payment_status) VALUES (%s, %s, %s, %s)",
        payments,
    )

    connection.commit()
    print("Sample data inserted successfully.")
    connection.close()


if __name__ == "__main__":
    insert_sample_data()