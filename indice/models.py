from django.db import models

# Create your models here.

class Documento(models.Model):
    id_document = models.AutoField(primary_key=True)
    length = models.IntegerField(default=0)
    path = models.CharField(max_length=200)
    
class Token(models.Model):
    id_token = models.AutoField(primary_key=True)
    term = models.CharField(max_length=200)
    document = models.ForeignKey('Documento', on_delete=models.CASCADE)