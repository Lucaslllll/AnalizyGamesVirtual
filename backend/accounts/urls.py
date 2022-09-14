from django.urls import path
from rest_framework import routers
from .api import UsuarioViewSet, LoginAPI
from rest_framework.authtoken import views

router = routers.DefaultRouter()




router.register('usuario', UsuarioViewSet, 'usuario')

urlpatterns = router.urls

urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token),
    path('session/login', LoginAPI.as_view(), name='login'),
    
]