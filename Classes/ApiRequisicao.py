"""
Classe ApiRequisicao

Realiza requisições na Api do Banco Central do Brasil para buscar listagem de moedas disponíveis para conversão.

A documentação da API pode ser encontrada no site abaixo:
https://dadosabertos.bcb.gov.br/dataset/taxas-de-cambio-todos-os-boletins-diarios/resource/
9d07b9dc-c2bc-47ca-af92-10b18bcd0d69

A URL para fazer a requisição da listagem de moedas é:
https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/Moedas?$top=100&$format=json&$select=simbolo,nomeFormatado

O retorno é um arquivo JSON com a seguinte estrutura:
{
    "@odata.context": "https://was-p.bcnet.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata$metadata#Moedas...",
    "value": [
        {
            "simbolo": "AUD",
            "nomeFormatado": "Dólar australiano"
        },
        Outras moedas...
    ]
}

A URL para fazer a requisição da cotação é:
https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)?
@moeda='EUR'&@dataCotacao='07-17-2020'&$top=100&$format=json

O retorno é um arquivo JSON com a seguinte estrutura:
{
    "@odata.context": "https://was-p.bcnet.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata$metadata#_CotacaoMoedaDia",
    "value": [
        {
            "paridadeCompra": 1.1417,
            "paridadeVenda": 1.142,
            "cotacaoCompra": 6.112,
            "cotacaoVenda": 6.1143,
            "dataHoraCotacao": "2020-07-17 10:08:17.85",
            "tipoBoletim": "Abertura"
        }
    ]
}

"""
import json
import requests
from Classes.CacheRequisicao import CacheRequisicao


class ApiRequisicao(CacheRequisicao):

    def __init__(self, requisicao=None, arquivo=None):
        super().__init__(arquivo)
        self._requisicao = requisicao
        self._arquivo = arquivo

    @property
    def requisicao(self):
        return self._requisicao

    @requisicao.setter
    def requisicao(self, valor):
        self._requisicao = valor

    def busca_moedas(self):
        """
        Método para buscar uma lista com todas as moedas disponíveis para o sistema de conversão. O sistema usa
        cache de 30 minutos antes de fazer uma nova requisição para a API.
        :return: Lista com as moedas disponíveis para conversão.
        """
        # Nome do arquivo com a listagem de moedas.
        self._arquivo = 'moedas.json'

        # Limpa os arquivos de cache com mais de 30 minutos.
        self.limpa_cache()

        # Verifica se existe arquivo de cache para a listagem de moedas. Caso não exista, faz uma chamada da API.
        cache = self.busca_cache()

        if cache:
            moedas = ['BRL - Real']

            # Abre o arquivo JSON.
            with open(self._path + cache, 'r', encoding='UTF-8') as arquivo:
                js = json.loads(arquivo.read())

            # Monta a lista com todas as moedas no arquivo JSON.
            [moedas.append(f"{moeda['simbolo']} - {moeda['nomeFormatado']}") for moeda in js['value']]

            return moedas
        else:
            url = 'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/' \
                  'Moedas?$top=100&$format=json&$select=simbolo,nomeFormatado'
            response = requests.get(url)

            if response.status_code == 200:
                try:
                    js = response.json()
                    moedas = ['BRL - Real']

                    # Monta a lista com todas as moedas no arquivo JSON.
                    [moedas.append(f"{moeda['simbolo']} - {moeda['nomeFormatado']}") for moeda in js['value']]

                    # Gera o arquivo de Cache.
                    json_dados = json.dumps(js, ensure_ascii=False, indent=3)
                    with open(self._path + self._arquivo, 'w', encoding='utf-8') as arquivo:
                        arquivo.write(json_dados)

                    return moedas
                except requests.ConnectionError:
                    return False
            else:
                return False

    def busca_cotacao(self, requisicao):
        """
        Método para buscar a cotação da requisição de conversão, seja no Cache ou na API.
        :param requisicao: Lista com os parâmetros para realizar a requisição.
        :return: Dicionário com os dados da cotação.
        """

        def moeda_requisicao(data_cotacao, moeda):
            """
            Conecta na API e faz a requisição da cotação.
            :param data_cotacao: Data com a formatação (mm-dd-YYYY) requisitada pela API.
            :param moeda: Símbolo (USD) da moeda.
            :return: O último valor de cotação no momento que a requisição foi realizada, caso a resposta da API seja
                     positiva (cod 200).
            """
            url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/" \
                  f"CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)" \
                  f"?@moeda='{moeda}'&@dataCotacao='{data_cotacao}'&$top=100&$format=json"

            response = requests.get(url)

            if response.status_code == 200:
                try:
                    json_arq = response.json()
                    if json_arq['value']:
                        return json_arq['value'][-1]['cotacaoCompra']  # Pega o último valor de cotação.
                    else:
                        return 'erro_data_cotacao'
                except requests.ConnectionError:
                    return False
            else:
                return False

        # Limpa os arquivos de cache com mais de 30 minutos.
        self.limpa_cache()

        # Seta as variáveis.
        data = requisicao[0]
        quantia = requisicao[1]
        morigem = requisicao[2]
        mconvert = requisicao[3]

        # Verifica se já existe um resultado no Cache para a consulta.
        self.arquivo = f"{data.replace('-', '')}_{quantia}_{morigem}_{mconvert}.json"
        cache = self.busca_cache()
        if cache:
            ret_requisicao = 'cache'  # Indica que a requisição foi respondia pelo Cache.

            # Abre o arquivo JSON.
            with open(self._path + cache, 'r', encoding='UTF-8') as arquivo:
                js_cache = json.loads(arquivo.read())

            morigem_tax = js_cache['morigem_tax']
            mconvert_tax = js_cache['mconvert_tax']
        else:
            ret_requisicao = 'api'  # Indica que a requisição foi respondia pela API,

            # Verifica se a moeda de origem é BRL (Real). Se não for, tenta pegar um arquivo de Cache.
            if morigem != 'BRL':
                cotacao_origem = moeda_requisicao(data, morigem)
                morigem_tax = cotacao_origem
            else:
                morigem_tax = 1

            # Verifica se a moeda para conversão é BRL (Real). Se não for, tenta pegar um arquivo de Cache.
            if mconvert != 'BRL':
                cotacao_convert = moeda_requisicao(data, mconvert)
                mconvert_tax = cotacao_convert
            else:
                mconvert_tax = 1

        # Dicionário com as cotações.
        cotacoes = {
            'data': data,                  # Data da cotação.
            'quantia': quantia,            # Quantia a ser convertida.
            'morigem': morigem,            # Moeda de origem.
            'morigem_tax': morigem_tax,    # Cotação da moeda de origem.
            'mconvert': mconvert,          # Moeda a ser convertida.
            'mconvert_tax': mconvert_tax,  # Cotação da moeda a ser convertida.
            'retorno': ret_requisicao      # Indica se a requisição foi atendida via Cache ou API.
        }

        # Se a consulta foi atendida pela API, gera um arquivo de Cache.
        if ret_requisicao == 'api':
            # Gera o arquivo de Cache.
            json_dados = json.dumps(cotacoes, ensure_ascii=False, indent=3)

            with open(self._path + self._arquivo, 'w', encoding='utf-8') as arquivo_json_url:
                arquivo_json_url.write(json_dados)

        return cotacoes
