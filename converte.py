"""
Sistema de conversão de moedas baseado nos dados fornecidos através da API do Banco Central do Brasil.
"""
import sys
from tkinter import Tk, FALSE
from Classes.ApiRequisicao import ApiRequisicao
from Classes.ConversaoMoedasApp import ConversaoMoedasApp
from Classes.FilaProcessamento import FilaProcessamento


def main():
    # Inicializa o módulo Tk do tkinter.
    janela = Tk()
    # Impede o redimensionamento da janela.
    janela.resizable(width=FALSE, height=FALSE)
    # Chama a classe que vai montar os elementos da janela.
    ConversaoMoedasApp(janela, ApiRequisicao(), FilaProcessamento(), 570, 400)
    janela.mainloop()


if __name__ == "__main__":
    main()
