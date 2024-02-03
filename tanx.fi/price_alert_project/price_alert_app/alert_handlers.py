import json
import time
import threading
from websockets import connect
from django.core.mail import send_mail
from .models import Alert

def handle_alerts():
    ws = connect('wss://stream.binance.com:9443/ws/btcusdt@trade')
    while True:
        data = ws.recv()
        data = json.loads(data)
        price = float(data['p'])
        for alert in Alert.objects.filter(status='created'):
            if price >= alert.target_price:
                alert.status = 'triggered'
                alert.save()
                send_mail(
                    'Price Alert',
                    f'The price of {alert.coin} has reached your target price of {alert.target_price}',
                    'harshulnanwani@gmail.com',
                    [alert.user.email],
                    fail_silently=False,
                )


import threading
from .models import Alert
from .alert_handlers import handle_alerts

def start_alert_handlers():
    t = threading.Thread(target=handle_alerts)
    t.start()

start_alert_handlers()