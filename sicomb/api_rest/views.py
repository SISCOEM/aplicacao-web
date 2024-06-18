from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from police.models import Police
from rest_framework import status

class LoginAPIView(APIView):
    def post(self, request):
        registration = request.data.get('registration')
        password = request.data.get('password')
        try:
            police = Police.objects.get(matricula=registration)
        except Police.DoesNotExist:
            return Response({'error_message': "Matrícula incorreta"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if check_password(password, police.password):
            if not police.activated or police.activator is None:
                return Response({'error_message': "Policial aguardando aprovação de um administrador"}, status=status.HTTP_400_BAD_REQUEST)
                        
            token, _ = Token.objects.get_or_create(user=police)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        
        else:
            return Response({'error': 'Credenciais incorretas'}, status=status.HTTP_400_BAD_REQUEST)
