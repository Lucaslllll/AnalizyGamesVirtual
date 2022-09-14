from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password

from .models import Noticias
from .serializers import NoticiasSerializer





class NoticiasViewSet(viewsets.ModelViewSet):
    queryset = Noticias.objects.all()
    serializer_class = NoticiasSerializer


