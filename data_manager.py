from pprint import pprint
import requests

GOOGLE_SHEET_API = "https://api.sheety.co/73cf0def7618587a0018adff7fde48af/flightDeals/prices"

class DataManager:
    def __init__(self):
        self.data = {}
    
    def getData(self):
        response = requests.get(GOOGLE_SHEET_API)
        self.data = response.json()['prices']
        
        return self.data
    
    def updateData(self):
        for city in self.data:
            new_data = {
                'price': {
                    'iataCode': city['iataCode']
                }
            }
            requests.put(url=f"{GOOGLE_SHEET_API}/{city['id']}", json=new_data)

    def get_customer_emails(self):
        customers_endpoint = "https://api.sheety.co/73cf0def7618587a0018adff7fde48af/flightDeals/users"
        response = requests.get(customers_endpoint)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data
    
