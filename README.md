<a href="https://www.linkedin.com/in/fabiocamposgp/" target="blank"><img src="https://img.shields.io/badge/Author-Fabio%20Campos-green" /></a> <img src="https://img.shields.io/badge/python-3.7%2B-blue" />

<h1>Serviço para Conversão de Moedas</h1>
A finalidade desse serviço é buscar a taxa de cotação das moedas selecionadas no aplicativo, via API disponibilizada pelo Banco Central do Brasil, na data desejada e realizar a conversão dos valores entre as moedas.
<br><br>
<b>Premissas</b>
<ul>
    <li>Utilizar a API disponibilizada pelo Banco Central do Brasil para realizar a conversão entre as moedas.</li>
    <li>Utilizar sistema de cache para responder as cosultas com os mesmos parâmetros. O tempo de vida do cache é de 30 minutos e não pode ser renovado com novas requisições. O retorno da conversão para o usuário deverá informar se o resultado foi obtido pelo cache ou online.</li>
    <li>Utilizar um sistema de fila para o serviço com possibilidade de indicar se a requisição é com prioridade normal ou alta. Requisições com prioridade alta passam a frente das requisições com prioridade normal</li>
</ul>

<b>Como o serviço funciona?</b><br>
Primeiramente, o usuário precisa informar os dados para o serviço, preenchendo os seguintes campos:
<ul>
  <li>Data da Cotação - Data que o usuário deseja buscar a taxa da cotação das moedas. Por padrão, o formato da data é dd/mm/YYYY.</li>
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
Como o serviço foi desenvolvido utilizando a linguagem Python 3.7+, o primeiro passo para configuração do ambiente é instalar o Python, caso não esteja instalado. Para isso, basta ir em https://www.python.org/downloads/ e baixar a última versão correspondente ao OS utilizado.
<br><br>
Após a instalação do Python, é necessário instalar algumas bibliotecas utilizadas pelo serviço. As bibliotecas são:

