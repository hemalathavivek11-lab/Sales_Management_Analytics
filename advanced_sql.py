from database import get_connection


def run_query(title, query, params=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params or ())
    rows = cursor.fetchall()

    print("\n" + "=" * 90)
    print(title)
    print("=" * 90)

    if rows:
        columns = list(rows[0].keys())
        print(" | ".join(columns))
        print("-" * 90)
        for row in rows:
            print(tuple(row.values()))
    else:
        print("No rows returned.")

    connection.close()


def main():
    run_query(
        "1. INNER JOIN - CUSTOMER ORDERS",
        """
        SELECT c.name AS customer_name, o.order_id, o.order_date, o.status, o.total_amount
        FROM customers c
        INNER JOIN orders o ON c.customer_id = o.customer_id
        ORDER BY o.order_id
        """,
    )

    run_query(
        "2. LEFT JOIN - ALL CUSTOMERS INCLUDING THOSE WITHOUT ORDERS",
        """
        SELECT c.name AS customer_name, COUNT(o.order_id) AS order_count
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.name
        ORDER BY order_count DESC
        """,
    )

    run_query(
        "3. MULTI-TABLE JOIN - ORDER ITEMS + PRODUCTS",
        """
        SELECT o.order_id, c.name AS customer_name, p.product_name, oi.quantity, oi.unit_price
        FROM orders o
        INNER JOIN customers c ON c.customer_id = o.customer_id
        INNER JOIN order_items oi ON oi.order_id = o.order_id
        INNER JOIN products p ON p.product_id = oi.product_id
        ORDER BY o.order_id
        """,
    )

    run_query(
        "4. SUBQUERY - CUSTOMERS WITH ABOVE-AVERAGE TOTAL SALES",
        """
        SELECT c.name, c.customer_id
        FROM customers c
        WHERE c.customer_id IN (
            SELECT o.customer_id
            FROM orders o
            WHERE o.status = 'COMPLETED'
            GROUP BY o.customer_id
            HAVING SUM(o.total_amount) > (
                SELECT AVG(total_sales)
                FROM (
                    SELECT SUM(total_amount) AS total_sales
                    FROM orders
                    WHERE status = 'COMPLETED'
                    GROUP BY customer_id
                ) sales_summary
            )
        )
        ORDER BY c.customer_id
        """,
    )

    run_query(
        "5. CTE - CUSTOMER SALES SUMMARY",
        """
        WITH customer_sales AS (
            SELECT customer_id, SUM(total_amount) AS total_sales
            FROM orders
            WHERE status = 'COMPLETED'
            GROUP BY customer_id
        )
        SELECT c.name, cs.total_sales
        FROM customer_sales cs
        INNER JOIN customers c ON c.customer_id = cs.customer_id
        ORDER BY cs.total_sales DESC
        """,
    )

    run_query(
        "6. CASE - ORDER VALUE CLASSIFICATION",
        """
        SELECT order_id, total_amount,
               CASE
                   WHEN total_amount >= 20000 THEN 'HIGH VALUE'
                   WHEN total_amount >= 5000 THEN 'MEDIUM VALUE'
                   ELSE 'LOW VALUE'
               END AS order_category
        FROM orders
        ORDER BY total_amount DESC
        """,
    )

    run_query(
        "7. WINDOW FUNCTION - RANK CUSTOMERS",
        """
        SELECT c.name,
               SUM(o.total_amount) AS total_sales,
               RANK() OVER (ORDER BY SUM(o.total_amount) DESC) AS sales_rank
        FROM customers c
        INNER JOIN orders o ON o.customer_id = c.customer_id
        WHERE o.status = 'COMPLETED'
        GROUP BY c.customer_id, c.name
        """,
    )

    run_query(
        "8. WINDOW FUNCTION - ROW_NUMBER OVER ORDERS",
        """
        SELECT order_id, total_amount,
               ROW_NUMBER() OVER (ORDER BY total_amount DESC) AS order_rank
        FROM orders
        """,
    )

    run_query(
        "9. WINDOW FUNCTION - RUNNING TOTAL",
        """
        SELECT order_date, total_amount,
               SUM(total_amount) OVER (ORDER BY order_date) AS running_total
        FROM orders
        WHERE status = 'COMPLETED'
        ORDER BY order_date
        """,
    )

    run_query(
        "10. MY SQL DATE FUNCTIONS - MONTHLY REVENUE",
        """
        SELECT DATE_FORMAT(order_date, '%Y-%m') AS month,
               SUM(total_amount) AS monthly_revenue,
               COUNT(order_id) AS order_count
        FROM orders
        WHERE status = 'COMPLETED'
        GROUP BY DATE_FORMAT(order_date, '%Y-%m')
        ORDER BY month
        """,
    )

    run_query(
        "11. TOP PRODUCTS BY SALES",
        """
        SELECT p.product_name, SUM(oi.quantity * oi.unit_price) AS revenue
        FROM products p
        INNER JOIN order_items oi ON p.product_id = oi.product_id
        INNER JOIN orders o ON o.order_id = oi.order_id
        WHERE o.status = 'COMPLETED'
        GROUP BY p.product_id, p.product_name
        ORDER BY revenue DESC
        LIMIT 5
        """,
    )


if __name__ == "__main__":
    main()