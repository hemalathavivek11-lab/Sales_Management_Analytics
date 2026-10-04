# Sales & Order Management Analytics System

A MySQL-backed sales and order analytics web application built with Python, Flask, HTML, CSS, JavaScript, Chart.js, and Pandas. The project is designed for a college project submission and is intended to run locally with MySQL Server and MySQL Workbench.

## Features

- Customer, product, order, and payment management
- Dashboard metrics and chart visualizations
- Sales analytics and revenue reports
- Advanced SQL examples using MySQL
- Index and optimization examples
- CSV export of reports
- API-based frontend data loading

## Tech Stack

- Python
- Flask
- MySQL
- MySQL Workbench
- HTML
- CSS
- JavaScript
- Chart.js
- Pandas

## Project Structure

- `app.py` – Flask application and API endpoints
- `database.py` – MySQL connection and schema creation
- `schema.sql` – MySQL table, view, and index definitions
- `insert_data.py` – sample data insertion script
- `analytics.py` – dashboard and analytics queries
- `advanced_sql.py` – analysis of advanced MySQL queries
- `database_optimization.py` – index and optimization examples
- `crud.py` – CRUD demonstration for MySQL
- `templates/index.html` – dashboard UI
- `static/style.css` – styling
- `static/script.js` – frontend logic and charts

## Local Setup

1. Install MySQL Server and MySQL Workbench.
2. Create a database named `sales_management` in MySQL Workbench or run the schema script.
3. Update `.env` with your local MySQL credentials.
4. Create and activate a Python virtual environment.
5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Create the database schema:

   ```bash
   python database.py
   ```

7. Insert sample data:

   ```bash
   python insert_data.py
   ```

8. Start the Flask app:

   ```bash
   python app.py
   ```

9. Open the app in your browser:

   ```text
   http://localhost:5000
   ```

## MySQL Workbench Setup

- Open MySQL Workbench.
- Connect to your local MySQL Server instance.
- Create a schema named `sales_management`.
- Run the SQL from `schema.sql` if needed.
- Verify that the following tables exist:
  - customers
  - products
  - orders
  - order_items
  - payments

## Environment Configuration

Edit `.env` before running the app:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=sales_management
```

## API Endpoints

- `GET /api/dashboard`
- `GET /api/customers`
- `POST /api/customers`
- `PUT /api/customers/<id>`
- `DELETE /api/customers/<id>`
- `GET /api/products`
- `POST /api/products`
- `PUT /api/products/<id>`
- `DELETE /api/products/<id>`
- `GET /api/orders`
- `POST /api/orders`
- `PUT /api/orders/<id>`
- `DELETE /api/orders/<id>`
- `GET /api/payments`
- `POST /api/payments`
- `PUT /api/payments/<id>`
- `DELETE /api/payments/<id>`
- `GET /api/analytics`
- `GET /api/reports`
- `GET /api/reports/export`

## Notes

This project has been implemented to use MySQL as the database layer and does not rely on SQLite.
