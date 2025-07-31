import requests

BASE_URL = "https://bookcart.azurewebsites.net/api"


def test_get_empty_wishlist(user_headers):
    headers, user_id = user_headers
    r = requests.get(f"{BASE_URL}/Wishlist/{user_id}", headers=headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) == 0


def test_add_and_remove_from_wishlist(user_headers_with_cart):
    headers, user_id = user_headers_with_cart

    r = requests.get(f"{BASE_URL}/Book")
    assert r.status_code == 200
    book_id = r.json()[0]["bookId"]

    r = requests.post(f"{BASE_URL}/Wishlist/ToggleWishlist/{user_id}/{book_id}", headers=headers)
    assert r.status_code == 200

    r = requests.get(f"{BASE_URL}/Wishlist/{user_id}", headers=headers)
    assert r.status_code == 200
    wishlist = r.json()
    assert any(book["bookId"] == book_id for book in wishlist)

    r = requests.post(f"{BASE_URL}/Wishlist/ToggleWishlist/{user_id}/{book_id}", headers=headers)
    assert r.status_code == 200

    r = requests.get(f"{BASE_URL}/Wishlist/{user_id}", headers=headers)
    assert r.status_code == 200
    wishlist = r.json()
    assert all(book["bookId"] != book_id for book in wishlist)


def test_delete_wishlist(user_headers_with_cart):
    headers, user_id = user_headers_with_cart

    r = requests.get(f"{BASE_URL}/Book")
    assert r.status_code == 200
    book_id = r.json()[0]["bookId"]

    r = requests.post(f"{BASE_URL}/Wishlist/ToggleWishlist/{user_id}/{book_id}", headers=headers)
    assert r.status_code == 200

    r = requests.delete(f"{BASE_URL}/Wishlist/{user_id}", headers=headers)
    assert r.status_code == 200

    r = requests.get(f"{BASE_URL}/Wishlist/{user_id}", headers=headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) == 0


def test_delete_empty_wishlist(user_headers):
    headers, user_id = user_headers

    r = requests.get(f"{BASE_URL}/Wishlist/{user_id}", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) == 0

    r = requests.delete(f"{BASE_URL}/Wishlist/{user_id}", headers=headers)
    assert r.status_code == 200

    r = requests.get(f"{BASE_URL}/Wishlist/{user_id}", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) == 0


def test_multiple_books_in_wishlist(user_headers_with_cart):
    headers, user_id = user_headers_with_cart

    r = requests.get(f"{BASE_URL}/Book")
    assert r.status_code == 200
    books = r.json()[:3]

    for book in books:
        r = requests.post(f"{BASE_URL}/Wishlist/ToggleWishlist/{user_id}/{book['bookId']}", headers=headers)
        assert r.status_code == 200

    r = requests.get(f"{BASE_URL}/Wishlist/{user_id}", headers=headers)
    assert r.status_code == 200
    wishlist = r.json()
    wishlist_ids = [b["bookId"] for b in wishlist]

    for book in books:
        assert book["bookId"] in wishlist_ids

    for book in books:
        r = requests.post(f"{BASE_URL}/Wishlist/ToggleWishlist/{user_id}/{book['bookId']}", headers=headers)
        assert r.status_code == 200

    r = requests.get(f"{BASE_URL}/Wishlist/{user_id}", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) == 0
