import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user=" ",
    password=" ",
    port="5432"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
print(cursor.fetchall())
conn.close()