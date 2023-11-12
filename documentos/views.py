from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from .models import Documento, Token
from django.shortcuts import render
from django.db.models import Q
from .forms import DocumentoCreateForm, TokenCreateForm
from index.textExtractor import TextExtractor

from index.bm25 import BM25Okapi

class DocumentoCreateView(CreateView):
    model = Documento
    fields = (
        "titulo",
        "autor",
        "instituicao",
        "arquivo_pdf"
    )
    template_name = "documentos/documento_new.html"
    success_url = reverse_lazy("documento_new")

    def post(self, request, *args, **kwargs):
        #super(DocumentoCreateView, self).post(request)
        form = DocumentoCreateForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            documento = form.save()
            #documento.save()
            path = f'/media/' + form.files['arquivo_pdf'].__str__()
            extracao_de_texo = TextExtractor(path)
            texto_completo = extracao_de_texo.get_full_text()
            doc = Documento.objects.get(id=documento.id)
            doc.tamanho = extracao_de_texo.get_quantidade_de_palavras()
            doc.save()
            keywords = extracao_de_texo.extrair_keywords(100)

            tokens_to_create = [Token(termo=kw, documento=documento) for kw in keywords]

# Use bulk_create para criar os objetos de uma só vez
            Token.objects.bulk_create(tokens_to_create)
            #for kw in keywords:
                #novo_token = Token(termo=kw, documento=documento)
                #novo_token.save()
        
            #Token.objects.create(token)
            
            
        return render(request, 'documentos/documento_new.html')
 
class DocumentoListView(ListView):
    model = Documento
    template_name = "documentos/documento_list.html"
    context_object_name = "documento_list"

class DocumentoDetailView(DetailView): # new
    model = Documento
    template_name = "documentos/documento_detail.html"

class DocumentoUpdateView(UpdateView): # new
    model = Documento
    fields = (
        "titulo",
        "autor",
        "instituicao"
    )
    template_name = "documentos/documento_edit.html"

class DocumentoDeleteView(DeleteView): # new
    model = Documento
    template_name = "documentos/documento_delete.html"
    success_url = reverse_lazy("documento_list")

def buscar(request):
    if request.method == 'GET':
        query = request.GET.get('q')  
        tipo_busca = request.GET.get('c')
        if tipo_busca == 'true':
            algoritmo_de_busca = BM25Okapi()
            retorno = algoritmo_de_busca.get_top_n(query)
            resultados = reclassificar(retorno)

        else:
            resultados = Documento.objects.filter(
                Q(titulo__icontains=query) |  
                Q(autor__icontains=query) | 
                Q(instituicao__icontains=query)
            )
        
        return render(request, 'documentos/documento_search.html', {'documento_list': resultados, 'query': query})

def reclassificar(documentos):
    res_titulo_exato = Documento.objects.filter(Q(titulo__icontains=query))
    res_autor_exato = Documento.objects.filter(Q(autor__icontains=query))
    res_palavra_chave_exato = Documento.objects.filter(Q(instituicao__icontains=query))
            
    res_titulo_abrangente = []
    res_autor_abrangente = []
    res_palavra_chave_abrangente = []

    for termo in query.split():
        titulo_abrangente = Documento.objects.filter(Q(titulo__icontains=query))
        res_titulo_abrangente = res_titulo_abrangente + titulo_abrangente
        autor_abrangente = Documento.objects.filter(Q(autor__icontains=query))
        res_autor_abrangente = res_autor_abrangente + autor_abrangente
        palavra_chave_abrangente = Documento.objects.filter(Q(instituicao__icontains=query))
        res_palavra_chave_abrangente = res_palavra_chave_abrangente + palavra_chave_abrangente

    N = len(documentos)
    if (N == 0):
        retorno = []
        for res in res_palavra_chave_exato:
            if res not in retorno:
                retorno.append(res)
        for res in res_titulo_exato:
            if res not in retorno:
                retorno.append(res)
        for res in res_autor_exato:
            if res not in retorno:
                retorno.append(res)
        for res in res_palavra_chave_abrangente:
            if res not in retorno:
                retorno.append(res)
        for res in res_titulo_abrangente:
            if res not in retorno:
                retorno.append(res)
        for res in res_autor_abrangente:
            if res not in retorno:
                retorno.append(res)
        return retorno

    peso_palavra_chave_exato = (0.1 / N)
    peso_titulo_exato = 1 + (0.05 / N)
    peso_autor_exato = 1 + (0.03 / N)

    peso_palavra_chave_abrangente = (0.15 / N)
    peso_titulo_abrangente = (0.1 / N)
    peso_autor_abrangente = (0.05 / N)

    for doc in documentos:
        peso = 0
        if doc[0] in res_autor_abrangente:
            peso += peso_autor_abrangente
        if doc[0] in res_titulo_abrangente:
            peso += peso_titulo_abrangente
        if doc[0] in res_palavra_chave_abrangente:
            peso += peso_palavra_chave_abrangente
        if doc[0] in res_autor_exato:
            peso += peso_autor_exato
        if doc[0] in res_titulo_exato:
            peso += peso_titulo_exato
        if doc[0] in res_palavra_chave_exato:
            peso += peso_palavra_chave_exato

        doc[1] = doc[1] * (1 + peso)

    documentos_reclassificados = sorted(vetores, key=lambda vetor: documentos[1])

    novo_ranking = []

    for d in documentos_reclassificados:
        novo_ranking.append(d[0])
    
    return novo_ranking