import requests
import time

BASE_URL = "https://bookcart.azurewebsites.net/api"


def generate_random_user():
    import random
    import string
    username = "user" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    password = "Testing123"
    return {
        "firstName": "Test",
        "lastName": "User",
        "userName": username,
        "password": password,
        "confirmPassword": password,
        "gender": "Male"
    }


def test_register_user_success():
    user_data = generate_random_user()
    response = requests.post(f"{BASE_URL}/User", json=user_data)
    print("Register response:", response.status_code, response.text)
    assert response.status_code == 200


def test_validate_username_taken():
    user_data = generate_random_user()
    requests.post(f"{BASE_URL}/User", json=user_data)

    max_attempts = 5
    for i in range(max_attempts):
        time.sleep(1)
        response = requests.get(f"{BASE_URL}/User/validateUserName/{user_data['userName']}")
        print(f"Attempt {i+1}: {response.status_code}, {response.text}")
        if response.status_code == 200 and response.json() is False:
            break
    else:
        assert False, "Username should be marked as taken after registration"


def test_login_success():
    user_data = generate_random_user()
    requests.post(f"{BASE_URL}/User", json=user_data)

    login_data = {
        "userName": user_data["userName"],
        "password": user_data["password"]
    }
    response = requests.post(f"{BASE_URL}/Login", json=login_data)
    print("Login response:", response.status_code, response.text)
    assert response.status_code == 200
    assert "token" in response.json()
