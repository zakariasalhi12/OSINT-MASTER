import requests
import os

class UsernameLookup :
    # request information
    requestTimeout = 120
    instagram_last_activity = "Unknown"

    # API's used for this tool
    apify_api_for_instagram_profile_info = "https://api.apify.com/v2/actors/apify~instagram-profile-scraper/run-sync-get-dataset-items?token="
    apify_api_for_instagram_profile_posts = "https://api.apify.com/v2/actors/apify~instagram-post-scraper/run-sync-get-dataset-items?token="
    apify_api_for_github_profile_info = "https://api.apify.com/v2/actors/kawsar~github-profile-scraper/run-sync-get-dataset-items?token="
    apify_api_for_tiktok_profile_info = "https://api.apify.com/v2/actors/fetch_cat~tiktok-profile-scraper/run-sync-get-dataset-items?token="
    apify_api_for_x_profile_info = "https://api.apify.com/v2/actors/igview-owner~x-twitter-profile-viewer/run-sync-get-dataset-items?token="
    apify_api_for_linkedin_profile_info = "https://api.apify.com/v2/actors/harvestapi~linkedin-profile-scraper/run-sync-get-dataset-items?token="

    
    def __init__(self, username):
        self.username = username
        if not self.username_validation():
            raise ValueError(f"Invalid username: {self.username}")

    def username_validation(self):
        # Validate that the username is not empty and contains no spaces
        try:
            if not self.username:
                return False

            if not isinstance(self.username, str):
                return False

            if " " in self.username:
                return False

            return True

        except (TypeError, ValueError):
            return False

    # Format the collected information for display
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
        result += f"   - Profile URL: {self.github_profileUrl}\n"
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
    
        result += "\nPlatform: X\n"
        result += f"   - Profile URL: {self.x_profile_url}\n"
        result += f"   - Username: {self.x_username}\n"
        result += f"   - Name: {self.x_name}\n"
        result += f"   - Biography: {self.x_bio}\n"
        result += f"   - Profile image: {self.x_profile_image}\n"
        result += f"   - Profile banner: {self.x_profile_banner}\n"
        result += f"   - Followers: {self.x_followers_count}\n"
        result += f"   - Following: {self.x_following_count}\n"
        result += f"   - Tweets count: {self.x_tweets_count}\n"
    
        result += "\nPlatform: TikTok\n"
        result += f"   - Profile URL: {self.tiktok_profileUrl}\n"
        result += f"   - Handle: {self.tiktok_handle}\n"
        result += f"   - Nickname: {self.tiktok_nickname}\n"
        result += f"   - Followers: {self.tiktok_followers}\n"
        result += f"   - Following: {self.tiktok_following}\n"
        result += f"   - Bio link: {self.tiktok_bioLink}\n"
        result += f"   - Video count: {self.tiktok_video_count}\n"
        result += f"   - Currently live: {self.tiktok_is_live}\n"
    
        result += "\nPlatform: LinkedIn\n"
        result += f"   - Public identifier: {self.linkedin_publicIdentifier}\n"
        result += f"   - LinkedIn URL: {self.linkedin_linkedinUrl}\n"
        result += f"   - First name: {self.linkedin_firstName}\n"
        result += f"   - Last name: {self.linkedin_lastName}\n"
        result += f"   - Headline: {self.linkedin_headline}\n"
        result += f"   - Connections count: {self.linkedin_connectionsCount}\n"
        result += f"   - Follower count: {self.linkedin_followerCount}\n"
        result += f"   - About: {self.linkedin_about}\n"
        result += f"   - Video count: {self.linkedin_video_count}\n"
        result += f"   - Currently live: {self.linkedin_is_live}\n"
    
        return result

    def instagram_lookup_posts(self):
        try :
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

            if not isinstance(data, list) or not data:
                profile_info = {}
            else:
                profile_info = data[0]

            self.last_activity = profile_info.get("timestamp" , "Unknown")

        except requests.exceptions.RequestException as error:
            raise error


    def instagram_lookup(self):
        try:
            APIFY_APIKEY = os.getenv("APIFY_APIKEY")

            body = {
                "usernames": [
                    self.username
                ],
            }

            # send request with field that i need
            response = requests.post(
                f"{self.apify_api_for_instagram_profile_info}{APIFY_APIKEY}&fields=username,fullName,followsCount,followersCount,inputUrl,private,verified,profilePicUrlHD,biography",
                timeout=self.requestTimeout,
                headers={
                    "Content-Type": "application/json"
                },
                json=body
            )

            data = response.json()

            # check if result is list if not then the request must be failed
            if not isinstance(data, list) or not data:
                profile_info = {}
            else:
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

            self.instagram_lookup_posts()

        except requests.exceptions.RequestException as error:
            raise error


    def tiktok_lookup(self):
        try:
            APIFY_APIKEY = os.getenv("APIFY_APIKEY")

            body = {
                "handles": [
                    self.username
                ],
                "includeRecentVideos": True,
                "maxVideosPerProfile": 1,
                "maxProfiles": 1,
                "maxConcurrency": 1,
                "runTimeSecs": 180,
                "proxyConfiguration": {
                    "useApifyProxy": True
                }
            }

            response = requests.post(
                f"{self.apify_api_for_tiktok_profile_info}{APIFY_APIKEY}",
                timeout=self.requestTimeout,
                headers={
                    "Content-Type": "application/json"
                },
                json=body
            )
            
            data = response.json()

            # check if result is list if not then the request must be failed
            if not isinstance(data, list) or not data:
                profile_info = {}
            else:
                profile_info = data[0]

            self.tiktok_profileUrl = profile_info.get("profileUrl" , "Unknown")
            self.tiktok_handle = profile_info.get("handle" , "Unknown")
            self.tiktok_nickname = profile_info.get("nickname", "Unknown")
            self.tiktok_followers = profile_info.get("followers", 0)
            self.tiktok_following = profile_info.get("following", 0)
            self.tiktok_bioLink = profile_info.get("bioLink", "Unknown")
            self.tiktok_video_count = profile_info.get("videosCount", 0)
            self.tiktok_is_live = profile_info.get("isLive", False)

        except requests.exceptions.RequestException as error:
            raise error



    def linkedin_lookup(self):
        try:
            APIFY_APIKEY = os.getenv("APIFY_APIKEY")

            body = {
                "profileScraperMode": "Profile details no email ($4 per 1k)",
                "queries": [
                    f"https://www.linkedin.com/in/{self.username}"
                ]
            }

            response = requests.post(
                f"{self.apify_api_for_linkedin_profile_info}{APIFY_APIKEY}",
                timeout=self.requestTimeout,
                headers={
                    "Content-Type": "application/json"
                },
                json=body
            )

            data = response.json()

            # check if result is list if not then the request must be failed
            if not isinstance(data, list) or not data:
                profile_info = {}
            else:
                profile_info = data[0]

            self.linkedin_publicIdentifier = profile_info.get("publicIdentifier" , "Unknown")
            self.linkedin_linkedinUrl = profile_info.get("linkedinUrl" , "Unknown")
            self.linkedin_firstName = profile_info.get("firstName", "Unknown")
            self.linkedin_lastName = profile_info.get("lastName", "Unknown")
            self.linkedin_headline = profile_info.get("headline", "Unknown")
            self.linkedin_connectionsCount = profile_info.get("connectionsCount", 0)
            self.linkedin_followerCount = profile_info.get("followerCount", 0)
            self.linkedin_about = profile_info.get("about", "Unknown")
            self.linkedin_video_count = profile_info.get("videosCount", 0)
            self.linkedin_is_live = profile_info.get("isLive", False)

        except requests.exceptions.RequestException as error:
            raise error

    def x_lookup(self):
        try:
            APIFY_APIKEY = os.getenv("APIFY_APIKEY")

            body = {
                "usernames": [
                    self.username
                ]
            }

            response = requests.post(
                f"{self.apify_api_for_x_profile_info}{APIFY_APIKEY}",
                timeout=self.requestTimeout,
                headers={
                    "Content-Type": "application/json"
                },
                json=body
            )
            
            data = response.json()

            # check if result is list if not then the request must be failed
            if not isinstance(data, list) or not data:
                profile_info = {}
            else:
                profile_info = data[0]

            self.x_profile_url = profile_info.get("profile_url" , "Unknown")
            self.x_username = profile_info.get("username" , "Unknown")
            self.x_name = profile_info.get("name", "Unknown")
            self.x_followers_count = profile_info.get("followers_count", 0)
            self.x_following_count = profile_info.get("following_count", 0)
            self.x_profile_image = profile_info.get("profile_image", "Unknown")
            self.x_profile_banner = profile_info.get("profile_banner", "Unknown")
            self.x_tweets_count = profile_info.get("tweets_count", 0)
            self.x_bio= profile_info.get("bio", "Unknown")

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

            # check if result is list if not then the request must be failed
            if not isinstance(data, list) or not data:
                profile_info = {}
            else:
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

    # Extract all the information from Github , Linkedin , Tiktok , Github , x (Twitter)
    def lookup(self):
        self.linkedin_lookup()
        self.tiktok_lookup()
        self.github_lookup()
        self.x_lookup()
        self.instagram_lookup()
        return self.result()

