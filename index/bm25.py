from documentos.models import Documento as document_model
from documentos.models import Token as token_model
from .util import Util
import math
import numpy as np
from multiprocessing import Pool, cpu_count
from collections import Counter
from django.db.models import Sum
"""
All of these algorithms have been taken from the paper:
Trotmam et al, Improvements to BM25 and Language Models Examined
Here we implement all the BM25 variations mentioned. 
"""
"""
class BM25:
    def __init__(self, documents):
        self.documents = documents
        self.document_count = len(documents)
        self.avg_document_length = sum(len(doc) for doc in documents) / self.document_count
        self.term_counts = self.calculate_term_counts()
        self.k1 = 1.2
        self.b = 0.75

    def calculate_term_counts(self):
        term_counts = Counter()
        for document in self.documents:
            term_counts.update(document)
        return term_counts

    def calculate_idf(self, term):
        document_with_term_count = self.term_counts[term]
        return math.log((self.document_count - document_with_term_count + 0.5) / (document_with_term_count + 0.5))

    def calculate_bm25_score(self, query, document):
        score = 0.0
        document_length = len(document)
        query_terms = Counter(query)

        for term in query_terms:
            if term not in self.documents:
                continue
            idf = self.calculate_idf(term)
            term_frequency = document.count(term)
            numerator = term_frequency * (self.k1 + 1)
            denominator = term_frequency + self.k1 * (1 - self.b + self.b * (document_length / self.avg_document_length))
            score += idf * (numerator / denominator)

        return score

    def rank_documents(self, query):
        document_scores = []
        for document in self.documents:
            score = self.calculate_bm25_score(query, document)
            document_scores.append((document, score))
        
        ranked_documents = sorted(document_scores, key=lambda x: x[1], reverse=True)
        return ranked_documents

"""
class BM25:
    def __init__(self):
        self.corpus_size = document_model.objects.count()
        self.avgdl = document_model.objects.aggregate(TOTAL = Sum('tamanho'))['TOTAL'] / self.corpus_size
        self.doc_freqs = []
        self.idf = {}
        self.doc_len = []
        self.doc_names = []

        #nd = self._initialize(corpus)
        #nd = self._initialize(document_model.objects.all())
        #self._calc_idf(nd)

    def __limpar_busca(self) -> None:
        self.doc_freqs = []
        self.idf = {}
        self.doc_len = []
        self.doc_names = []

    def _initialize(self, corpus):
        nd = {}  # word -> number of documents with word
        num_doc = 0
        print(len(corpus))
        #self.corpus_size = document_model.objects.count()
        #print(self.corpus_size)
        #self.avgdl = document_model.objects.aggregate(TOTAL = Sum('tamanho'))['TOTAL'] / self.corpus_size
        for documento in corpus:
            #self.doc_len.append(documento.tamanho)
            num_doc += documento.tamanho
            #self.doc_names.append(documento.id)
            print(documento.tamanho)
            frequencies = {}
           # for token in token_model.objects.all():
            #    frequencies[token.termo] = token.quantidade
            #self.doc_freqs.append(frequencies)
            #doc_freqs guarda docs = [{word: freq}]
            for word, freq in frequencies.items():
                try:
                    nd[word]+=1
                except KeyError:
                    nd[word] = 1
        return nd

    def _tokenize_corpus(self, corpus):
        pool = Pool(cpu_count())
        tokenized_corpus = pool.map(self.tokenizer, corpus)
        return tokenized_corpus

    def _calc_idf(self, nd):
        raise NotImplementedError()

    def get_scores(self, query):
        raise NotImplementedError()

    def get_batch_scores(self, query, doc_ids):
        raise NotImplementedError()

    def get_top_n(self, query, stemmer, cache_query, n=5):

      #  assert self.corpus_size == len(documents), "The documents given don't match the index corpus!"

        query = stemmer.text_stemming(query)
        #print(query)
        scores, documentos, novo_cache_query = self.get_scores(query, stemmer, cache_query)
        #print(scores)
        #top_n = np.argsort(scores)[::-1][:n]
        #print(top_n)
        top_documentos = self.get_document_models(scores, documentos)
        top_documentos = top_documentos[:n]
        #print(top_documents)
        self.__limpar_busca()
        return top_documentos , novo_cache_query
    
    def get_document_models(self, top_n, documentos):
        selected_documents = []
        docs_ordenados = []
        best_scores = []
        util = Util()

        scores_ordenados = dict(sorted(top_n.items(), key=lambda item: item[1], reverse=True))
        #print(scores_ordenados)
        for k, v in scores_ordenados.items():
            #print(k)
            doc = documentos.get(k)
            docs_ordenados.append([doc,v])
        #print(documentos)
        #print(docs_ordenados)
        return docs_ordenados

class BM25Okapi(BM25):
    def __init__(self, k1=1.5, b=0.75, epsilon=0.25):
        self.k1 = k1
        self.b = b
        self.epsilon = epsilon
        super().__init__()

    def _calc_idf(self, tokens):
        

        """
        Calculates frequencies of terms in documents and in corpus.
        This algorithm sets a floor on the idf values to eps * average_idf
        """
        #self.idf = {}
        # collect idf sum to calculate an average idf for epsilon value
        idf_sum = 0
        # collect words with negative idf to set them a special epsilon value.
        # idf can be negative if word is contained in more than half of documents
        negative_idfs = []
        for t in tokens:
            idf = math.log(self.corpus_size - t.quantidade + 0.5) - math.log(t.quantidade + 0.5)
            self.idf[t.id_token] = idf
            idf_sum += idf
            if idf < 0:
                negative_idfs.append(word)

        
        self.average_idf = (idf_sum / len(self.idf)) if len(self.idf) > 0 else 0

        eps = self.epsilon * self.average_idf
        for word in negative_idfs:
            self.idf[t.id_token] = eps

    def get_scores(self, query, stemmer, cache_query):
        """
        The ATIRE BM25 variant uses an idf function which uses a log(idf) score. To prevent negative idf scores,
        this algorithm also adds a floor to the idf value of epsilon.
        See [Trotman, A., X. Jia, M. Crane, Towards an Efficient and Effective Search Engine] for more info
        :param query:
        :return:
        """
        #score = np.zeros(self.corpus_size)
        #doc_len = np.array(self.doc_len)
        tokens = []
        #score = []
        vetor_query = query.split()
        vetor_query = list(filter(lambda tok: len(tok) > 2, vetor_query))
        print(vetor_query) 
        for q in vetor_query:
            busca = cache_query.get(q) or None
            if(busca == None):
                print(f"nao pulou {q}")
                busca = token_model.objects.filter(termo__startswith=q)
                cache_query[q] = busca
            lista_filtrada = list(filter(lambda tok: stemmer.text_stemming(tok.termo).rstrip() == q, busca))
            tokens += lista_filtrada
    
            #q_freq = np.array([(doc.get(q) or 0) for doc in self.doc_freqs])
           # print(self.doc_freqs[0].get(q))
           # for i in q_freq:
           #     print(i)
          #  print(self.idf.get(q))
            #score += (self.idf.get(q) or 0) * (q_freq * (self.k1 + 1) /
             #                                  (q_freq + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)))
           # print(score)
        self._calc_idf(tokens)
        documentos = {}

        scores = {}
        for t in tokens:
            documentos[t.documento.id] = t.documento
            #print(q)
           # print(self.idf.get(t.id_token))
            score = (self.idf.get(t.id_token) or 0) * (t.quantidade * (self.k1 + 1) /
                                               (t.quantidade + self.k1 * (1 - self.b + self.b * t.documento.tamanho / self.avgdl)))
            if t.documento.id in scores:
                scores[t.documento.id] += score
            else:
                scores[t.documento.id] = score
        
        
        return scores, documentos, cache_query

    def get_batch_scores(self, query, doc_ids):
        """
        Calculate bm25 scores between query and subset of all docs
        """
        assert all(di < len(self.doc_freqs) for di in doc_ids)
        score = np.zeros(len(doc_ids))
        doc_len = np.array(self.doc_len)[doc_ids]
        for q in query:
            q_freq = np.array([(self.doc_freqs[di].get(q) or 0) for di in doc_ids])
            score += (self.idf.get(q) or 0) * (q_freq * (self.k1 + 1) /
                                               (q_freq + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)))
        return score.tolist()


class BM25L(BM25):
    def __init__(self , tokenizer=None, k1=1.5, b=0.75, delta=0.5):
        # Algorithm specific parameters
        self.k1 = k1
        self.b = b
        self.delta = delta
        super().__init__( )

    def _calc_idf(self, tokens):
        #self.idf = {
        #print(len(tokens))
        for t in tokens:
            #print(t.__str__())
            idf = math.log(self.corpus_size + 1) - math.log(len(tokens) + 0.5)
            self.idf[t.id_token] = idf
        

 #   def get_scores(self, query):
#        score = np.zeros(self.corpus_size)
 #       doc_len = np.array(self.doc_len)
#        for q in query:
#            q_freq = np.array([(doc.get(q) or 0) for doc in self.doc_freqs])
#            ctd = q_freq / (1 - self.b + self.b * doc_len / self.avgdl)
#            score += (self.idf.get(q) or 0) * (self.k1 + 1) * (ctd + self.delta) / \
#                     (self.k1 + ctd + self.delta)
#        return score

    def get_scores(self, query, stemmer,cache_query):
        
        tokens = []
        #score = []
        vetor_query = query.split()
        vetor_query = list(filter(lambda tok: len(tok) > 2, vetor_query))
        print(vetor_query) 
        for q in vetor_query:
            busca = cache_query.get(q) or None
            if(busca == None):
                print(f"nao pulou {q}")
                busca = token_model.objects.filter(termo__startswith=q)
                cache_query[q] = busca           
            lista_filtrada = list(filter(lambda tok: stemmer.text_stemming(tok.termo).rstrip() == q, busca))
            tokens += lista_filtrada
            #busca = [tok for tok in busca if stemmer.text_stemming(tok.termo) == q]
            #for t in lista_filtrada:
                #stem = stemmer.text_stemming(t.termo)
                #print(stem.rstrip() , " - ", len(stem), q, q == stem.rstrip())

            
        #print(len(tokens))
        self._calc_idf(tokens)
        documentos = {}
        #print(self.idf)
        scores = {}
        for t in tokens:
            
            documentos[t.documento.id] = t.documento
            
            #print(q)
           # print(self.idf.get(t.id_token))
            ctd = t.quantidade / (1 - self.b + self.b * t.documento.tamanho / self.avgdl)
            score = (self.idf.get(q) or 0) * (self.k1 + 1) * (ctd + self.delta) / \
                     (self.k1 + ctd + self.delta)
            
            if t.documento.id in scores:
                scores[t.documento.id] += score
                #print("foi")
            else:
                scores[t.documento.id] = score
                #print("foi2")
        
        
        return scores, documentos, cache_query


    def get_batch_scores(self, query, doc_ids):
        """
        Calculate bm25 scores between query and subset of all docs
        """
        assert all(di < len(self.doc_freqs) for di in doc_ids)
        score = np.zeros(len(doc_ids))
        doc_len = np.array(self.doc_len)[doc_ids]
        for q in query:
            q_freq = np.array([(self.doc_freqs[di].get(q) or 0) for di in doc_ids])
            ctd = q_freq / (1 - self.b + self.b * doc_len / self.avgdl)
            score += (self.idf.get(q) or 0) * (self.k1 + 1) * (ctd + self.delta) / \
                     (self.k1 + ctd + self.delta)
        return score.tolist()


class BM25Plus(BM25):
    def __init__(self, tokenizer=None, k1=1.5, b=0.75, delta=1):
        # Algorithm specific parameters
        self.k1 = k1
        self.b = b
        self.delta = delta
        super().__init__()

   # def _calc_idf(self, nd):
   #     for word, freq in nd.items():
   #         idf = math.log((self.corpus_size + 1) / freq)
   #         self.idf[word] = idf

    def _calc_idf(self, tokens):
        #self.idf = {}
        for t in tokens:
            if (t.quantidade == 0):
                idf = math.log((self.corpus_size + 1) / 1)
            else:
                idf = math.log((self.corpus_size + 1) / t.quantidade)
            self.idf[t.id_token] = idf

   # def get_scores(self, query):
   #     tokens = []
   #     score = []
   #     score = np.zeros(self.corpus_size)
   #     doc_len = np.array(self.doc_len)
   #     for q in query:
   #         q_freq = np.array([(doc.get(q) or 0) for doc in self.doc_freqs])
   #         score += (self.idf.get(q) or 0) * (self.delta + (q_freq * (self.k1 + 1)) /
   #                                            (self.k1 * (1 - self.b + self.b * doc_len / self.avgdl) + q_freq))
   #     return score

    def get_scores(self, query, stemmer, cache_query):
        tokens = []
        #score = []
        vetor_query = query.split()
        vetor_query = list(filter(lambda tok: len(tok) > 2, vetor_query))
        print(vetor_query) 
        for q in vetor_query:
            busca = cache_query.get(q) or None
            if(busca == None):
                print(f"nao pulou {q}")
                busca = token_model.objects.filter(termo__startswith=q)
                cache_query[q] = busca
            lista_filtrada = list(filter(lambda tok: stemmer.text_stemming(tok.termo).rstrip() == q, busca))
            tokens += lista_filtrada  
            
        self._calc_idf(tokens)
        documentos = {}

        scores = {}
        for t in tokens:
            documentos[t.documento.id] = t.documento

            score = (self.idf.get(t.id_token) or 0) * (self.delta + (t.quantidade * (self.k1 + 1)) /
                                               (self.k1 * (1 - self.b + self.b * t.documento.tamanho / self.avgdl) + t.quantidade))
            if t.documento.id in scores:
                scores[t.documento.id] += score
            else:
                scores[t.documento.id] = score
        
        
        return scores, documentos, cache_query

    def get_batch_scores(self, query, doc_ids):
        """
        Calculate bm25 scores between query and subset of all docs
        """
        assert all(di < len(self.doc_freqs) for di in doc_ids)
        score = np.zeros(len(doc_ids))
        doc_len = np.array(self.doc_len)[doc_ids]
        for q in query:
            q_freq = np.array([(self.doc_freqs[di].get(q) or 0) for di in doc_ids])
            score += (self.idf.get(q) or 0) * (self.delta + (q_freq * (self.k1 + 1)) /
                                               (self.k1 * (1 - self.b + self.b * doc_len / self.avgdl) + q_freq))
        return score.tolist()


# BM25Adpt and BM25T are a bit more complicated than the previous algorithms here. Here a term-specific k1
# parameter is calculated before scoring is done

# class BM25Adpt(BM25):
#     def __init__(self, corpus, k1=1.5, b=0.75, delta=1):
#         # Algorithm specific parameters
#         self.k1 = k1
#         self.b = b
#         self.delta = delta
#         super().__init__(corpus)
#
#     def _calc_idf(self, nd):
#         for word, freq in nd.items():
#             idf = math.log((self.corpus_size + 1) / freq)
#             self.idf[word] = idf
#
#     def get_scores(self, query):
#         score = np.zeros(self.corpus_size)
#         doc_len = np.array(self.doc_len)
#         for q in query:
#             q_freq = np.array([(doc.get(q) or 0) for doc in self.doc_freqs])
#             score += (self.idf.get(q) or 0) * (self.delta + (q_freq * (self.k1 + 1)) /
#                                                (self.k1 * (1 - self.b + self.b * doc_len / self.avgdl) + q_freq))
#         return score
#
#
# class BM25T(BM25):
#     def __init__(self, corpus, k1=1.5, b=0.75, delta=1):
#         # Algorithm specific parameters
#         self.k1 = k1
#         self.b = b
#         self.delta = delta
#         super().__init__(corpus)
#
#     def _calc_idf(self, nd):
#         for word, freq in nd.items():
#             idf = math.log((self.corpus_size + 1) / freq)
#             self.idf[word] = idf
#
#     def get_scores(self, query):
#         score = np.zeros(self.corpus_size)
#         doc_len = np.array(self.doc_len)
#         for q in query:
#             q_freq = np.array([(doc.get(q) or 0) for doc in self.doc_freqs])
#             score += (self.idf.get(q) or 0) * (self.delta + (q_freq * (self.k1 + 1)) /
#                                                (self.k1 * (1 - self.b + self.b * doc_len / self.avgdl) + q_freq))
#         return score