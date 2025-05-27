from lib.models.magazine import Magazine
from lib.models.author import Author

def test_magazine_contributors():
    magazine = Magazine.find_by_id(1)
    contributors = magazine.contributors()
    assert isinstance(contributors, list)
    assert all(isinstance(author, Author) for author in contributors)

def test_magazine_article_titles():
    magazine = Magazine.find_by_id(1)
    titles = magazine.article_titles()
    assert isinstance(titles, list)
    assert all(isinstance(title, str) for title in titles)
