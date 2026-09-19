import requests
import os
from datetime import datetime

class UsernameLookup :

    # instagram
    # Github
    # tiktok
    
    # request information
    requestTimeout = 120
    instagram_last_activity = "Unknown"
    
    apify_api_for_instagram_profile_info = "https://api.apify.com/v2/actors/apify~instagram-profile-scraper/run-sync-get-dataset-items?token="
    apify_api_for_instagram_profile_posts = "https://api.apify.com/v2/actors/apify~instagram-post-scraper/run-sync-get-dataset-items?token="

    apify_api_for_github_profile_info = "https://api.apify.com/v2/actors/kawsar~github-profile-scraper/run-sync-get-dataset-items?token="


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
        result = "Platform: Instagram\n"
        result += f"   - Profile URL: {self.instagram_input_url}\n"
        result += f"   - Username: {self.instagram_username}\n"
        result += f"   - Full name: {self.instagram_full_name}\n"
        result += f"   - Biography: {self.instagram_biography}\n"
        result += f"   - Profile picture: {self.instagram_profile_pic_url}\n"
        result += f"   - Followers: {self.instagram_followers_count}\n"
        result += f"   - Follows count: {self.instagram_follows_count}\n"
        result += f"   - Private account: {self.instagram_private}\n"
        result += f"   - Verified account: {self.instagram_verified}\n"
        result += f"   - Last activity: {self.instagram_last_activity}\n"

        result += "\nPlatform: GitHub\n"
        result += f"   - profileUrl: {self.github_profileUrl}\n"
        result += f"   - Username: {self.github_username}\n"
        result += f"   - Name: {self.github_name}\n"
        result += f"   - Biography: {self.github_bio}\n"
        result += f"   - Avatar URL: {self.github_avatarUrl}\n"
        result += f"   - Followers: {self.github_followers}\n"
        result += f"   - Following: {self.github_following}\n"
        result += f"   - Location: {self.github_location}\n"
        result += f"   - Public repositories: {self.github_publicRepos}\n"
        result += f"   - Account created at: {self.github_createdAt}\n"
        result += f"   - Last activity: {self.github_last_activity}\n"

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
                f"{self.apify_api_for_instagram_profile_posts}{APIFY_APIKEY}&fields=timestamp",
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
                f"{self.apify_api_for_instagram_profile_info}{APIFY_APIKEY}&fields=username,fullName,followsCount,followersCount,inputUrl,private,verified,profilePicUrlHD,biography",
                timeout=self.requestTimeout,
                headers={
                    "Content-Type": "application/json"
                },
                json=body
            )

            data = response.json()
            profile_info = data[0]

            self.instagram_username = profile_info.get("username", "Unknown")
            self.instagram_full_name = profile_info.get("fullName", "Unknown")
            self.instagram_followers_count = profile_info.get("followersCount", 0)
            self.instagram_input_url = profile_info.get("inputUrl", "Unknown")
            self.instagram_private = profile_info.get("private", False)
            self.instagram_verified = profile_info.get("verified", False)
            self.instagram_profile_pic_url = profile_info.get("profilePicUrlHD", "Unknown")
            self.instagram_biography = profile_info.get("biography", "Unknown")
            self.instagram_follows_count = profile_info.get("followsCount" , "Unknown")

            self.insatgram_lookup_posts()

        except requests.exceptions.RequestException as error:
            raise error

    def github_lookup(self):
        try:
            APIFY_APIKEY = os.getenv("APIFY_APIKEY")

            body = {
                "maxItems": 1,
                "requestTimeoutSecs": self.requestTimeout,
                "username": self.username
            }

            response = requests.post(
                f"{self.apify_api_for_github_profile_info}{APIFY_APIKEY}",
                timeout=self.requestTimeout,
                headers={
                    "Content-Type": "application/json"
                },
                json=body
            )
            
            data = response.json()
            profile_info = data[0]

            self.github_profileUrl = profile_info.get("profileUrl" , "Unknown")
            self.github_avatarUrl = profile_info.get("avatarUrl", "Unknown")
            self.github_username = profile_info.get("username", "Unknown")
            self.github_name = profile_info.get("name", "Unknown")
            self.github_bio = profile_info.get("bio", "Unknown")
            self.github_location = profile_info.get("location", "Unknown")
            self.github_followers = profile_info.get("followers", 0)
            self.github_following = profile_info.get("following", 0)
            self.github_publicRepos = profile_info.get("publicRepos", 0)
            self.github_createdAt = profile_info.get("createdAt", "Unknown")
            self.github_last_activity = profile_info.get("updatedAt", "Unknown")

        except requests.exceptions.RequestException as error:
            raise error

    
    def lookup(self):
        self.intagram_lookup()
        self.github_lookup()
        return self.result()

