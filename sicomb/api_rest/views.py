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
            return Response({'error_message': "Matrícula incorreta"}, status=401)
        if check_password(password, police.password):
            if not police.activated or police.activator is None:
                return Response({'error_message': "Matrícula incorreta"}, status=400)
                        
            token, _ = Token.objects.get_or_create(user=police)
            return Response({'token': token.key})
        
        else:
            return Response({'error': 'Credenciais incorretas'}, status=400)
        