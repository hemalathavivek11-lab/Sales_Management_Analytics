from database import get_connection


def get_customers():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers ORDER BY customer_id")
    rows = cursor.fetchall()
    connection.close()
    return rows


def add_customer(name, email, city, signup_date):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO customers (name, email, city, signup_date) VALUES (%s, %s, %s, %s)",
        (name, email, city, signup_date),
    )
    connection.commit()
    connection.close()
    print("Customer inserted successfully!")


def update_customer(customer_id, city):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE customers SET city = %s WHERE customer_id = %s", (city, customer_id))
    connection.commit()
    connection.close()
    print("Customer updated successfully!")


def delete_customer(customer_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
    connection.commit()
    connection.close()
    print("Customer deleted successfully!")


if __name__ == "__main__":
    print("\n1. INSERT")
    add_customer("Demo Customer", "demo.customer@gmail.com", "Coimbatore", "2024-10-12")

    print("\n2. SELECT")
    for row in get_customers():
        print(row)

    print("\n3. UPDATE")
    update_customer(1, "Madurai")

    print("\n4. DELETE")
    delete_customer(1)

    print("\n5. FINAL LIST")
    for row in get_customers():
        print(row)
