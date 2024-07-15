import paypalrestsdk
from django.conf import settings

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

def create_paypal_payment(cart):
    total_amount = sum([item.product.price * item.quantity for item in cart.items.all()])
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://localhost:8000/payment/execute/",
            "cancel_url": "http://localhost:8000/payment/cancel/"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": item.product.name,
                    "sku": item.product.id,
                    "price": str(item.product.price),
                    "currency": "USD",
                    "quantity": item.quantity
                } for item in cart.items.all()]
            },
            "amount": {
                "total": str(total_amount),
                "currency": "USD"
            },
            "description": "Payment for cart."
        }]
    })
    
    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return link.href
    else:
        return None