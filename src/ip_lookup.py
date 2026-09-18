import requests
import ipaddress
class IPLookup :
    
    # request information
    requestTimeout = 5
    api = "https://api.ffraud.com/public/ip/"

    def __init__(self, ip):
        self.ip = ip
        if not self.ip_validation():
            raise ValueError(f"Invalid IP address: {self.ip}")

    def ip_validation(self):
        try:
            ipaddress.ip_address(self.ip)
            return True
        except ValueError:
            return False

    def result(self):
        result = ""

        result += f"IP: {self.ip}\n"
        result += f"ISP: {self.isp}\n"
        result += f"TOR: {self.tor}\n"
        result += f"VPN: {self.vpn}\n"
        result += f"Proxy: {self.proxy}\n"

        result += "\n"
        result += "Geolocation Informations:\n"
        result += f"Country: {self.country}\n"
        result += f"City: {self.city}\n"
        result += f"Latitude: {self.latitude}\n"
        result += f"Longitude: {self.longitude}\n"
        result += f"ASN: {self.asn}\n"
        result += f"Timezone: {self.timezone}\n"

        result += "\n"
        result += "Security Informations:\n"
        result += f"Fraud Score: {self.fraud_score}\n"
        result += f"Risk: {self.risk}\n"
        result += f"Reason: {self.reason}\n"

        return result
    
    def lookup(self):
        try :
            response = requests.get(self.api + self.ip , timeout=self.requestTimeout)
            
            data = response.json() 

            # info
            self.isp = data.get("ISP","Unknown")
            self.proxy = data.get("proxy","Unknown")
            self.tor = data.get("tor","Unknown")
            self.vpn = data.get("vpn","Unknown")

            # security check
            self.fraud_score = data.get("fraud_score")
            self.risk  = data.get("risk")
            self.reason = data.get("reason")

            # geo
            geo = data.get("geo", {})
            self.country = geo.get("country","Unknown")
            self.city = geo.get("city","Unknown")
            self.latitude = geo.get("latitude","Unknown")
            self.longitude = geo.get("longitude","Unknown")
            self.asn = geo.get("asn")
            self.timezone = geo.get("timezone","Unknown")

            return self.result()

        except requests.exceptions.RequestException as error:
            raise error

