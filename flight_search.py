import requests
from flight_data import FlightData
FLIGHT_SEARCH_API = "API_KEY"
FLIGHT_SEARCH_ENDPOINT = "https://api.tequila.kiwi.com"

class FlightSearch:
    
    def getIataCode(self, city):
        location_endpoint = f"{FLIGHT_SEARCH_ENDPOINT}/locations/query"
        headers = {'apikey': FLIGHT_SEARCH_API}
        query = {
            'term': city,
            'location_types': "city"
        }
        
        
        response = requests.get(url=location_endpoint, params=query, headers=headers)
        response.raise_for_status()
        
        
        return response.json()['locations'][0]['code']
        
        
    def getFlightData(self, from_city_code, to_city_code, from_time, to_time):
        search_endpont = f"{FLIGHT_SEARCH_ENDPOINT}/v2/search"
        headers = {'apikey': FLIGHT_SEARCH_API}
        query = {
            'fly_from': from_city_code,
            'fly_to': to_city_code,
            'date_from': from_time.strftime("%d/%m/%Y"),
            'date_to': to_time.strftime("%d/%m/%Y"),
            'nights_in_dst_from': 7,
            'nights_in_dst_to': 28,
            'flight_type': 'round',
            'one_for_city': 1,
            'max_stopovers': 0,
            'curr': "USD"
        }
        
        response = requests.get(url=search_endpont, params=query, headers=headers)
        try:
            data = response.json()['data'][0]
        except IndexError:
            query['max_stopovers'] = 1
            response = requests.get(url=search_endpont, params=query, headers=headers)
            try:
                data = response.json()['data'][0]
            except IndexError:
                print(f"No flights found for {to_city_code}.")
            else:
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][1]["cityTo"],
                    destination_airport=data["route"][1]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][2]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"],
                )
                return flight_data
        else:
            #print(data)
            flight_data = FlightData(
                price=data['price'],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            print(f'{flight_data.destination_city}: ${flight_data.price}')
        
            return flight_data
