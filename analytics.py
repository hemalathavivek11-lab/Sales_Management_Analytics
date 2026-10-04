from database import get_connection


def fetch_records(query, params=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params or ())
    rows = cursor.fetchall()
    connection.close()
    return rows


def fetch_scalar(query, params=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params or ())
    row = cursor.fetchone()
    connection.close()
    if row is None:
        return 0
    return next(iter(row.values()))


def get_dashboard_summary():
    revenue = fetch_scalar("SELECT COALESCE(SUM(total_amount),0) AS total FROM orders WHERE status = 'COMPLETED'")
    total_orders = fetch_scalar("SELECT COUNT(*) AS total FROM orders")
    total_customers = fetch_scalar("SELECT COUNT(*) AS total FROM customers")
    total_products = fetch_scalar("SELECT COUNT(*) AS total FROM products")
    avg_order_value = fetch_scalar("SELECT COALESCE(AVG(total_amount),0) AS total FROM orders WHERE status = 'COMPLETED'")
    recent_orders = fetch_records(
        """
        SELECT o.order_id, c.name AS customer_name, o.order_date, o.status, o.total_amount
        FROM orders o
        INNER JOIN customers c ON c.customer_id = o.customer_id
        ORDER BY o.order_id DESC
        LIMIT 10
        """
    )

    return {
        "total_revenue": float(revenue),
        "total_orders": int(total_orders),
        "total_customers": int(total_customers),
        "total_products": int(total_products),
        "average_order_value": float(avg_order_value),
        "recent_orders": recent_orders,
        "monthly_revenue": fetch_records(
            """
            SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, SUM(total_amount) AS revenue
            FROM orders
            WHERE status = 'COMPLETED'
            GROUP BY DATE_FORMAT(order_date, '%Y-%m')
            ORDER BY month
            """
        ),
        "top_products": fetch_records(
            """
            SELECT p.product_name, SUM(oi.quantity * oi.unit_price) AS revenue
            FROM order_items oi
            INNER JOIN products p ON p.product_id = oi.product_id
            INNER JOIN orders o ON o.order_id = oi.order_id
            WHERE o.status = 'COMPLETED'
            GROUP BY p.product_id, p.product_name
            ORDER BY revenue DESC
            LIMIT 5
            """
        ),
        "sales_by_category": fetch_records(
            """
            SELECT p.category, SUM(oi.quantity * oi.unit_price) AS revenue
            FROM order_items oi
            INNER JOIN products p ON p.product_id = oi.product_id
            INNER JOIN orders o ON o.order_id = oi.order_id
            WHERE o.status = 'COMPLETED'
            GROUP BY p.category
            ORDER BY revenue DESC
            """
        ),
        "order_status_summary": fetch_records(
            "SELECT status, COUNT(*) AS total FROM orders GROUP BY status ORDER BY total DESC"
        ),
        "payment_status_summary": fetch_records(
            "SELECT payment_status, COUNT(*) AS total, SUM(amount) AS value FROM payments GROUP BY payment_status ORDER BY total DESC"
        ),
        "top_customers": fetch_records(
            """
            SELECT c.name AS customer_name, SUM(o.total_amount) AS total_sales
            FROM customers c
            INNER JOIN orders o ON o.customer_id = c.customer_id
            WHERE o.status = 'COMPLETED'
            GROUP BY c.customer_id, c.name
            ORDER BY total_sales DESC
            LIMIT 5
            """
        ),
    }


def get_analytics_overview():
    return {
        "revenue_by_month": fetch_records(
            "SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, SUM(total_amount) AS revenue FROM orders WHERE status='COMPLETED' GROUP BY month ORDER BY month"
        ),
        "top_products": fetch_records(
            "SELECT p.product_name, SUM(oi.quantity) AS units_sold, SUM(oi.quantity * oi.unit_price) AS revenue FROM order_items oi INNER JOIN products p ON p.product_id = oi.product_id INNER JOIN orders o ON o.order_id = oi.order_id WHERE o.status='COMPLETED' GROUP BY p.product_id, p.product_name ORDER BY revenue DESC LIMIT 10"
        ),
        "top_customers": fetch_records(
            "SELECT c.name AS customer_name, SUM(o.total_amount) AS revenue FROM customers c INNER JOIN orders o ON o.customer_id = c.customer_id WHERE o.status='COMPLETED' GROUP BY c.customer_id, c.name ORDER BY revenue DESC LIMIT 10"
        ),
        "sales_by_category": fetch_records(
            "SELECT p.category, SUM(oi.quantity * oi.unit_price) AS revenue FROM order_items oi INNER JOIN products p ON p.product_id = oi.product_id INNER JOIN orders o ON o.order_id = oi.order_id WHERE o.status='COMPLETED' GROUP BY p.category ORDER BY revenue DESC"
        ),
        "units_sold": fetch_scalar("SELECT COALESCE(SUM(quantity),0) FROM order_items"),
        "average_order_value": fetch_scalar("SELECT COALESCE(AVG(total_amount),0) FROM orders WHERE status='COMPLETED'"),
        "repeat_customers": fetch_scalar("SELECT COUNT(*) FROM (SELECT customer_id FROM orders GROUP BY customer_id HAVING COUNT(order_id) > 1) t"),
        "minimum_order_value": fetch_scalar("SELECT COALESCE(MIN(total_amount),0) FROM orders WHERE status='COMPLETED'"),
        "maximum_order_value": fetch_scalar("SELECT COALESCE(MAX(total_amount),0) FROM orders WHERE status='COMPLETED'"),
        "order_status_analysis": fetch_records("SELECT status, COUNT(*) AS total FROM orders GROUP BY status ORDER BY total DESC"),
        "payment_status_analysis": fetch_records("SELECT payment_status, COUNT(*) AS total, SUM(amount) AS value FROM payments GROUP BY payment_status ORDER BY total DESC"),
    }


def get_reports():
    return {
        "sales_summary": fetch_records("SELECT * FROM sales_summary ORDER BY order_id"),
        "customer_sales_report": fetch_records("SELECT * FROM customer_sales ORDER BY total_sales DESC"),
        "product_sales_report": fetch_records("SELECT * FROM product_sales ORDER BY revenue DESC"),
        "monthly_sales_report": fetch_records("SELECT * FROM monthly_revenue ORDER BY month"),
        "order_status_report": fetch_records("SELECT status, COUNT(*) AS total_orders, SUM(total_amount) AS revenue FROM orders GROUP BY status ORDER BY total_orders DESC"),
        "payment_report": fetch_records("SELECT payment_status, COUNT(*) AS total_payments, SUM(amount) AS total_paid FROM payments GROUP BY payment_status ORDER BY total_paid DESC"),
    }


def get_customers():
    return fetch_records("SELECT * FROM customers ORDER BY customer_id")


def get_products():
    return fetch_records("SELECT * FROM products ORDER BY product_id")


def get_orders():
    return fetch_records(
        """
        SELECT o.order_id, o.customer_id, c.name AS customer_name, o.order_date, o.status, o.total_amount
        FROM orders o
        INNER JOIN customers c ON c.customer_id = o.customer_id
        ORDER BY o.order_id
        """
    )


def get_payments():
    return fetch_records(
        "SELECT payment_id, order_id, payment_date, amount, payment_status FROM payments ORDER BY payment_id"
    )