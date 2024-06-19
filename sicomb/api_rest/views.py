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
            try:
                police = Police.objects.get(username=registration)

            except Police.DoesNotExist:
                pass
                return Response({'error_message': "Matrícula incorreta"})
        
        if check_password(password, police.password):
            if not police.activated or police.activator is None:
                return Response({'error_message': "Policial aguardando aprovação de um administrador"})
                        
            token, _ = Token.objects.get_or_create(user=police)
            return Response({
                'token': token.key,
                'ok': True,
                }, status=status.HTTP_200_OK)
        
        else:
            return Response({'error_message': 'Credenciais incorretas'})
