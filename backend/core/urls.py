#from django.conf.urls import url
from django.urls import path
from rest_framework import routers
from .api import NoticiasViewSet
from rest_framework.authtoken import views
    

router = routers.DefaultRouter()
# router = routers.SimpleRouter()


router.register('noticias', NoticiasViewSet, 'noticias')


urlpatterns = router.urls


