from lib.scripts.setup_db import get_connection

class Article:
    def __init__(self, title, content, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute("""
                UPDATE articles SET title = ?, content = ?, author_id = ?, magazine_id = ?
                WHERE id = ?
            """, (self.title, self.content, self.author_id, self.magazine_id, self.id))
        else:
            cursor.execute("""
                INSERT INTO articles (title, content, author_id, magazine_id)
                VALUES (?, ?, ?, ?)
            """, (self.title, self.content, self.author_id, self.magazine_id))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @classmethod
    def get_all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles")
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row[0], title=row[1], content=row[2], author_id=row[3], magazine_id=row[4]) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row[0], title=row[1], content=row[2], author_id=row[3], magazine_id=row[4])
        return None

    def author(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (self.author_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        from lib.models.author import Author
        return Author(id=row[0], name=row[1], email=row[2])

    def magazine(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (self.magazine_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        from lib.models.magazine import Magazine
        return Magazine(id=row[0], name=row[1], category=row[2])

    def __repr__(self):
        return f"<Article '{self.title}' by Author {self.author_id} in Magazine {self.magazine_id}>"

    def __eq__(self, other):
        if not isinstance(other, Article):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
