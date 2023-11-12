class Util:
    def __init__(self):
        pass
    
    def indices_maior_valor(self, vetor):
        retorno = []
        for i in range(len(vetor)):
            pos_max_valor = self.pos_maior_valor(vetor)
            retorno.append(pos_max_valor)
            vetor[pos_max_valor] = None
        return retorno

    def pos_maior_valor(self, vetor):
        if not vetor:
            return None

        maior_valor = vetor[0]
        posicao_maior_valor = 0

        for i in range(1, len(vetor)):
            if vetor[i] > maior_valor:
                maior_valor = vetor[i]
                posicao_maior_valor = i

        return posicao_maior_valor
    