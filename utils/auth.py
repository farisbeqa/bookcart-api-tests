import requests
from utils.config import BASE_URL, USERNAME, PASSWORD

def get_token():
    url = f"{BASE_URL}/Login"
    payload = {
        "userName": USERNAME,
        "password": PASSWORD
    }

    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Login failed: {response.text}"

    data = response.json()
    token = data["token"]
    user_id = data["userDetails"]["userId"]
    return token, user_id
