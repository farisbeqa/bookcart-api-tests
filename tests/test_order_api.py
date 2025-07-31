import requests
import time

BASE_URL = "https://bookcart.azurewebsites.net/api"


def test_checkout_and_order_history(user_headers_with_cart):
    headers, user_id = user_headers_with_cart

    cart_resp = requests.get(f"{BASE_URL}/ShoppingCart/{user_id}", headers=headers)
    print("[CART CONTENT]", cart_resp.status_code, cart_resp.text)
    assert cart_resp.status_code == 200
    cart_data = cart_resp.json()
    assert len(cart_data) > 0

    cart_item = cart_data[0]
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
    print("[CHECKOUT]", r.status_code, r.text)
    assert r.status_code == 200

    time.sleep(1)

    r = requests.get(f"{BASE_URL}/Order/{user_id}", headers=headers)
    print("[ORDER HISTORY]", r.status_code, r.text)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) > 0


def test_checkout_with_empty_payload_should_fail(user_headers_with_cart):
    headers, user_id = user_headers_with_cart

    r = requests.post(f"{BASE_URL}/CheckOut/{user_id}", headers=headers, json={})
    print("[NEGATIVE CHECKOUT]", r.status_code, r.text)
    assert r.status_code in [400, 500]


def test_checkout_without_auth_should_fail(user_headers_with_cart):
    _, user_id = user_headers_with_cart

    r = requests.post(f"{BASE_URL}/CheckOut/{user_id}", json={})
    print("[CHECKOUT WITHOUT AUTH]", r.status_code, r.text)
    assert r.status_code == 401


def test_checkout_with_invalid_user_should_fail(user_headers_with_cart):
    headers, _ = user_headers_with_cart

    invalid_user_id = 999999
    r = requests.post(f"{BASE_URL}/CheckOut/{invalid_user_id}", headers=headers, json={})
    print("[CHECKOUT INVALID USER]", r.status_code, r.text)
    assert r.status_code in [400, 404, 500]
