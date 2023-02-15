import smtplib

from flight_data import FlightData
from twilio.rest import Client

ACCOUNT_SID = "SID"
AUTH_TOKEN = "TOKEN"
PHONE = "TWILIO PHONE"
MYPHONE = "YOUR_PHONE"
MY_EMAIL = "GMAIL"
MY_PASSWORD = "USE GOOGLE APP PASSWORD"

class NotificationManager:
    def __init__(self, flight_data: FlightData):
        self.flight_data = flight_data
        self.if_via_stop_over = '\n'
        
        if flight_data.stop_overs > 0:
          self.if_via_stop_over = f"Flight has {self.flight_data.stop_overs} stop over, via {flight_data.via_city}."
        
    def sendSMS(self):
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        
        message = client.messages.create(
            body=f"Low Price Alert! Only ${self.flight_data.price}"
                 f"to fly from {self.flight_data.origin_city}-{self.flight_data.origin_airport} "
                 f"to {self.flight_data.destination_city}-{self.flight_data.destination_airport}, "
                 f"from {self.flight_data.out_date} to {self.flight_data.return_date}."
                 f"{self.if_via_stop_over}",
            from_=PHONE,
            to=MYPHONE,
        )
        
        print(message.status)
        
    def sendEmail(self, emails, message, google_flight_link):
      with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        for email in emails:
          connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=email,
            msg=f"Subject:New Low Price Flight!\n\n{message}\n{google_flight_link}".encode('utf-8')
          )
      
