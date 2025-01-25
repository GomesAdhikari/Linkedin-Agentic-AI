import requests
from datetime import datetime
from Oauth import auth, headers
from src.phidata import main

# Your LinkedIn API credentials file
credentials = 'credentials.json'
access_token = auth(credentials)  # Authenticate the API
headers = headers(access_token)  # Create headers to attach to the API call.

def user_info(headers):
    '''
    Get user information from LinkedIn
    '''
    response = requests.get('https://api.linkedin.com/v2/userinfo', headers=headers)
    user_info = response.json()
    return user_info

# Get user id to make a UGC post
user_info = user_info(headers)
urn = user_info['sub']

# UGC will replace shares over time.
api_url = 'https://api.linkedin.com/v2/ugcPosts'
author = f'urn:li:person:{urn}'

# Custom message you want to post
message = main()
message = message['news_content']

post_data = {
    "author": author,
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": message  # The custom message you want to post
            },
            "shareMediaCategory": "NONE"  # Add this line to resolve the 422 error
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}

if __name__ == '__main__':
    r = requests.post(api_url, headers=headers, json=post_data)
    if r.status_code in [200, 201]:
        print("Post successful!")
    else:
        print(f"Failed to post. Status Code: {r.status_code}")
    
    # Print the response body to inspect further details
    print("Response JSON:", r.json())