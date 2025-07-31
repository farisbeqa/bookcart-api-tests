import pytest
import requests
import random
import string
import time

BASE_URL = "https://bookcart.azurewebsites.net/api"


def _register_and_login():
    username = "user" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    password = "Testing123"
    user_data = {
        "firstName": "Tester",
        "lastName": "Pytest",
        "userName": username,
        "password": password,
        "confirmPassword": password,
        "gender": "Male",
        "role": "User"
    }

    r = requests.post(f"{BASE_URL}/User", json=user_data)
    assert r.status_code == 200, f"[REGISTER FAIL] {r.status_code} - {r.text}"

    for _ in range(5):
        r = requests.post(f"{BASE_URL}/Login", json={"userName": username, "password": password})
        if r.status_code == 200:
            break
        time.sleep(1)

    assert r.status_code == 200, f"[LOGIN FAIL] {r.status_code} - {r.text}"
    res = r.json()

    token = res["token"]
    user_id = res["userDetails"]["userId"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    return headers, user_id


@pytest.fixture
def user_headers():
    headers, user_id = _register_and_login()
    return headers, user_id


@pytest.fixture
def user_headers_with_cart():
    headers, user_id = _register_and_login()

    r = requests.get(f"{BASE_URL}/Book")
    assert r.status_code == 200
    book_id = r.json()[0]["bookId"]

    r = requests.post(f"{BASE_URL}/ShoppingCart/AddToCart/{user_id}/{book_id}", headers=headers)
    assert r.status_code in [200, 409]

    return headers, user_id
