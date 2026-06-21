import sqlite3

conn = sqlite3.connect("events.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE events ADD COLUMN embedding TEXT;
""")

conn.commit()
conn.close()

print("Column added!")