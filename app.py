from io import BytesIO

import pandas as pd
from flask import Flask, jsonify, render_template, request, send_file

from analytics import (
    get_analytics_overview,
    get_customers,
    get_dashboard_summary,
    get_orders,
    get_payments,
    get_products,
    get_reports,
)
from database import get_connection

app = Flask(__name__)


def execute_write(query, params):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query, params)
    connection.commit()
    inserted_id = cursor.lastrowid
    connection.close()
    return inserted_id


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/health")
def health():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        connection.close()
        return jsonify({"status": "ok", "database": "mysql"})
    except Exception as exc:  # pragma: no cover
        return jsonify({"status": "error", "message": str(exc)}), 500


@app.route("/api/dashboard")
def dashboard():
    return jsonify(get_dashboard_summary())


@app.route("/api/customers", methods=["GET", "POST"])
def customers_api():
    if request.method == "GET":
        return jsonify(get_customers())

    data = request.get_json(silent=True) or {}
    query = "INSERT INTO customers (name, email, city, signup_date) VALUES (%s, %s, %s, %s)"
    params = (data.get("name"), data.get("email"), data.get("city"), data.get("signup_date"))
    customer_id = execute_write(query, params)
    return jsonify({"message": "Customer added successfully.", "customer_id": customer_id}), 201


@app.route("/api/customers/<int:customer_id>", methods=["PUT", "DELETE"])
def customer_by_id(customer_id):
    if request.method == "PUT":
        data = request.get_json(silent=True) or {}
        query = "UPDATE customers SET name=%s, email=%s, city=%s, signup_date=%s WHERE customer_id=%s"
        params = (data.get("name"), data.get("email"), data.get("city"), data.get("signup_date"), customer_id)
        execute_write(query, params)
        return jsonify({"message": "Customer updated successfully."})

    query = "DELETE FROM customers WHERE customer_id=%s"
    execute_write(query, (customer_id,))
    return jsonify({"message": "Customer deleted successfully."})


@app.route("/api/products", methods=["GET", "POST"])
def products_api():
    if request.method == "GET":
        return jsonify(get_products())

    data = request.get_json(silent=True) or {}
    query = "INSERT INTO products (product_name, category, price, stock) VALUES (%s, %s, %s, %s)"
    params = (data.get("product_name"), data.get("category"), data.get("price"), data.get("stock"))
    product_id = execute_write(query, params)
    return jsonify({"message": "Product added successfully.", "product_id": product_id}), 201


@app.route("/api/products/<int:product_id>", methods=["PUT", "DELETE"])
def product_by_id(product_id):
    if request.method == "PUT":
        data = request.get_json(silent=True) or {}
        query = "UPDATE products SET product_name=%s, category=%s, price=%s, stock=%s WHERE product_id=%s"
        params = (data.get("product_name"), data.get("category"), data.get("price"), data.get("stock"), product_id)
        execute_write(query, params)
        return jsonify({"message": "Product updated successfully."})

    query = "DELETE FROM products WHERE product_id=%s"
    execute_write(query, (product_id,))
    return jsonify({"message": "Product deleted successfully."})


@app.route("/api/orders", methods=["GET", "POST"])
def orders_api():
    if request.method == "GET":
        return jsonify(get_orders())

    data = request.get_json(silent=True) or {}
    query = "INSERT INTO orders (customer_id, order_date, status, total_amount) VALUES (%s, %s, %s, %s)"
    params = (data.get("customer_id"), data.get("order_date"), data.get("status"), data.get("total_amount"))
    order_id = execute_write(query, params)
    return jsonify({"message": "Order added successfully.", "order_id": order_id}), 201


@app.route("/api/orders/<int:order_id>", methods=["PUT", "DELETE"])
def order_by_id(order_id):
    if request.method == "PUT":
        data = request.get_json(silent=True) or {}
        query = "UPDATE orders SET customer_id=%s, order_date=%s, status=%s, total_amount=%s WHERE order_id=%s"
        params = (data.get("customer_id"), data.get("order_date"), data.get("status"), data.get("total_amount"), order_id)
        execute_write(query, params)
        return jsonify({"message": "Order updated successfully."})

    query = "DELETE FROM orders WHERE order_id=%s"
    execute_write(query, (order_id,))
    return jsonify({"message": "Order deleted successfully."})


@app.route("/api/payments", methods=["GET", "POST"])
def payments_api():
    if request.method == "GET":
        return jsonify(get_payments())

    data = request.get_json(silent=True) or {}
    query = "INSERT INTO payments (order_id, payment_date, amount, payment_status) VALUES (%s, %s, %s, %s)"
    params = (data.get("order_id"), data.get("payment_date"), data.get("amount"), data.get("payment_status"))
    payment_id = execute_write(query, params)
    return jsonify({"message": "Payment added successfully.", "payment_id": payment_id}), 201


@app.route("/api/payments/<int:payment_id>", methods=["PUT", "DELETE"])
def payment_by_id(payment_id):
    if request.method == "PUT":
        data = request.get_json(silent=True) or {}
        query = "UPDATE payments SET order_id=%s, payment_date=%s, amount=%s, payment_status=%s WHERE payment_id=%s"
        params = (data.get("order_id"), data.get("payment_date"), data.get("amount"), data.get("payment_status"), payment_id)
        execute_write(query, params)
        return jsonify({"message": "Payment updated successfully."})

    query = "DELETE FROM payments WHERE payment_id=%s"
    execute_write(query, (payment_id,))
    return jsonify({"message": "Payment deleted successfully."})


@app.route("/api/analytics")
def analytics_api():
    return jsonify(get_analytics_overview())


@app.route("/api/reports")
def reports_api():
    return jsonify(get_reports())


@app.route("/api/reports/export")
def export_reports():
    report_data = get_reports()
    frames = []
    for section_name, rows in report_data.items():
        if rows:
            frame = pd.DataFrame(rows)
            frame.insert(0, "section", section_name)
            frames.append(frame)

    if not frames:
        empty = pd.DataFrame({"section": [], "value": []})
        output = BytesIO()
        empty.to_csv(output, index=False)
        output.seek(0)
        return send_file(output, mimetype="text/csv", as_attachment=True, download_name="sales_reports.csv")

    combined = pd.concat(frames, ignore_index=True)
    output = BytesIO()
    combined.to_csv(output, index=False)
    output.seek(0)
    return send_file(output, mimetype="text/csv", as_attachment=True, download_name="sales_reports.csv")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)