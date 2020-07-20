"""
Classe para montar o sistema de Cache das requisições.
Filesystem = cache/
"""
import os
from datetime import datetime
from os import listdir
from os.path import isfile, getmtime


class CacheRequisicao:

    def __init__(self, arquivo):
        self._arquivo = arquivo
        self._path = 'cache/'           # Pasta onde os arquivos de Cache ficam armazenados.
        self.cache_duracao = int(1800)  # O tempo de vida do Cache é de 1800 segundos (30 minutos).

    @property
    def arquivo(self):
        return self._arquivo

    @arquivo.setter
    def arquivo(self, valor):
        self._arquivo = valor

    def busca_cache(self):
        """
        Método que verifica se existe um arquivo de cache para a requisição.
        :return: Arquivo de Cache caso ele sena encontrado e esteja válido, caso contrário, retorna False.
        """
        # Varre a pasta cache e retorna o arquivo setado pela variável self._arquivo se ele for encontrado.
        # Ignora subpastas.
        cache = [arq for arq in listdir(self._path) if isfile(self._path + arq) and arq == self._arquivo]

        # Se o arquivo for encontrado, verifica se ele ainda é válido. Caso não seja, retorna False.
        if cache:
            return cache[0]
        else:
            return False

    def limpa_cache(self):
        """
        Limpa todos os arquivos de cache que não forem mais válidos, ou seja, com mais de 30 minutos de geração.
        :return:
        """
        arquivos = [arq for arq in listdir(self._path) if isfile(self._path + arq)]

        for cache in arquivos:
            # Busca a data/hora da última modificação do arquivo, a data/hora corrente e o delta entre as variáveis.
            ult_modificacao = datetime.fromtimestamp(getmtime(self._path + cache))
            data_corrente = datetime.now()
            delta = int((data_corrente - ult_modificacao).total_seconds())

            # Se o delta for inferior ao tempo de duração do Cache, retorna o arquivo de Cache.
            # Caso seja maior, exclui o arquivo e retorna False.
            if delta > self.cache_duracao:
                # Remove o arquivo da pasta Cache.
                try:
                    os.remove(self._path + cache)
                except OSError:
                    pass
