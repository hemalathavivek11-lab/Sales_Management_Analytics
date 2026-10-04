from database import get_connection


connection = get_connection()
cursor = connection.cursor()

cursor.execute("SHOW TABLES")
rows = cursor.fetchall()

print("Tables in database:")
for row in rows:
    print(row[0])

connection.close()