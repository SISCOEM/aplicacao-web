from django.urls import path
from . import views, apis

# /equipment
urlpatterns = [
    path("", views.filter_equipment, name="filter_equipment"), # mostra a tela de gerencia dos equipamentos
    path("approve/", views.approve_equipment, name="approve_equipment"), # aprova um equipamento
    path("cadastro/", views.register_edit_equipment, name="register_equipment"), # registra o equipamento
    path("editar/<str:id>/", views.register_edit_equipment, name="edit_equipment"), # edita o equipamento
    
    path("modelos/", views.filter_model, name="manage_model"), # mostra a tela de gerencia dos modelos de equipamentos
    path("modelos/approve/", views.approve_model, name="approve_model"), # aprova o modelo
    path("modelo/cadastro/", views.register_edit_model, name="register_model"), # leva ao form para registrar o modelo
    path("modelo/cadastro/<str:model_name>/", views.register_edit_model, name="register_model"), # registra o modelo
    path("modelo/edit/<str:model_name>/<int:id>/", views.register_edit_model, name="edit_model"), # edita o modelo
    path("tag/test/", views.test_tag, name="test_tag"), # tela de teste de tags
    path("tag/api/test/", apis.get_tag, name="test_tag_api"), # api para receber as tags lidas com fim de teste
    
    path("allow_cargo", apis.allow_cargo), # faz a confirmação pela parte do policial de poder realizar a carga (Libera o botão ao adjunto)
    path("get_disponivel", apis.get_equipment_avalible), # retorna em json o equipamento do uid inserido (em formato JSON)
    path("get_indisponivel/<int:id>/", apis.get_equipment_unvalible), # retorna em json o equipamento do uid inserido para descarga (em formato JSON)
    path("get/<str:serial_number>", apis.get_equipment_serNum), # retorna em o equipamento a partir do numero de série ou munição do calibre (nesse caso deve receber a requisição com prefixo de 'bullet::')
    path("valid_uid", apis.valid_uid), # valida o uid inserido para cadastrar (em formato JSON)
    path("valid_serial_number/<str:sn>/", apis.valid_serial_number), # valida o numero serial pra cadastro (em formato JSON)
    path("set", apis.set_uid), # seta o uid (em formato API)
    path("lista_espera/get/", apis.get_uids), # retorna os uids (em formato API)
    path("bullets/get/", apis.get_bullets), # retorna todas as munições (em formato API)
    # path("get_models", get_models_equipment), # retorna todos os models
    path("<str:pk>/info_equipamento/", views.get_equipment_info, name='get_equipment_info'),
]
