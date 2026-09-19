import requests
import os
import re
import socket
from datetime import datetime
class DomainEnum :
    
    # request information
    requestTimeout = 120
    whois_api = "https://api.who.is/v1/whois/"
    crt_api = "https://crt.sh/?q=%25."
    canopystack_api = "https://canopystack.dev/api/subdomain-takeover?host="

    def __init__(self, domain):
        self.domain = domain
        if not self.domain_validation():
            raise ValueError(f"Invalid Domain: {self.domain}")

    def get_ip(self, domain):
        try:
            return socket.gethostbyname(domain)
        except socket.gaierror:
            return "Unknown"

    def domain_validation(self):
        try:
            domain = self.domain.strip().lower() # remove spaces and make the domain in lower case
            pattern = r"^(?!-)(?:[a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,63}$" # regex pattern to check if the domain is valid

            if not re.match(pattern, domain):
                return False

            return True

        except (AttributeError, TypeError):
            return False

    # Format the collected information for display 
    def result(self):
        result = f"Main Domain: {self.domain}\n\n"

        result += "General informations:\n"
        result += f"  - Whois_server: {self.whois_server}\n"
        result += f"  - IP address: {self.get_ip(self.domain)}\n"
        result += f"  - Registrar: {self.registrar}\n\n"
        
        result += "Admin informations:\n"
        result += f"  - Admin Name: {self.admin['name']}\n"
        result += f"  - Admin Phone: {self.admin['phone']}\n"
        result += f"  - Admin Email: {self.admin['email']}\n\n"

        result += "Domain Events:\n"

        for event, date in self.events.items():
            result += f"  - {event}: {date}\n"

        result += "\n"
        result += "Subdomains and ssl details:\n"

        for domain, certificate in sorted(self.sub_domains.items()):
            result += f"  - Domain: {domain}\n"
            result += f"  - certificate Expiration date: {certificate['not_after']}\n"
            result += f"  - certificate Issuer: {certificate['issuer_name']}\n"
            result += f"  - IP address : {self.get_ip(domain)}\n"
            result += "-" * 50 + "\n"

        result += "Potential Subdomain Takeover Risks:\n"

        for scan in self.scan_result:
            result += f"  - Host: {scan['requestedHost']}\n"
            result += f"  - Details: {scan['detail']}\n"
            result += "\n"

        return result

    def who_is(self):
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
        except Exception as e:
            raise e

    def find_subdomains(self):
        try:
            self.scan_result = []

            for domain, _ in sorted(self.sub_domains.items()):

                response = requests.get(
                    self.canopystack_api + domain,
                    timeout=self.requestTimeout,
                )

                response.raise_for_status()
                data = response.json()

                result = {
                    "requestedHost": data.get("requestedHost", "Unknown"),
                    "detail": data.get("detail", "Unknown")
                }

                self.scan_result.append(result)

        except Exception as e:
            raise e
        
    def subdomain_takeover_scan(self):
        try:
            response = requests.get(
                self.crt_api + self.domain + "&output=json&exclude=expired&deduplicate=Y",
                timeout=self.requestTimeout,
            )

            response.raise_for_status()
            data = response.json()

            self.sub_domains = {}

            for certificate in data:
                names = certificate.get("name_value", "").splitlines()
                certificate_date = datetime.fromisoformat(certificate["not_before"])

                for name in names:
                    name = name.strip().lower()

                    if not name or name.startswith("*."):
                        continue

                    # Keep only the newest certificate for this domain
                    if (name not in self.sub_domains or certificate_date > self.sub_domains[name]["not_before"]):
                        self.sub_domains[name] = {
                            "not_before": certificate_date,
                            "not_after": certificate.get(
                                "not_after", "Unknown"
                            ),
                            "issuer_name": certificate.get(
                                "issuer_name", "Unknown"
                            ),
                        }

        except Exception as e:
            raise e

    def enumeration(self):
        self.who_is()
        self.subdomain_takeover_scan()
        self.find_subdomains()
        return self.result()

