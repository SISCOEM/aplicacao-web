from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password
from police.models import Police
from rest_framework import status
from load.models import Load, Equipment_load
from django.shortcuts import get_object_or_404, get_list_or_404
from load.serializers import LoadSerializer, Equipment_loadSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.conf import settings
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
                return Response({'error_message': "Matrícula incorreta"})
        if check_password(password, police.password):
            print('Policial ', police)
            print('User', request.user)
            if not police.activated or police.activator is None:
                return Response({'error_message': "Policial aguardando aprovação de um administrador"})
            if request.data.get('type_login') != 'request':            
                token, _ = Token.objects.get_or_create(user=police)
                return Response({
                    'token': token.key,
                    'ok': True,
                    'registration': police.matricula
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'ok': True,
                    })
        else:
            return Response({'error_message': 'Credenciais incorretas'})
class InfoUser(APIView):
    def get(self, request, registration):
        try:
            police = Police.objects.filter(matricula=registration).first()
            if police is None:
                police = Police.objects.filter(id=registration).first()
            image_url = police.image_path.url if police.image_path else None
            return Response({
                'img_path': image_url,
                'name': police.name,
                'number_phone': police.telefone,
                'cipm': police.lotacao,
                'email': police.email
            })
        except Exception as error:
            print(error)
            return Response({
                "error_message": error
            })

class ProfilePhotoPath(APIView):
    def get(self, request, registration):
        try: 
            police = Police.objects.filter(matricula=registration).first()
            return Response({
                'img_path': police.image_path.url if police.image_path else None
            })
            
        except Exception as error:
            print(error)
            return Response({
                'error_message': 'Deu erro aqui meu patrao'
            })
            

class PoliceLoadsReport(APIView):
    
    permission_classes = [IsAuthenticated] # É obrigatório estar logado
    
    def get(self, request, registration):
        try:
            police = get_object_or_404(Police, matricula=registration)
            loads = Load.objects.filter(police=police)
            carriedOutLoads = 0
            finishedLoads = 0
            notFinishedLoads = 0
            if len(loads) > 0:
                carriedOutLoads = 0
                finishedLoads = 0
                for load in loads:
                    if load.turn_type != 'descarga':
                        carriedOutLoads += 1
                        if load.returned_load_date is not None:
                            finishedLoads += 1
                notFinishedLoads = carriedOutLoads - finishedLoads
            return Response({
                    'carriedOutLoads': carriedOutLoads,
                    'finishedLoads': finishedLoads,
                    'notFinishedLoads': notFinishedLoads
                })                 
        except Exception as error:
            print(error)
            return Response({
                'erro': error
            })
            
class PoliceLoadsInfo(APIView):
    
    permission_classes = [IsAuthenticated] # É obrigatório estar logado
    
    def get(self, request, registration):
        try:
            police = get_object_or_404(Police, matricula=registration)
            loads = Load.objects.filter(police=police)
            loads_formatted = []
            for load in loads:
                if load.turn_type != 'descarga':
                    loads_formatted.append(load)
            serializer = LoadSerializer(loads_formatted, many=True)
            print(serializer.data)
            return Response(serializer.data)
        except Exception as error:
            print(error)
            return Response({
                'erro': str(error)
            })

class EquipmentLoadsInfo(APIView):
    
    permission_classes = [IsAuthenticated] # É obrigatório estar logado
    
    def get(self, request, load_id):
        try:
            equipment_load = get_list_or_404(Equipment_load, load_id=load_id)
            serializer = Equipment_loadSerializer(equipment_load, many=True)
            return Response(serializer.data)
        except Exception as error:
            print(error)
            return Response({
                'erro': str(error)
            })
            
class PushToken(APIView):
    def post(self, request, registration, tokenPush):
        try:
            police = Police.objects.get(matricula=registration)
            police.pushToken = tokenPush
            police.save()
            return Response({
                'ok': True
            })
        except Exception as error:
            print(error)
            return Response({
                'erro': str(error)
            })

@api_view(['GET'])
@ensure_csrf_cookie
def get_csrf_token(request):
    return Response({'csrfToken': get_token(request)})

class GetAdjunct(APIView):
    def get(self, request):
        permission_classes = [IsAuthenticated] # É obrigatório estar logado

        print(settings.AUX)
        data = {
            'matricula': settings.AUX['registration_adjunct'],
            'ok': True
        }
        print(data)
        return Response(data)