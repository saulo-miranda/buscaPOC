from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from .teste import Teste
from index.stemmer.savoy import Savoy
from index.stemmer.rslp import RSLP 
from index.bm25 import BM25Okapi, BM25L, BM25Plus

# Create your views here.
class TesteView(TemplateView):
    template_name = "teste/index.html"

def popular_banco(request):
    if request.method == 'GET':
        teste = Teste()
        #documentos = teste.listar_arquivos()
        #print(documentos)
        total = len(documentos)
        processados = 0
        lote = 16500
        atual = 6585#conferir se houve adição parcial de documento 
        #documentos = documentos[atual:lote]
        documentos = []
        #191.185.79.82/32
        for documento in documentos:
            inserir_documento(documento, atual, lote, teste) # Executa em paralelo
            atual += 1
        
        return redirect('home')

def inserir_documento(documento, atual, lote, teste):
    try:
        teste.salvar_documento_banco(documento, 200)
        print(atual, "de", lote)
    except Exception as e:
        print("Erro -", atual, "de", lote, e)

def teste_regis(request):
    N = 100
    cache_query = {}
    if request.method == 'GET':
        savoy = request.GET.get('savoy')
        rslp = request.GET.get('rslp')
        bm25okapi = request.GET.get('bm25okapi')  
        bm25l = request.GET.get('bm25l') 
        bm25plus = request.GET.get('bm25plus')    
        teste = Teste()
        queries_teste = teste.ler_queries_teste()
        #queries_teste = queries_teste[13:14]
        if bm25l == 'true':
            algoritmo_de_busca = BM25L()
            if rslp == 'true':
                stemmer = RSLP()
                print(cache_query)
                i = 1
                for t in queries_teste:
                    #algoritmo_de_busca = BM25Okapi()
                   # print(t[1])
                    query = stemmer.text_stemming(t[1])
                    resultados, cache_query = algoritmo_de_busca.get_top_n(query, stemmer, cache_query, N)
                    print(resultados)
                    resultados = teste.conferir_gabarito(t[0], resultados)
                    print(resultados)
                    salvar_arquivo(i, resultados, t, 'bm25l_rslp')
                    i+=1
                  #  print(len(resultados))
            if savoy == 'true':
                stemmer = Savoy()
                print(cache_query)
                i = 1
                for t in queries_teste:
                    #algoritmo_de_busca = BM25Okapi()
                #    print(t[1])
                    query = stemmer.text_stemming(t[1])
                    query = query.lower()
                    resultados, cache_query = algoritmo_de_busca.get_top_n(query, stemmer, cache_query, N)
                    print(resultados)
                    resultados = teste.conferir_gabarito(t[0], resultados)
                    print(resultados)
                    salvar_arquivo(i, resultados, t, 'bm25l_savoy')
                    i+=1
                 #   print(len(resultados))
        if bm25plus == 'true':
            algoritmo_de_busca = BM25Plus()
            if rslp == 'true':
                stemmer = RSLP()
                #print(len(queries_teste))
                i = 1
                print(cache_query)
                #queries_teste = queries_teste[:3]
                for t in queries_teste:
                    #algoritmo_de_busca = BM25Okapi()
                    #print(t[1])
                    query = stemmer.text_stemming(t[1])
                    resultados, cache_query = algoritmo_de_busca.get_top_n(query, stemmer, cache_query, N)
                    print(resultados)
                    resultados = teste.conferir_gabarito(t[0], resultados)
                    print(resultados)
                    salvar_arquivo(i, resultados, t, 'bm25plus_rslp')
                    i+=1
                 #   print(len(resultados))
            if savoy == 'true':
                stemmer = Savoy()
               # print(len(queries_teste))
                print(cache_query)
                i = 1
                for t in queries_teste:
                    #algoritmo_de_busca = BM25Okapi()
                #    print(t[1])
                    query = stemmer.text_stemming(t[1])
                    query = query.lower()
                    resultados, cache_query = algoritmo_de_busca.get_top_n(query, stemmer, cache_query, N)
                    print(resultados)
                    resultados = teste.conferir_gabarito(t[0], resultados)
                    print(resultados)
                    salvar_arquivo(i, resultados, t, 'bm25plus_savoy')
                    i+=1
                #    print(len(resultados))

        if bm25okapi == 'true':
            algoritmo_de_busca = BM25Okapi()
            if rslp == 'true':
                stemmer = RSLP()
                #print(len(queries_teste))
                i = 1
                #queries_teste = queries_teste[:3]
                print(cache_query)
                for t in queries_teste:
                    #algoritmo_de_busca = BM25Okapi()
                    #print(t[1])
                    
                    query = stemmer.text_stemming(t[1])
                    #print(query)
                    resultados, cache_query = algoritmo_de_busca.get_top_n(query, stemmer, cache_query, N)
                    print(resultados)
                    resultados = teste.conferir_gabarito(t[0], resultados)
                    print(resultados)
                    salvar_arquivo(i, resultados, t, 'bm25_rslp')
                    i+=1
                    #print(len(resultados))
            if savoy == 'true':
                stemmer = Savoy()
                #print(len(queries_teste))
                print(cache_query)
                i = 1
                for t in queries_teste:
                    #algoritmo_de_busca = BM25Okapi()
                    #print("foi")
                    query = stemmer.text_stemming(t[1])
                    query = query.lower()
                #    print(query)
                    resultados, cache_query = algoritmo_de_busca.get_top_n(query, stemmer, cache_query, N)
                    print(resultados)
                    resultados = teste.conferir_gabarito(t[0], resultados)
                    print(resultados)
                    salvar_arquivo(i, resultados, t, 'bm25_savoy')
                    i+=1
                #    print(len(resultados))
        

        #resultados = algoritmo_de_busca.get_top_n(queries_teste[0][1])
        #print(resultados)
        return render(request, 'documentos/documento_new.html')

def salvar_arquivo(num_query, resultados, query, nome_arquivo):
    set_resultados = set(resultados)
    resultados = list(set_resultados)
    with open(f'{nome_arquivo}.txt', 'a') as arquivo:
        arquivo.write(f'{num_query}: {query}\n')
        for res in resultados:
            arquivo.write(f'{res}\n')
    