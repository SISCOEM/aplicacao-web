from django.urls import path
from . import views, apis

urlpatterns = [
    path(
        "fazer_carga/", views.confirm_load, name="fazer_carga"
    ),  # Redireciona pra página de carga
    path(
        "fazer_carga/cancelar", views.cancel_load
    ),  # Cancelar a carga zerando a lista na views
    path(
        "get/<int:id>/", apis.get_load
    ),  # Retorna uma resposta JSON com todas as cargas (caso necessário)
    path(
        "get/cargas_policial/<str:plate>/", apis.get_loads_police
    ),  # Retorna uma resposta JSON com todas as cargas do policial com filtro por matricula (caso necessário)
    path(
        "lista_equipamentos/add/",
        apis.add_list_equipment,
    ),  # adiciona um equipamento à lista na views vindo do front
    path(
        "lista_equipamentos/add/observation/",
        apis.add_obs,
    ),  # adiciona uma observação a um equipamento em uma descarga
    path(
        "lista_equipamentos/remover/",
        apis.remove_list_equipment,
    ),  # Remove um equipamento da lista na views vindo do front a solicitação
    path("lista_equipamentos/get", apis.get_list_equipment_avalible),
    # Retorna a lista da views
    path("lista_equipamentos_atual/get", apis.get_list_equipment),
    path("info/get", apis.get_info),
    path("", views.filter_loads, name='filter_cargas'),
    #Retorna a o policial resposável pela carga e a lista de equipamentos da carga
    path("<str:pk>/carga_policial/", views.get_carga_policial, name='carga_polical'),
    path("read_qrcode/", views.read_qrcode),
    path("relatorio/enviar/<int:id>", apis.send_load_relatory),
    path("relatorio/receber/<int:id>", apis.get_relatory),
    path("check_load/<int:id>", apis.check_load),
    path("api/reset_rfid/", apis.reset_rfid),
]
