from datetime import *
from data_manager import *
from flight_search import *
from flight_data import *
from notification_manager import *

GOOGLE_SHEET_API = "https://api.sheety.co/73cf0def7618587a0018adff7fde48af/flightDeals/prices"
FLIGHT_SEARCH_API = "API_KEY"
ACCOUNT_SID = "SID"
AUTH_TOKEN = "TOKEN"
PHONE = "TWILIO_PHONE"

data_manager = DataManager()
sheet_data = data_manager.getData()
ORIGIN_CITY_IATA = "IAH"

search = FlightSearch()

for city in sheet_data:
  if len(city['iataCode']) == 0:
      city['iataCode'] = search.getIataCode(city['city'])
      
data_manager.data = sheet_data
data_manager.updateData()


tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
  flight = search.getFlightData(
    ORIGIN_CITY_IATA,
    destination["iataCode"],
    from_time=tomorrow,
    to_time=six_month_from_today
  )
  notification_manager = NotificationManager(flight)
  
  try:
    if destination['lowestPrice'] > flight.price:
      notification_manager.sendSMS()
      
      users = data_manager.get_customer_emails()
      emails = [row['email'] for row in users]
      names = [row['firstName'] for row in users]

      message = f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} " \
                f"to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
      
      if flight.stop_overs > 0:
        message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

      link = f"https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"
      notification_manager.sendEmail(emails, message, link)
      
  except AttributeError:
    continue
  

