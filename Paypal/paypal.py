import paypalrestsdk

paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": "",
    "client_secret": ""})

invoice = paypalrestsdk.Invoice({
    'merchant_info': {
        "email": "",
    },
    "billing_info": [{
        "email": ""
    }],
    "items": [{
        "name": "Commission",
        "quantity": 1,
        "unit_price": {
            "currency": "USD",
            "value": 2
        }
    }],
})

response = invoice.create()
print(response)
print(invoice)
response = invoice.send()
print(response)
