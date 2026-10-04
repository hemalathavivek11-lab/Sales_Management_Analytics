from database import get_connection


def show_query_plan(title, query):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"EXPLAIN {query}")
    rows = cursor.fetchall()
    print("\n" + "=" * 90)
    print(title)
    print("=" * 90)
    for row in rows:
        print(row)
    connection.close()


def main():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_order_date ON orders(order_date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_payments_order_id ON payments(order_id)")
    connection.commit()

    print("MySQL indexes created successfully.")

    print("\nSales summary view:")
    cursor.execute("SELECT * FROM sales_summary ORDER BY order_id LIMIT 5")
    for row in cursor.fetchall():
        print(row)

    print("\nProduct sales view:")
    cursor.execute("SELECT * FROM product_sales ORDER BY revenue DESC LIMIT 5")
    for row in cursor.fetchall():
        print(row)

    connection.close()

    show_query_plan(
        "EXPLAIN - ORDER QUERY USING CUSTOMER INDEX",
        "SELECT * FROM orders WHERE customer_id = 1"
    )

    show_query_plan(
        "EXPLAIN - PAYMENT FILTER USING ORDER INDEX",
        "SELECT * FROM payments WHERE order_id = 5"
    )

    print("\nOptimization completed successfully.")


if __name__ == "__main__":
    main()