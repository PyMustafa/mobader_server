from django.test import TestCase
from .models import BookDoctor


book_query = BookDoctor.objects
print(f'book_query: {book_query}')
print(f'book_query.all: {book_query.all()}')



"""
retrieve_charge_response.text: {
  "id": "chg_TS03A3720232200Mg4k2011678",
  "object": "charge",
  "live_mode": false,
  "customer_initiated": true,
  "api_version": "V2",
  "method": "GET",
  "status": "CAPTURED",
  "amount": 50.00,
  "currency": "SAR",
  "threeDSecure": false,
  "card_threeDSecure": false,
  "save_card": false,
  "product": "GOSELL",
  "description": "Test Description",
  "metadata": {
    "udf1": "Metadata 1"
  },
  "order": {
    "id": "ord_Hc0F44231900sAy20lo10i48"
  },
  "transaction": {
    "authorization_id": "258244",
    "timezone": "UTC+03:00",
    "created": "1700517697184",
    "expiry": {
      "period": 30,
      "type": "MINUTE"
    },
    "asynchronous": false,
    "amount": 13.47,
    "currency": "USD"
  },
  "reference": {
    "track": "tck_TS05A3820232200Pt742011787",
    "payment": "3820232200117877614",
    "gateway": "123456789012345",
    "acquirer": "332419258244",
    "transaction": "txn_01",
    "order": "ord_01"
  },
  "response": {
    "code": "000",
    "message": "Captured"
  },
  "card_security": {
    "code": "M",
    "message": "MATCH"
  },
  "acquirer": {
    "response": {
      "code": "00",
      "message": "Approved"
    }
  },
  "gateway": {
    "response": {
      "code": "0",
      "message": "Transaction Approved"
    }
  },
  "card": {
    "object": "card",
    "first_six": "401200",
    "first_eight": "40120000",
    "scheme": "VISA",
    "brand": "VISA",
    "last_four": "0026"
  },
  "receipt": {
    "id": "203920232200117289",
    "email": true,
    "sms": true
  },
  "customer": {
    "id": "cus_TS05A3720232201Dy8g2011700",
    "first_name": "samy",
    "last_name": "hassan",
    "email": "samyhassan@gmail.com",
    "phone": {
      "country_code": "966",
      "number": "1114004545"
    }
  },
  "merchant": {
    "country": "SA",
    "currency": "SAR",
    "id": "27422286"
  },
  "source": {
    "object": "token",
    "type": "CARD_NOT_PRESENT",
    "payment_type": "CREDIT",
    "payment_method": "VISA",
    "channel": "INTERNET",
    "id": "tok_tXiE3423191pQka20VQ102785",
    "on_file": false
  },
  "redirect": {
    "status": "SUCCESS",
    "url": "https://2752-102-185-153-196.ngrok-free.app"
  },
  "post": {
    "status": "SUCCESS",
    "url": "https://2752-102-185-153-196.ngrok-free.app/api/v1/tap_webhook/"
  },
  "activities": [
    {
      "id": "activity_TS03A3720232201Yh4i2011731",
      "object": "activity",
      "created": 1700517697184,
      "status": "INITIATED",
      "currency": "SAR",
      "amount": 50.00,
      "remarks": "charge - created"
    },
    {
      "id": "activity_TS03A4020232201p1PK2011069",
      "object": "activity",
      "created": 1700517700069,
      "status": "CAPTURED",
      "currency": "USD",
      "amount": 13.47,
      "remarks": "charge - captured"
    }
  ],
  "auto_reversed": false
}
"""