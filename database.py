import sqlite3

DB_NAME = "events.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        
        source TEXT,
        company TEXT,
        actors TEXT,
       
         event_date TEXT,
        location TEXT,
        
        ticket_sale TEXT,
        summary TEXT,
        
        url TEXT,
        embedding TEXT
    )
    """)

    conn.commit()
    conn.close()


from embeddings import get_embedding, cosine_similarity


def is_duplicate(new_embedding, threshold=0.85):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT embedding FROM events WHERE embedding IS NOT NULL")

    existing = cursor.fetchall()

    conn.close()

    for (emb,) in existing:

        try:
            score = cosine_similarity(new_embedding, emb)

            if score >= threshold:
                return True

        except:
            continue

    return False


def save_event(data):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO events (
        source,
        company,
        actors,
        event_date,
        location,
        ticket_sale,
        summary,
        url,
        embedding

    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        data.get("source", ""),
        data.get("company", ""),
        ", ".join(data.get("actors", [])),
        data.get("date", ""),
        data.get("location", ""),
        str(data.get("ticket_sale", False)),
        data.get("summary", ""),
        data.get("url", ""),
        data.get("embedding", "")

    ))

    conn.commit()
    conn.close()


def get_events():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM events
    ORDER BY event_date ASC
    """)

    events = cursor.fetchall()

    conn.close()

    return events

def get_event(event_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM events WHERE id = ?",
        (event_id,)
    )

    event = cursor.fetchone()

    conn.close()

    return event


def search_events(query):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM events
    WHERE actors LIKE ?
    OR summary LIKE ?
    OR location LIKE ?
    ORDER BY event_date ASC
    """, (f"%{query}%", f"%{query}%", f"%{query}%"))

    results = cursor.fetchall()

    conn.close()

    return results

def get_upcoming_events():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM events
    WHERE event_date >= date('now')
    ORDER BY event_date ASC
    """)

    events = cursor.fetchall()

    conn.close()

    return events