#from django.conf.urls import url
from django.urls import path
from rest_framework import routers
from .api import UsuarioViewSet, LoginAPI

router = routers.DefaultRouter()
# router = routers.SimpleRouter()

router.register('usuario', UsuarioViewSet, 'usuario')


urlpatterns = router.urls

urlpatterns += [
    path('session/login', LoginAPI.as_view(), name='login'),
    
]
