from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine

def test_article_author_and_magazine():
    article = Article.get_all()[0]
    assert isinstance(article.author(), Author)
    assert isinstance(article.magazine(), Magazine)

def test_article_title_presence():
    article = Article.get_all()[0]
    assert isinstance(article.title, str)
    assert len(article.title) > 0
