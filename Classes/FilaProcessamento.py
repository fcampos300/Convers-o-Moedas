"""
Classe para montar a fila de processamento das requisições de conversão.
"""


class FilaProcessamento:

    def __init__(self):
        self.itens = list()

    def inserir_prioridade_alta(self, item):
        self.itens.insert(0, item)

    def inserir_prioridade_normal(self, item):
        self.itens.append(item)

    def busca_fila(self):
        return self.itens

    def limpa_fila(self):
        self.itens.clear()
