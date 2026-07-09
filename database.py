import sqlite3

DATABASE_NAME = "lyrics.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT,
        artist TEXT,
        album TEXT,
        release_year TEXT,

        genre TEXT,
        mood TEXT,
        emotion TEXT,
        theme TEXT,

        language TEXT,
        confidence TEXT,

        summary TEXT,

        favorite INTEGER DEFAULT 0

    )
    """)

    connection.commit()
    connection.close()


def save_analysis(data):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""

    INSERT INTO history(

        title,
        artist,
        album,
        release_year,

        genre,
        mood,
        emotion,
        theme,

        language,
        confidence,

        summary,
        favorite

    )

    VALUES(?,?,?,?,?,?,?,?,?,?,?,?)

    """,(

        data.get("title","Unknown"),
        data.get("artist","Unknown"),
        data.get("album","Unknown"),
        data.get("release_year","Unknown"),

        data.get("genre","Unknown"),
        data.get("mood","Unknown"),
        data.get("emotion","Unknown"),
        data.get("theme","Unknown"),

        data.get("language","Unknown"),
        data.get("confidence","Unknown"),

        data.get("summary","Unknown"),

        0

    ))

    connection.commit()
    connection.close()


def get_history():

    connection = get_connection()

    rows = connection.execute("""

    SELECT *

    FROM history

    ORDER BY id DESC

    """).fetchall()

    connection.close()

    return rows


def get_song(song_id):

    connection = get_connection()

    song = connection.execute("""

    SELECT *

    FROM history

    WHERE id=?

    """,(song_id,)).fetchone()

    connection.close()

    return song


def search_history(keyword):

    connection = get_connection()

    rows = connection.execute("""

    SELECT *

    FROM history

    WHERE

    title LIKE ?

    OR artist LIKE ?

    OR genre LIKE ?

    """,(

        f"%{keyword}%",

        f"%{keyword}%",

        f"%{keyword}%"

    )).fetchall()

    connection.close()

    return rows


def delete_song(song_id):

    connection = get_connection()

    connection.execute(
        "DELETE FROM history WHERE id=?",
        (song_id,)
    )

    connection.commit()
    connection.close()


def favorite_song(song_id):

    connection = get_connection()

    connection.execute(
        "UPDATE history SET favorite=1 WHERE id=?",
        (song_id,)
    )

    connection.commit()
    connection.close()


def get_favorites():

    connection = get_connection()

    rows = connection.execute("""

    SELECT *

    FROM history

    WHERE favorite=1

    ORDER BY id DESC

    """).fetchall()

    connection.close()

    return rows


def get_dashboard():

    connection = get_connection()
    cursor = connection.cursor()

    total = cursor.execute(
        "SELECT COUNT(*) FROM history"
    ).fetchone()[0]

    favorites = cursor.execute(
        "SELECT COUNT(*) FROM history WHERE favorite=1"
    ).fetchone()[0]

    latest = cursor.execute(
        "SELECT title FROM history ORDER BY id DESC LIMIT 1"
    ).fetchone()

    top_genre = cursor.execute("""

    SELECT genre

    FROM history

    GROUP BY genre

    ORDER BY COUNT(*) DESC

    LIMIT 1

    """).fetchone()

    top_mood = cursor.execute("""

    SELECT mood

    FROM history

    GROUP BY mood

    ORDER BY COUNT(*) DESC

    LIMIT 1

    """).fetchone()

    connection.close()

    return {

        "total": total,
        "favorites": favorites,
        "latest": latest["title"] if latest else "No Songs",
        "top_genre": top_genre["genre"] if top_genre else "Unknown",
        "top_mood": top_mood["mood"] if top_mood else "Unknown",
        "status": "Connected"

    }


# ---------- NEW FUNCTIONS ----------

def get_genre_stats():

    connection = get_connection()

    rows = connection.execute("""

    SELECT genre, COUNT(*) AS count

    FROM history

    GROUP BY genre

    ORDER BY count DESC

    """).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def get_mood_stats():

    connection = get_connection()

    rows = connection.execute("""

    SELECT mood, COUNT(*) AS count

    FROM history

    GROUP BY mood

    ORDER BY count DESC

    """).fetchall()

    connection.close()

    return [dict(row) for row in rows]