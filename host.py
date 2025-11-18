import psycopg2

conn_info = {
    "host": "aws-1-ap-southeast-1.pooler.supabase.com",
    "port": "6543",
    "dbname": "postgres",
    "user": "postgres.ppwvmujtrvxwlgxvfwny",
    "password": "mw60fV77ooK72B6D",
}

try:
    conn = psycopg2.connect(**conn_info)
    print("✅ Koneksi berhasil!")

    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM mytable;")
    count = cur.fetchone()[0]
    print(f"📊 Jumlah data: {count}")

    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")
