from django.db import models

# Create your models here.
class Usuario(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=255)
	active = models.BooleanField(default=False)
	date_expiration = models.DateTimeField(null=True, blank=True)

# class Jogos(models.Model):
# 	