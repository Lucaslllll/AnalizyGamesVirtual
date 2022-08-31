#from django.conf.urls import url
from django.urls import path
from rest_framework import routers
from .api import UsuarioViewSet

router = routers.DefaultRouter()

router.register('usuario', UsuarioViewSet, 'usuario')


urlpatterns = router.urls

# urlpatterns += [
#   
#]
