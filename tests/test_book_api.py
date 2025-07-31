import requests

BASE_URL = "https://bookcart.azurewebsites.net/api"

def test_get_all_books():
    r = requests.get(f"{BASE_URL}/Book")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) > 0


def test_get_book_by_id():
    r = requests.get(f"{BASE_URL}/Book")
    assert r.status_code == 200
    books = r.json()
    book_id = books[0]["bookId"]

    r = requests.get(f"{BASE_URL}/Book/{book_id}")
    assert r.status_code == 200
    assert r.json()["bookId"] == book_id


def test_get_similar_books():
    r = requests.get(f"{BASE_URL}/Book")
    assert r.status_code == 200
    book_id = r.json()[0]["bookId"]

    r = requests.get(f"{BASE_URL}/Book/GetSimilarBooks/{book_id}")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_get_categories_list():
    r = requests.get(f"{BASE_URL}/Book/GetCategoriesList")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
