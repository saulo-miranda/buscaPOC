import xml.etree.ElementTree as ET
from index.ingest import Ingest
import pickle
import glob, os
from tqdm import tqdm
import time
from django_project import settings
from index.textExtractor import TextExtractor
import yake
from documentos.models import Documento, Token
from unidecode import unidecode
import string

class Teste():
    def __init__(self) -> None:
        self.DOCUMENTS_PATH = settings.BASE_DIR.__str__() + "/teste/test_collection/regis-collection-master/documents/"
        self.QUERIES_PATH = settings.BASE_DIR.__str__() + "/teste/test_collection/regis-collection-master/queries.xml" 
        self.GABARITO_QUERIES_PATH = settings.BASE_DIR.__str__() + "/teste/test_collection/regis-collection-master/qrels.txt" 
        self.gabarito = {}
        self.ler_gabarito()

    def listar_arquivos(self):
        padrao_arquivos = os.path.join(self.DOCUMENTS_PATH, '*.xml')
       # print(self.DOCUMENTS_PATH)
        arquivos = glob.glob(padrao_arquivos)
        return arquivos

    def ler_queries_teste(self):
        try:
            tree = ET.parse(self.QUERIES_PATH)  
            root = tree.getroot()  
            retorno = []
            for top in root.findall('top'):
                num = top.find('num').text
                title = top.find('title').text
                retorno.append([num, title])
            return retorno
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
        except IOError as e:
            print(f"Error reading XML file: {e}")

    def read_xml_file(self, file_path):
        try:
            tree = ET.parse(file_path)  
            root = tree.getroot()  
            for element in root.iter():
                print(f"Tag: {element.tag}, Text: {element.text}")
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
        except IOError as e:
            print(f"Error reading XML file: {e}")

    def extract_docid_from_xml(self, file_path):
        try:
            tree = ET.parse(file_path)  
            root = tree.getroot()  
            for field in root.iter('field'):
                if field.get('name') == 'docid':
                    docid = field.text
                    return docid
            return None
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
        except IOError as e:
            print(f"Error reading XML file: {e}")

    def extract_text_from_xml(self, file_path):
        try:
            tree = ET.parse(file_path)  
            root = tree.getroot()  
            for field in root.iter('field'):
                if field.get('name') == 'docid':
                    docid = field.text
                if field.get('name') == 'text':
                    text = field.text
                    return docid, text
            return None
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
        except IOError as e:
            print(f"Error reading XML file: {e}")


    def salvar_objeto(self, objeto, nome_arquivo):
        with open(nome_arquivo, 'wb') as arquivo:
            pickle.dump(objeto, arquivo)

    def carregar_objeto(self, nome_arquivo):
        with open(nome_arquivo, 'rb') as arquivo:
            objeto = pickle.load(arquivo)
        return objeto


    def extrair_keywords(self, texto, n):
        language = "pt"
        max_ngram_size = 3
        deduplication_threshold = 0.9
        deduplication_algo = 'seqm'
        windowSize = 1
        tabela = str.maketrans('', '', string.punctuation)
        texto = unidecode(texto).lower()
        custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=n, features=None)
        keywords = custom_kw_extractor.extract_keywords(texto)
        texto = texto.translate(tabela)
        vetor_texto = texto.split()
        palavras_unicas = []
        for k in keywords:
            termo = k[0]
            for w in termo.split():
                if len(w) > 2:
                    palavras_unicas.append(w)
        conjunto = set(palavras_unicas)
        palavras_unicas = list(conjunto)
        quantidades_palavras = {}
        for t in palavras_unicas:
            contagem = vetor_texto.count(t)
            quantidades_palavras[t] = contagem
        #for k, v in quantidades_palavras.items():
        #    print(k, " - ", v)
        #print(vetor_texto)
        return quantidades_palavras

    def salvar_documento_banco(self, file_path, n_palavras_chave):
        id_doc, texto = self.extract_text_from_xml(file_path)
        tamanho = len(texto.split(' '))
        novo_documento = Documento(titulo =id_doc,autor = "Autor Teste", instituicao = "Instituição Teste", arquivo_pdf = None, tamanho = tamanho )
        novo_documento.save()
        keywords = self.extrair_keywords(texto, n_palavras_chave)
        tokens_to_create = [Token(termo=kw, documento=novo_documento, quantidade=quantidade) for kw, quantidade in keywords.items()]
        Token.objects.bulk_create(tokens_to_create)
        
        #self.salvar_objeto(ingest.get_index(), "index1.dump")

    def ler_gabarito(self):
        self.gabarito = {}
        with open(self.GABARITO_QUERIES_PATH, 'r') as f:
            for linha in f:
                partes = linha.strip().split()
                chave = partes[0]
                valor = partes[2]
                pontos = int(partes[3])

                if pontos > 0:
                    if chave not in self.gabarito:
                        self.gabarito[chave] = {}
                    else:
                        self.gabarito[chave][valor] = pontos

    def conferir_gabarito(self, n_query, resultado):
        acertos = []
        #print(resultado)
        for res in resultado:
            if res.titulo in self.gabarito[n_query]:
                acertos.append(res.titulo)
        #print(acertos)
        return acertos



#ingest = Ingest()

#documents = listar_arquivos(DOCUMENTS_PATH)

#novo_index = carregar_objeto("index.dump")
#print(novo_index.get_collection_size())
#tarefa_demorada(documents)
