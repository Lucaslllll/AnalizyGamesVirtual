from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Noticias
from .serializers import NoticiasSerializer





class NoticiasViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )

    queryset = Noticias.objects.all()
    serializer_class = NoticiasSerializer


