<a href="https://www.linkedin.com/in/fabiocamposgp/" target="blank"><img src="https://img.shields.io/badge/Author-Fabio%20Campos-green" /></a> <img src="https://img.shields.io/badge/python-3.7%2B-blue" />

<h1>Serviço para Conversão de Moedas</h1>
A finalidade dessa solução é buscar a taxa de cotação das moedas pré-selecionadas, para uma determinada data, via API disponibilizada pelo Banco Central do Brasil, e realizar a conversão dos valores entre as moedas.
<br><br>
<b>Premissas</b>
<ul>
    <li>Utilizar a API disponibilizada pelo Banco Central do Brasil para realizar a conversão entre as moedas.</li>
    <li>Utilizar sistema de cache para responder as cosultas com os mesmos parâmetros. O tempo de vida do cache é de 30 minutos e não pode ser renovado com novas requisições. O retorno da conversão para o usuário deverá informar se o resultado foi obtido pelo cache ou online.</li>
    <li>Utilizar um sistema de fila para o serviço com possibilidade de indicar se a requisição é com prioridade normal ou alta. Requisições com prioridade alta passam a frente das requisições com prioridade normal</li>
</ul>

<b>Como a solução funciona?</b><br>
Primeiramente, o usuário precisa informar os dados necessários, preenchendo os seguintes campos:
<ul>
  <li>Data da Cotação - Data na qual o usuário deseja buscar a taxa da cotação das moedas. Por padrão, o formato da data é dd/mm/YYYY.</li>
  <li>Prioridade - Prioridade que a requisição será atendida pelo serviço (normal e alta).</li>
  <li>Quantia - Quantia que será convertida entre as moedas.</li>
  <li>Converter de - Taxa de conversão da moeda que o usuário deseja converter.</li>
  <li>Para - Taxa de conversão para moeda que o usuário deseja converter.</li>
</ul>
Depois que o usuário preenche/seleciona todos os campos, o serviço envia a requisição para uma fila, que responde de acordo com a posição da requisição em relação as outras requisições e a prioridade selecionada. Quando chega o momento de atender a requisição do usuário, o gerenciador da fila chama o gerenciador da API que procura no gerenciador de cache uma solicitação com os mesmos parâmetros da consulta. Se o Gerenciador de cache não achar um registro correspondente, ele responde que nada foi encontrado e o gerenciador da API faz uma requisição online para a API do Banco Central do Brasil, passando os dados preenchidos/selecionados pelo usuário, e obtendo como retorno os dados de conversão das moedas. De posse dos dados, o gerenciador da API cria um arquivo de cache para a consulta e devolve os dados convertidos para o gerenciador da fila, que devolve o resultado convertido para o usuário final.
<br><br>
Todo esse processo pode ser visualizado pelo diagrama abaixo:
<br><br>
<img src="https://github.com/fcampos300/Conversao-Moedas/blob/master/Diagrama.png?raw=true" alt="Diagrama.png">
<br><br>
<b>Instalação</b><br>
Passo 1 - Como o serviço foi desenvolvido utilizando a linguagem Python 3.7+, o primeiro passo para configuração do ambiente é instalar o Python, caso não esteja instalado. Para isso, basta ir em https://www.python.org/downloads/ e baixar a última versão correspondente ao OS utilizado.
<br><br>
Passo 2 - Após a instalação do Python, também é necessário instalar a biblioteca Requests, para trabalhar com as requisições HTTP nas chamadas da API.<br>
Referência - https://pypi.org/project/requests/2.7.0/<br>
Instalação:<br>
<pre>pip install requests</pre>
Passo 3 - Clonar ou fazer download do repositório.<br>
Com o ambiente preparado e o serviço baixado, é só digitar o comando abaixo no terminal para rodar o aplicativo.
<pre>python converte.py</pre>
<br>
Em caso de algum problema/dúvida com as outras bibliotecas utilizadas pelo serviço na hora da instalação, elas podem ser encontradas nos seguintes links:<br>
tkinter: https://tkdocs.com/tutorial/install.html<br>
datetime: https://pypi.org/project/DateTime/<br>
json: https://pypi.org/project/jsonlib-python3/<br>
os: https://pypi.org/project/os-sys/<br>
<br>
<b>API</b><br>
A API utilizada para buscar a conversão é disponibilizada pelo Banco Central do Brasil e pode ser encontrada no link 
https://dadosabertos.bcb.gov.br/dataset/taxas-de-cambio-todos-os-boletins-diarios/resource/9d07b9dc-c2bc-47ca-af92-10b18bcd0d69<br>
Documentação: https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/documentacao
<br><br>
Ponto de acesso para as moedas:<br>
https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/Moedas?$top=100&$format=json&$select=simbolo,nomeFormatado<br>
Ponto de acesso para as cotações:<br>
https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)?@moeda=''&@dataCotacao=''&$top=100&$format=json
<br><br>
<b>Gerenciador de Fila</b><br>
Para esse case, foi desenvolvido um gerenciador simples, onde o próprio aplicativo gerencia as solicitações em uma lista Python. Para um sistema implementado, o ideal é um serviço agendado, rodando em real time, gerenciando todas as requisições do serviço via arquivo ou banco de dados. No case, eu tentei simular esse cenário, onde o usuário pode fazer várias solicitações de conversão, inclusive setando prioridade e só após o clique no botão de Processar, as requisições são atendidas.
<br><br>
<b>Gerenciador de Cache</b><br>
Sistema simples de cache em arquivo em disco. No case, a limpeza dos arquivos com mais de 30 minutos de geração é feito dentro do próprio aplicativo, porém, o ideal é agendar um serviço para realizar essa limpeza periodicamente. 
<br><br>
O sistema foi desenvolvido respeitando a premissa, porém, analisando com mais calma, o ideal seria fazer o cache das cotações e guardar por 30 minutos, e não da consulta em si. Por exemplo, na conversão de 1000 USD pra EUR, o sistema deveria guardar as cotações do USD e do EUR para usar em novas consultas por essas moedas, indiferente da quantia desejada.
<br><br>
<b>Caso de Uso</b><br>
Utilização da solução realizada no ambiente Windows 10.
<br><br>
Tela de entrada de parâmetros:<br>
<img src="https://github.com/fcampos300/Conversao-Moedas/blob/master/tela1.jpg?raw=true" alt="tela1.jpg">
<br>
Fila de processamento com 1 requisição:<br>
<img src="https://github.com/fcampos300/Conversao-Moedas/blob/master/tela2.jpg?raw=true" alt="tela2.jpg">
<br>
Fila de processamento com várias requisições:<br>
<img src="https://github.com/fcampos300/Conversao-Moedas/blob/master/tela3.jpg?raw=true" alt="tela3.jpg">
Resultado das conversões:<br>
<img src="https://github.com/fcampos300/Conversao-Moedas/blob/master/tela4.jpg?raw=true" alt="tela4.jpg">
