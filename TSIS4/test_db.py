import psycopg2

try:
    conn = psycopg2.connect(
        dbname="snake_db",
        user="ernazartolegenov",
        password="",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()
    cur.execute("SELECT version();")

    print("✅ CONNECTED")
    print(cur.fetchone())

    cur.close()
    conn.close()

except Exception as e:
    print("❌ ERROR:", e)