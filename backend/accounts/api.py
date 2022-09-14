from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password

from .models import Usuario
from .serializers import UsuarioSerializer, LoginSerializer




class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer



class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)

        userOb = Usuario.objects.get(email=serializer.validated_data['email'])

        return Response({
                            "id": userOb.id,
                            "first_name": userOb.first_name,
                            "last_name": userOb.last_name,
                            "email" : userOb.email
                        
                        })

