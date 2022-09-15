from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.hashers import make_password, check_password

from .models import Usuario
from .serializers import UsuarioSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated



class UsuarioViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, )

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer



class LoginAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    
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

