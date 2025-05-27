from lib.models.author import Author
from lib.models.article import Article

def test_author_has_articles():
    author = Author.find_by_id(1)
    articles = author.articles()
    assert isinstance(articles, list)
    assert all(isinstance(article, Article) for article in articles)
    assert len(articles) > 0

def test_author_magazines():
    author = Author.find_by_id(1)
    magazines = author.magazines()
    names = [m.name for m in magazines]
    assert "Tech Today" in names or "Health Weekly" in names

def test_author_write_article():
    author = Author.find_by_id(1)
    magazine = author.magazines()[0]
    article = author.write_article(magazine, "New Discovery")
    assert article in author.articles()
    assert article.title == "New Discovery"
