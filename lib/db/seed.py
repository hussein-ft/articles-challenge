from lib.db.connection import CONN, CURSOR

def seed_database():
    CURSOR.executescript("""
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

    CONN.commit()
    print("🌱 Database seeded successfully.")

if __name__ == "__main__":
    seed_database()