import requests

BASE_URL = "https://bookcart.azurewebsites.net/api"

def test_login_user(user_headers):
    headers, user_id = user_headers
    token = headers.get("Authorization")
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 10
    assert user_id is not None

def test_get_all_books(user_headers):
    headers, _ = user_headers
    url = f"{BASE_URL}/Book"
    r = requests.get(url, headers=headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) > 0

def test_add_book_to_cart(user_headers):
    headers, user_id = user_headers

    books_url = f"{BASE_URL}/Book"
    books_response = requests.get(books_url, headers=headers)
    assert books_response.status_code == 200

    book_id = books_response.json()[0]["bookId"]

    add_url = f"{BASE_URL}/ShoppingCart/AddToCart/{user_id}/{book_id}"
    add_response = requests.post(add_url, headers=headers)
    assert add_response.status_code == 200

def test_view_cart(user_headers):
    headers, user_id = user_headers
    url = f"{BASE_URL}/ShoppingCart/{user_id}"
    response = requests.get(url, headers=headers)
    assert response.status_code == 200

    cart_items = response.json()
    assert isinstance(cart_items, list)

def test_checkout_cart(user_headers):
    headers, user_id = user_headers
    url = f"{BASE_URL}/CheckOut/{user_id}"
    headers_with_content = headers.copy()
    headers_with_content["Content-Type"] = "application/json"

    response = requests.post(url, headers=headers_with_content)
    assert response.status_code == 200
