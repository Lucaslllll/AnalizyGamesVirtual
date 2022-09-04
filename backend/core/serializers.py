from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuario



class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

    def validate_password(self, data):
        value = make_password(password=data, salt=None, hasher='pbkdf2_sha256')
        return value

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


    def validate(self, data):
        

        try:
            userOb = Usuario.objects.get(email=data['email'])
        except Usuario.DoesNotExist:
            userOb = None

        if userOb == None:
            raise serializers.ValidationError("Dados errados, 01")

        corresponde = check_password(password=data['password'], encoded=userOb.password)


        if corresponde == False:
        # if data['password'] != userOb.password:
            raise serializers.ValidationError("Dados errados, 02")


#         encoded_jwt = jwt.encode({"payload": "tuamae"}, data['password'], algorithm="HS256")
#         print(encoded_jwt)

        return data



