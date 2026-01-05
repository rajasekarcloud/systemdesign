#!/bin/bash

ALB_DNS="http://<ALB_DNS>"
SHORT_KEY="<SHORT_KEY>"

# Function to fetch a long URL using a short key
fetch_url() {
    SHORT_KEY=$1
    RESPONSE=$(curl -s -X GET "$ALB_DNS/fetch_url/$SHORT_KEY")
    
    if echo "$RESPONSE" | grep -q "long_url"; then
        echo "Fetched URL: $RESPONSE"
    else
        echo "Error fetching URL: $RESPONSE"
    fi
}

# Function to delete a short URL using a short key
delete_url() {
    SHORT_KEY=$1
    RESPONSE=$(curl -s -X DELETE "$ALB_DNS/delete_url/$SHORT_KEY")
    
    if echo "$RESPONSE" | grep -q "deleted successfully"; then
        echo "Short URL deleted successfully"
    else
        echo "Error deleting URL: $RESPONSE"
    fi
}

echo "Fetching URL for short key: $SHORT_KEY"
fetch_url "$SHORT_KEY"

echo "Deleting URL for short key: $SHORT_KEY"
delete_url "$SHORT_KEY"
