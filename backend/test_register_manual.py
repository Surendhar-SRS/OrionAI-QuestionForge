import requests
import sys


def test_register():
    url = "http://localhost:8000/api/auth/register"
    data = {
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User",
    }

    print(f"Testing registration against {url}...")
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            print("SUCCESS: Registration worked!")
        elif response.status_code == 400 and "already exists" in response.text:
            print("SUCCESS: User already exists (Backend is reachable)")
        else:
            print("FAILURE: Unexpected response")
            sys.exit(1)

    except Exception as e:
        print(f"FAILURE: Could not connect to backend. Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    test_register()
