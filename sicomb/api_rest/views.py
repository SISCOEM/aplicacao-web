from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password 
from police.models import Police
# Create your views here.
def LoginAPIView(request):
    if request.method == 'POST':
        registration = request.data.get('registration')
        password = request.data.get('password')
        try:
            police = Police.objects.get(matricula=registration)
        except Police.DoesNotExist:
            return Response({'error_message': "Matrícula incorreta"})
        if check_password(password, police.password):
            
        print(user)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Credenciais incorretas'}, status=400)
        