#from django.conf.urls import url
from django.urls import path
from rest_framework import routers
from .api import UsuarioViewSet

router = routers.DefaultRouter()

router.register('Usuario', UsuarioViewSet, 'article')


urlpatterns = router.urls

# urlpatterns += [
#   
#]
