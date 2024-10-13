import tweepy
import requests
import time

# X API credentials
API_KEY = 'Xvp1atYrypF9wwv63Eo3pUBai'
API_SECRET_KEY = 'M4FsDJSe4qgYEvUiVggCsxz9g1f9gciUmI6jr9Ol1SHbFBTTlP'
ACCESS_TOKEN = '1845087675889360911-VavxKomFJOzViVHKUAaA9NUldtbyKJ'
ACCESS_TOKEN_SECRET = 'qrSm12sMf21npcf9HF0mk4AjT7S1Q4ja6KZFsTWVIifeA'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAL17wQEAAAAAZiKXjXM7jgdSs870VmPG82g6Bmc%'

# TheCatAPI credentials
CAT_API_KEY = 'live_WiBSTzo5U6c9sE76X1FyEsBsqkOaI9Eq9mBKNQl3ftSXktCRQPmiRXvUrj8HjmfG'

# Authenticate to X
client = tweepy.Client(bearer_token=BEARER_TOKEN, 
                       consumer_key=API_KEY, 
                       consumer_secret=API_SECRET_KEY, 
                       access_token=ACCESS_TOKEN, 
                       access_token_secret=ACCESS_TOKEN_SECRET)

def get_cat_image():
    headers = {'x-api-key': CAT_API_KEY}
    try:
        response = requests.get("https://api.thecatapi.com/v1/images/search", headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        image_url = response.json()[0]['url']
        image_response = requests.get(image_url)
        image_response.raise_for_status()  # Check for HTTP errors
        with open("cat.jpg", "wb") as file:
            file.write(image_response.content)
        return "cat.jpg"
    except requests.RequestException as e:
        print(f"Error fetching cat image: {e}")
        return None

def post_cat_picture():
    cat_image_path = get_cat_image()
    if cat_image_path:
        try:
            # Upload the image
            media_upload_url = "https://upload.twitter.com/1.1/media/upload.json"
            files = {'media': open(cat_image_path, 'rb')}
            response = requests.post(media_upload_url, headers={'Authorization': f'Bearer {BEARER_TOKEN}'}, files=files)
            print("Media Upload Response:", response.text)  # Debugging print
            media_id = response.json().get('media_id_string')

            if media_id:
                # Post the tweet with the image
                tweet_url = "https://api.twitter.com/2/tweets"
                payload = {
                    "text": "Here’s a cat picture!",
                    "media": {
                        "media_ids": [media_id]
                    }
                }
                headers = {
                    'Authorization': f'Bearer {BEARER_TOKEN}',
                    'Content-Type': 'application/json'
                }
                response = requests.post(tweet_url, headers=headers, json=payload)
                print("Tweet Post Response:", response.text)  # Debugging print
                if response.status_code == 201:
                    print("First, we conquer the couch. Then, the world!")
                else:
                    print(f"Error posting to X: {response.json()}")
            else:
                print(f"Error uploading media: {response.json()}")

        except requests.RequestException as e:
            print(f"Error posting to X: {e}")

def main():
    while True:
        post_cat_picture()
        time.sleep(1800)  # Post every 30 minutes

if __name__ == "__main__":
    main()
