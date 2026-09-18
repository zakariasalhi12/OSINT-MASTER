import requests
class UsernameLookup :
    
    # request information
    requestTimeout = 5
    api = "https://api.ffraud.com/public/ip/"

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
        result = ""

        return result
    
    def lookup(self):
        try :
            response = requests.get(self.api , timeout=self.requestTimeout)
            
            data = response.json() 

            return self.result()

        except requests.exceptions.RequestException as error:
            raise error

