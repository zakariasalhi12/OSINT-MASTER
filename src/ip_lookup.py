import requests

class IPlookup :
    # private fields
    
    # request information
    requestTimeout = 5
    api = "https://api.ffraud.com/public/ip/"

    # global ip info
    isp = "unknown"
    proxy = "unknown"
    vpn = "unknown"
    tor = "unknown"

    # geo
    country = "unknown"
    city = "unknown"
    latitude = "unknown"
    longitude = "unknown"
    asn = "unknown"
    timezone = "unknown"

    # security check
    fraud_score = "unknown"
    risk  = "unknown"
    reason = "unknown"

    def __init__(self, ip):
        self.ip = ip

    def ip_validation(self):
        print("hello")

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
            self.isp = data["ISP"]
            self.proxy = data["proxy"]
            self.tor = data["tor"]
            self.vpn = data["vpn"]

            # geo
            self.country = data["geo"]["country"]
            self.city = data["geo"]["city"]
            self.latitude = data["geo"]["latitude"]
            self.longitude = data["geo"]["longitude"]
            self.asn = data["geo"]["asn"]
            self.timezone = data["geo"]["timezone"]

            # security check
            self.fraud_score = data["fraud_score"]
            self.risk  = data["risk"]
            self.reason = data["reason"]

            print(self.result())

        except requests.exceptions.RequestException as error:
            raise error

