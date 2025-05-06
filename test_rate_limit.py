import requests
import time

# Replace with your actual API URL
BASE_URL = 'http://localhost:8000/api'

# Replace with your actual JWT token
headers = {
    'Authorization': 'Bearer your_jwt_token_here',
    'Content-Type': 'application/json'
}

def test_rate_limit():
    print("Testing rate limit...")
    print("Making 101 requests to trigger rate limit...")
    
    # Make 101 requests (1 more than the limit)
    for i in range(101):
        response = requests.get(f'{BASE_URL}/user-profiles/', headers=headers)
        print(f"Request {i+1}: Status Code = {response.status_code}")
        
        if response.status_code == 429:
            print("\nRate limit hit! Response:")
            print(response.json())
            break
        
        # Small delay to make the output readable
        time.sleep(0.1)

if __name__ == "__main__":
    test_rate_limit() 