from django.shortcuts import render
import requests

# Create your views here.
class NotificationService:
    def __init__(self):
        self.expo_push_url = 'https://exp.host/--/api/v2/push/send'
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
    def send_notification(self, title, message, data, expo_push_token):
        data = {
            'to': expo_push_token,
            'title': title,
            'body': message,
            'data': data
        }
        response = requests.post(self.expo_push_url, headers=self.headers, json=data)
        return response.json()
    
def send_notification(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        data = request.POST.get('data')
        expo_push_token = request.POST.get('expo_push_token')
        
        notification_service = NotificationService()
        response = notification_service.send_notification(title, message, data, expo_push_token)
        return render(request, 'notifications_app_mobile/send_notification.html', {'response': response})
    
    return render(request, 'notifications_app_mobile/send_notification.html', {})