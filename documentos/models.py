from django.db import models
from django.forms import ValidationError

def validate_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError("O arquivo deve ser no formato PDF.")


class Documento(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    instituicao = models.CharField(max_length=200)
    arquivo_pdf = models.FileField(validators=[validate_pdf])
    tamanho = models.BigIntegerField(default=1) 
    def __str__(self):
        return  self.titulo
    
class Token(models.Model):
    id_token = models.AutoField(primary_key=True) 
    termo = models.CharField(max_length=200)
    documento = models.ForeignKey('Documento', on_delete=models.CASCADE)
    quantidade = models.BigIntegerField(default=1) 

    def __str__(self):
        return  self.termo + " - " + self.documento.__str__() 

    def instanciar(self, termo, documento):
        self.termo = termo
        self.documento = documento

    def incrementar(self):
        self.quantidade += 1
