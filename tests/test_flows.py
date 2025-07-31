import requests
import time

BASE_URL = "https://bookcart.azurewebsites.net/api"

def test_full_user_flow(user_headers_with_cart):
    headers, user_id = user_headers_with_cart

    r = requests.get(f"{BASE_URL}/Book", headers=headers)
    assert r.status_code == 200
    books = r.json()
    assert len(books) > 0
    first_book_id = books[0]["bookId"]

    r = requests.post(f"{BASE_URL}/Wishlist/ToggleWishlist/{user_id}/{first_book_id}", headers=headers)
    assert r.status_code == 200

    r = requests.get(f"{BASE_URL}/Wishlist/{user_id}", headers=headers)
    assert r.status_code == 200
    wishlist = r.json()
    assert any(book["bookId"] == first_book_id for book in wishlist)

    r = requests.get(f"{BASE_URL}/ShoppingCart/{user_id}", headers=headers)
    assert r.status_code == 200
    cart_items = r.json()
    assert len(cart_items) > 0

    cart_item = cart_items[0]
    book = cart_item["book"]
    quantity = cart_item["quantity"]
    cart_total = book["price"] * quantity

    checkout_payload = {
        "orderDetails": [
            {
                "book": book,
                "quantity": quantity
            }
        ],
        "cartTotal": cart_total
    }

    r = requests.post(f"{BASE_URL}/CheckOut/{user_id}", headers=headers, json=checkout_payload)
    assert r.status_code == 200

    time.sleep(1)

    r = requests.get(f"{BASE_URL}/Order/{user_id}", headers=headers)
    assert r.status_code == 200
    orders = r.json()
    assert isinstance(orders, list)
    assert len(orders) > 0

    r = requests.post(f"{BASE_URL}/Wishlist/ToggleWishlist/{user_id}/{first_book_id}", headers=headers)
    assert r.status_code == 200

    r = requests.get(f"{BASE_URL}/Wishlist/{user_id}", headers=headers)
    assert r.status_code == 200
    wishlist = r.json()
    assert all(book["bookId"] != first_book_id for book in wishlist)
