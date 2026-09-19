import requests
import os
from datetime import datetime

class UsernameLookup :

    # instagram
    # Github
    # tiktok
    
    # request information
    requestTimeout = 120
    apify_api_for_profile_info = "https://api.apify.com/v2/actors/apify~instagram-profile-scraper/run-sync-get-dataset-items?token="
    apify_api_for_profile_posts = "https://api.apify.com/v2/actors/apify~instagram-post-scraper/run-sync-get-dataset-items?token="

    def __init__(self, username):
        self.username = username
        if not self.username_validation():
            raise ValueError(f"Invalid username: {self.username}")

    def username_validation(self):
        try:
            return True
        except ValueError:
            return False

    def result(self):
        result = f"Platform: Instagram\n"

        result += f"   - Username: {self.username}\n"
        result += f"   - Full name: {self.full_name}\n"
        result += f"   - Followers: {self.followers_count}\n"
        result += f"   - followsCount: {self.follows_count}\n"
        result += f"   - Profile URL: {self.input_url}\n"
        result += f"   - Private account: {self.private}\n"
        result += f"   - Verified account: {self.verified}\n"
        result += f"   - Profile picture: {self.profile_pic_url}\n"
        result += f"   - Biography: {self.biography}\n"
        result += f"   - Last Activity : {self.last_activity}"

        return result


    def insatgram_lookup_posts(self):
        APIFY_APIKEY = os.getenv("APIFY_APIKEY")

        body = {
            "username": [
                self.username
            ],
            "resultsLimit" : 1,
            "dataDetailLevel": "basicData",
            "skipPinnedPosts": True,
        }

        response = requests.post(
                f"{self.apify_api_for_profile_posts}{APIFY_APIKEY}&fields=timestamp",
                timeout=self.requestTimeout,
                headers={
                    "Content-Type": "application/json"
                },
                json=body
            )

        data = response.json()

        if not data:
            self.last_activity = "Unknown"
            return

        timestamp = data[0].get("timestamp")

        if timestamp:
            post_date = datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            )

            self.last_activity = post_date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.last_activity = "Unknown"
        

    def intagram_lookup(self):
        try:
            APIFY_APIKEY = os.getenv("APIFY_APIKEY")

            body = {
                "usernames": [
                    self.username
                ],
            }

            response = requests.post(
                f"{self.apify_api_for_profile_info}{APIFY_APIKEY}&fields=username,fullName,followsCount,followersCount,inputUrl,private,verified,profilePicUrlHD,biography",
                timeout=self.requestTimeout,
                headers={
                    "Content-Type": "application/json"
                },
                json=body
            )

            response.raise_for_status()
            data = response.json()

            if not data:
                raise ValueError("No data found for this username")

            profile_info = data[0]

            self.username = profile_info.get("username", "Unknown")
            self.full_name = profile_info.get("fullName", "Unknown")
            self.followers_count = profile_info.get("followersCount", 0)
            self.input_url = profile_info.get("inputUrl", "Unknown")
            self.private = profile_info.get("private", False)
            self.verified = profile_info.get("verified", False)
            self.profile_pic_url = profile_info.get("profilePicUrlHD", "Unknown")
            self.biography = profile_info.get("biography", "Unknown")
            self.follows_count = profile_info.get("followsCount" , "Unknown")

            self.insatgram_lookup_posts()

            return self.result()

        except requests.exceptions.RequestException as error:
            raise error
    
    def lookup(self):
        self.intagram_lookup()
        return self.result()

