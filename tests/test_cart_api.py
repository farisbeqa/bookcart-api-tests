import requests

BASE_URL = "https://bookcart.azurewebsites.net/api"

def get_first_book_id():
    r = requests.get(f"{BASE_URL}/Book")
    assert r.status_code == 200, f"Failed to get books: {r.text}"
    return r.json()[0]["bookId"]

def test_add_to_cart_and_get_cart(user_headers):
    headers, user_id = user_headers
    book_id = get_first_book_id()

    data = {"userId": user_id, "bookId": book_id, "quantity": 2}
    r = requests.post(f"{BASE_URL}/ShoppingCart/AddToCart", json=data, headers=headers)
    assert r.status_code == 200

    r = requests.get(f"{BASE_URL}/ShoppingCart/{user_id}", headers=headers)
    assert r.status_code == 200
    cart_items = r.json()
    assert any(item["bookId"] == book_id for item in cart_items)

def test_update_cart_quantity(user_headers):
    headers, user_id = user_headers
    book_id = get_first_book_id()

    data = {"userId": user_id, "bookId": book_id, "quantity": 1}
    r = requests.post(f"{BASE_URL}/ShoppingCart/AddToCart", json=data, headers=headers)
    assert r.status_code == 200

    r = requests.put(f"{BASE_URL}/ShoppingCart/{user_id}/{book_id}?quantity=5", headers=headers)
    assert r.status_code == 200

    r = requests.get(f"{BASE_URL}/ShoppingCart/{user_id}", headers=headers)
    updated_item = next(item for item in r.json() if item["bookId"] == book_id)
    assert updated_item["quantity"] == 5

def test_delete_cart_item(user_headers):
    headers, user_id = user_headers
    book_id = get_first_book_id()

    data = {"userId": user_id, "bookId": book_id, "quantity": 1}
    r = requests.post(f"{BASE_URL}/ShoppingCart/AddToCart", json=data, headers=headers)
    assert r.status_code == 200

    r = requests.delete(f"{BASE_URL}/ShoppingCart/{user_id}/{book_id}", headers=headers)
    assert r.status_code == 200

    r = requests.get(f"{BASE_URL}/ShoppingCart/{user_id}", headers=headers)
    cart_items = r.json()
    assert not any(item["bookId"] == book_id for item in cart_items)
