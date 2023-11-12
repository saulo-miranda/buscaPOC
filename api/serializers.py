from documentos.models import Documento, Token
from rest_framework import serializers

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:

        model = Documento
        fields = ['titulo', 'autor', 'instituicao', 'arquivo_pdf']

class TokenSerializer(serializers.ModelSerializer):
    class Meta:

        model = Token
        fields = ['termo', 'quantidade', 'documento']
