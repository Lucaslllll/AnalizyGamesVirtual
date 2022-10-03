from django.db import models

# Create your models here.




class Noticias(models.Model):
	title = models.CharField(max_length=1000)
	thumb = models.ImageField()
	preview = models.CharField(max_length=150, null=True)
	details = models.TextField()
	date = models.DateTimeField(null=True, blank=True)


class ImagensNoticias(models.Model):
	images = models.ImageField()
	noticias_key = models.ForeignKey(Noticias, on_delete=models.CASCADE)
