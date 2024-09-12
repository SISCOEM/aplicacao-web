from django.shortcuts import render
from .models import Notification
import requests

# Create your views here.
class NotificationService:
    def __init__(self):
        self.expo_push_url = 'https://exp.host/--/api/v2/push/send'
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
    def send_notification(self, title, emoji_title, emoji_body, body, data, expo_push_token):
        notification = Notification(title=title, body=body, data=data, to=expo_push_token)
        data_notification = {
            'to': expo_push_token,
            'title': title + ' ' + emoji_title,
            'body': body + ' ' + emoji_body,
            'data': data
        }
        response = requests.post(self.expo_push_url, headers=self.headers, json=data_notification)
        if expo_push_token is None:
            pass
        else:
            notification.save()
        return response.json()
