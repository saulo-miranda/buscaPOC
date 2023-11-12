from django import forms 
from .models import Documento, Token

class  DocumentoCreateForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = [
            "titulo",
            "autor",
            "instituicao",
            "arquivo_pdf"
        ]

class  TokenCreateForm(forms.ModelForm):
    class Meta:
        model = Token
        fields = [
            "termo", 
            "quantidade", 
            "documento"
        ]