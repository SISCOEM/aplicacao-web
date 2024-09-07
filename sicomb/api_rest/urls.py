from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='loginAPI'),
    path('info_user/<str:registration>', views.InfoUser.as_view(), name='info_userAPI'),
    path('profile_image_user/<str:registration>', views.ProfilePhotoPath.as_view(), name='profile_image_userAPI'),
    path("police_loads_report/<str:registration>", views.PoliceLoadsReport.as_view(), name="police_loads_infoAPI"),
    path("police_loads_info/<str:registration>", views.PoliceLoadsInfo.as_view(), name="police_loads_detailAPI"),
    path("equipment_loads_info/<str:load_id>", views.EquipmentLoadsInfo.as_view(), name="equipment_loads_infoAPI"),
    path("push-token/<str:registration>/<str:tokenPush>", views.PushToken.as_view(), name="push_tokenAPI"),
    path("get-csrf-token/", views.get_csrf_token, name="get_csrf_tokenAPI"),
    path("get-adjunct/", views.GetAdjunct.as_view(), name="get_adjunctAPI"),
    path("get-equipment-list/", views.GetEquipmentList.as_view(), name="get_equipment_listAPI"),
    path("confirm-load/", views.ConfirmLoad.as_view(), name="confirm_loadAPI"),
    path("verify-conexion/", views.VerifyConexion.as_view(), name="verify_conexionAPI"),
]
