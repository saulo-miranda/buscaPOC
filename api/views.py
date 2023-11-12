import os
from django_project import settings
from documentos.models import Documento, Token
from index.textExtractor import TextExtractor
from rest_framework import viewsets , permissions, status, serializers
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from .serializers import DocumentoSerializer, TokenSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
import yake

@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_items': '/all',
        'Buscar por autor': '/?autor=nome_do_autor',
        'Buscar por titulo': '/?titulo=titulo_do_trabalho',
        'Buscar por instituicao': '/?instituicao=instituicao_do_autor',
        'Buscar por titulo ou autor ou instituição': '/?q=query',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/documento/pk/delete'
    }
 
    return Response(api_urls)

@api_view(['POST'])
def add_documentos(request):
    documento = DocumentoSerializer(data=request.data)
 
    # validating for already existing data
    if Documento.objects.filter(**request.data).exists(): 
        raise serializers.ValidationError('This data already exists')
    if documento.is_valid():
        #autor = documento['autor']
        #titulo = documento['titulo']
        #instituicao = documento['instituicao']
        #arquivo_pdf = documento['arquivo_pdf']
        #criar_documento_e_tokens(documento)
        documento_salvo = documento.save()
        termos = ["termo1", "termo2", "termo3"]  # Substitua isso pela lógica real
        for t in termos:
            novo_token = Token(termo=t, documento=documento_salvo)
            novo_token.save()
  

            # Use bulk_create para inserir todos os Tokens de uma vez no banco de dados
        #Token.objects.bulk_create(tokens)
        #print(documento.data)
        #print(settings.MEDIA_ROOT)
        path = documento.data['arquivo_pdf']
        print(path)
        extracao_de_texo = TextExtractor(path)
        texto_completo = extracao_de_texo.get_full_text()
        print(documento.data['arquivo_pdf'])
        language = "pt"
        max_ngram_size = 3
        deduplication_threshold = 0.9
        deduplication_algo = 'seqm'
        windowSize = 1
        numOfKeywords = 100

        custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
        keywords = custom_kw_extractor.extract_keywords(texto_completo)

        for kw in keywords:
            novo_token = Token(termo=kw[0], documento=documento_salvo)
            novo_token.save()
        #novo_documento = Documento.objects.
        #tokens = extracao_de_texo.extrair_tokens(documento_salvo)
        #Token.objects.bulk_create(tokens, 100)
        return Response(documento.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def view_documentos(request):
    if request.query_params:
        query = request.GET.get('q')  
        
        if(query != None):
            documentos = Documento.objects.filter(
                Q(titulo__icontains=query) |  
                Q(autor__icontains=query) | 
                Q(instituicao__icontains=query)
            )
        else:
            query = request.query_params 
            documentos = Documento.objects.filter(**request.query_params.dict())
    else:
        documentos = Documento.objects.all()
 
    # if there is something in items else raise error
    if documentos:
        serializer = DocumentoSerializer(documentos, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PUT'])
def update_documentos(request, pk):
    item = Documento.objects.get(pk=pk)
    data = DocumentoSerializer(instance=item, data=request.data)
 
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE'])
def delete_documents(request, pk):
    item = get_object_or_404(Documento, pk=pk)
    item.delete()
    return Response(status=status.HTTP_202_ACCEPTED)