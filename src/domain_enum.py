import requests
import os
import re
import socket

class DomainEnum :
    
    # request information
    requestTimeout = 5
    whois_api = "https://api.who.is/v1/whois/"

    def __init__(self, domain):
        self.domain = domain
        if not self.domain_validation():
            raise ValueError(f"Invalid Domain: {self.domain}")

    def get_ip(self):
        try:
            return socket.gethostbyname(self.domain)
        except socket.gaierror:
            return "Unknown"

    def domain_validation(self):
        try:
            domain = self.domain.strip().lower()

            pattern = r"^(?!-)(?:[a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,63}$"

            if not re.match(pattern, domain):
                return False

            return True

        except (AttributeError, TypeError):
            return False

    def result(self):
        result = f"Main Domain: {self.domain}\n\n"

        result += "General informations:\n"
        result += f"Whois_server: {self.whois_server}\n"
        result += f"IP address: {self.get_ip()}\n\n"
        result += f"Registrar: {self.registrar}\n\n"
        
        result += "Admin informations:\n"
        result += f"Admin Name: {self.admin['name']}\n"
        result += f"Admin Phone: {self.admin['phone']}\n"
        result += f"Admin Email: {self.admin['email']}\n\n"

        result += "Domain Events:\n"

        for event, date in self.events.items():
            result += f"{event}: {date}\n"

        return result

    def enumeration(self):
        try:
            WHOIS_APIKEY = os.getenv("WHOIS_APIKEY")

            response = requests.get(
                self.whois_api + self.domain,
                timeout=self.requestTimeout,
                headers={
                    "Authorization": f"Bearer {WHOIS_APIKEY}"
                }
            )

            data = response.json()

            self.whois_server = data.get("whois_server", "Unknown")
            self.registrar = data.get("registrar", "Unknown")

            contacts = data.get("contacts", {})
            admin = contacts.get("admin", {})
            events = data.get("events", [])

            self.admin = {
                "name": admin.get("name", "Unknown"),
                "phone": admin.get("phone", "Unknown"),
                "email": admin.get("email", "Unknown")
            }

            self.events = {}

            for event in events:
                action = event.get("event_action", "Unknown")
                date = event.get("event_date", "Unknown")

                self.events[action] = date

            return self.result()

        except Exception as e:
            raise e

