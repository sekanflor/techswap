#!/bin/bash

# Replace with your actual JWT token
TOKEN="your_jwt_token_here"

# Make 101 requests
for i in {1..101}
do
    echo "Making request $i..."
    response=$(curl -s -w "\n%{http_code}" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        http://localhost:8000/api/user-profiles/)
    
    # Split response and status code
    body=$(echo "$response" | head -n -1)
    status=$(echo "$response" | tail -n 1)
    
    echo "Status Code: $status"
    
    if [ "$status" -eq 429 ]; then
        echo "Rate limit hit! Response:"
        echo "$body"
        break
    fi
    
    # Small delay
    sleep 0.1
done 