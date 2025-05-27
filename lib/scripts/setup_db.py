import sqlite3

DB_PATH = 'articles.db'  # Use a file DB or ':memory:' for tests

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    with open('lib/db/schema.sql', 'r') as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()

def seed_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        DELETE FROM articles;
        DELETE FROM authors;
        DELETE FROM magazines;

        INSERT INTO authors (name, email)
        VALUES
            ('Alice Smith', 'alice@example.com'),
            ('Bob Johnson', 'bob@example.com');

        INSERT INTO magazines (name, category)
        VALUES
            ('Tech Today', 'Technology'),
            ('Health Weekly', 'Health');

        INSERT INTO articles (title, content, author_id, magazine_id)
        VALUES
            ('AI and You', 'All about AI.', 1, 1),
            ('The Future of Health', 'How tech helps health.', 1, 2),
            ('Wellness Hacks', 'Simple health tips.', 2, 2);
    """)
    conn.commit()
    conn.close()

def setup_database():
    create_tables()
    seed_database()
