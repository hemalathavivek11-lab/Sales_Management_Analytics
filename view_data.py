from database import get_connection


connection = get_connection()
cursor = connection.cursor()

for table_name in ["customers", "products", "orders", "order_items", "payments"]:
    print(f"\n{table_name.upper()}")
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 10")
    for row in cursor.fetchall():
        print(row)

connection.close()