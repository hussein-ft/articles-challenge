# lib/models/author.py

from lib.scripts.setup_db import get_connection

class Author:
    def __init__(self, name, email, id=None):
        self.id = id
        self.name = name
        self.email = email

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute("UPDATE authors SET name = ?, email = ? WHERE id = ?", (self.name, self.email, self.id))
        else:
            cursor.execute("INSERT INTO authors (name, email) VALUES (?, ?)", (self.name, self.email))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @classmethod
    def get_all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors")
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row[0], name=row[1], email=row[2]) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls(id=row[0], name=row[1], email=row[2]) if row else None

    def articles(self):
        from lib.models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(id=row[0], title=row[1], content=row[2], author_id=row[3], magazine_id=row[4]) for row in rows]

    def magazines(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON a.magazine_id = m.id
            WHERE a.author_id = ?
        """, (self.id,))
        from lib.models.magazine import Magazine
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(id=row[0], name=row[1], category=row[2]) for row in rows]

    def write_article(self, magazine, title):
        from lib.models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
            (title, "", self.id, magazine.id)
        )
        conn.commit()
        article_id = cursor.lastrowid
        conn.close()
        return Article.find_by_id(article_id)

    def __repr__(self):
        return f"<Author {self.name} ({self.email})>"
