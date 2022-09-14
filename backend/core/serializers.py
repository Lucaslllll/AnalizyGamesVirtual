from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import Noticias, ImagensNoticias







class NoticiasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticias
        fields = '__all__'


class ImagensNoticiasSerializer(serializers.Serializer):
    class Meta:
        model = Noticias
        fields = '__all__'