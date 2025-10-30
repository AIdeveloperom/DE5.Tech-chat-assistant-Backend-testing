import requests

# Test the /chat endpoint
def test_chat_endpoint():
    url = "http://127.0.0.1:8000/chat"
    payload = {
        "message": "What is DE5?",
        "user_id": "test_user"
    }
    response = requests.post(url, json=payload)
    print(f"Chat endpoint status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

# Test the /leads endpoint
def test_leads_endpoint():
    url = "http://127.0.0.1:8000/leads"
    payload = {
        "name": "John Doe",
        "email": "john@example.com",
        "inquiry_type": "investor"
    }
    response = requests.post(url, json=payload)
    print(f"Leads endpoint status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

# Test the root endpoint
def test_root_endpoint():
    url = "http://127.0.0.1:8000/"
    response = requests.get(url)
    print(f"Root endpoint status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

if __name__ == "__main__":
    print("Testing DE5 Chat Assistant Backend endpoints...")
    chat_ok = test_chat_endpoint()
    leads_ok = test_leads_endpoint()
    root_ok = test_root_endpoint()
    if chat_ok and leads_ok and root_ok:
        print("All tests passed!")
    else:
        print("Some tests failed.")
