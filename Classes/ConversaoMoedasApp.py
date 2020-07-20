"""
Classe para montar a janela do script de conversão de moedas utilizando a biblioteca tkinter do Python.
"""
from datetime import datetime
from tkinter import *
from tkinter import messagebox, font, ttk, scrolledtext
from tkinter.ttk import Combobox


class ConversaoMoedasApp(Frame):

    def __init__(self, janela, api, fila, w_janela=200, h_janela=100):
        """
        Método construtor da Classe.
        :param janela: Objeto instanciado do tkinter.
        :param api: Objeto instanciado da classe ApiRequisicao.
        :param w_janela: Largura da janela. Default 200, caso o parâmetro não seja passado.
        :param h_janela: Altura da janela. Default 100, caso o parâmetro não seja passado.
        """
        Frame.__init__(self, janela, background="white")
        self.janela = janela
        self.api = api
        self.fila = fila
        self.w_janela = w_janela
        self.h_janela = h_janela
        self.style = ttk.Style()         # instancia o estilo da janela.
        self.style.theme_use("default")  # Seta como estilo default.
        self.centraliza_janela()         # Centraliza a janela na tela.
        self.monta_janela()              # Monta a janela.

    def centraliza_janela(self):
        """
        Método para centralizar a abertura da janela de acordo com a resolução da tela.
        """
        novo_x = (self.janela.winfo_screenwidth() - self.w_janela) / 2
        novo_y = (self.janela.winfo_screenheight() - self.h_janela) / 2
        self.janela.geometry('%dx%d+%d+%d' % (self.w_janela, self.h_janela, novo_x, novo_y))

    def valida_data(self, dt):
        """
        Método para validação de datas.
        :param dt: String com a data desejada no formato dd/mm/YYYY.
        :return: Caso o parâmetro seja passado no formato correto, retorna uma lista de 3 elementos, sendo:
                    Pos 0 -> Objeto datetime com a data passada como parâmetro.
                    Pos 1 -> Objeto datetime com a data corrente (dd/mm/YYYY).
                    Pos 2 -> A diferança de dias entre as duas datas.
                 Caso o parâmetro seja passado no formato incorreto, retorna False.
        """
        try:
            data = datetime.strptime(dt, "%d/%m/%Y").date()
            data_hoje = datetime.strptime(str(datetime.now().strftime("%d/%m/%Y"))[:10], "%d/%m/%Y").date()
            delta_data = (data - data_hoje).days

            return [data, data_hoje, delta_data]
        except ValueError:
            return False

    def monta_janela(self):
        """
        Método para montar a janela com todos os objetos necessários para realizar a conversão de moedas.
        """
        def acao_agendamento():
            """
            Função para realizar a conversão das moedas.
            """
            # Seta as variáveis locais.
            data = self.valida_data(entry_data.get())
            quantia = entry_quantia.get()
            moeda1 = combo_morigem.get()
            moeda2 = combo_mconvert.get()

            if not quantia.isdigit():
                messagebox.showerror('Erro!', 'Por favor, digite apenas números no campo Quantia.')
                entry_quantia.focus()
            elif not data:
                messagebox.showerror('Erro!', 'Formato inválido! Favor usar o formato dd/mm/YYYY')
                entry_data.focus()
            elif data[0].weekday() == 5 or data[0].weekday() == 6:
                messagebox.showerror('Erro!', 'Para dias não úteis, escolha a cotação do último dia útil anterior a '
                                              'data seleciona.')
                entry_data.focus()
            elif data[2] > 0:
                messagebox.showerror('Erro!', 'A Data da Cotação não pode ser maior que a data de hoje.')
                entry_data.focus()
            elif not quantia or int(quantia) == 0:
                messagebox.showerror('Erro!', 'Por favor, digite a quantia que deseja converter.')
                entry_quantia.focus()
            elif moeda1 == moeda2:
                messagebox.showerror('Erro!', 'Por favor, selecione moedas diferentes para realizar a conversão.')
                combo_mconvert.focus()
            else:
                # Monta uma lista para ser inserida na fila de processamento.
                item = [
                    f"{data[0].month}-{data[0].day}-{data[0].year}",  # Data padrão que a API pede;
                    int(quantia),                                     # Quantia;
                    moeda1.split('-')[0].strip(),                     # Moeda Origem;
                    moeda2.split('-')[0].strip(),                     # Moeda para conversão;
                    f"{data[0].day}/{data[0].month}/{data[0].year}",  # Data padrão BR;
                ]

                # Verifica se a inserção é prioridade normal ou alta.
                if self.selecionado.get() == 'Normal':
                    self.fila.inserir_prioridade_normal(item)
                else:
                    self.fila.inserir_prioridade_alta(item)

                # Busca a fila para inserir no grid.
                fila_processamento = self.fila.busca_fila()
                if fila_processamento:
                    # Frame Fila Processamento.
                    frame_fila = Frame(self.janela)
                    frame_fila.grid(row=2, column=0, sticky=W, pady=5)

                    # Labels.
                    lbl_fila = Label(frame_fila, text="Fila de Processamento", font=fonte)
                    lbl_fila.grid(column=0, row=0, sticky=W, padx=padx, pady=pady)

                    # Adiciona os itens da fila.
                    texto = ''
                    for item in fila_processamento:
                        texto += f"{item[1]} {item[2]} para {item[3]} na cotação do dia {item[4]}\n"

                    # Monta o frame que vai receber o texto com os elementos da fila.
                    frame_texto = scrolledtext.ScrolledText(self.janela, height=12, width=86, font=("Arial", 8))
                    frame_texto.insert("end", texto)
                    frame_texto.grid(row=3, column=0)

                    # Botões.
                    btn_proc = Button(self.janela, text="Processar", bg="blue", fg="white", command=acao_processar)
                    btn_proc.grid(row=4, column=0, pady=12)

        def acao_processar():
            # Busca a fila de processamento.
            fila_processamento = self.fila.busca_fila()

            # Monta o frame que vai receber o texto com os elementos da fila.
            frame_texto = scrolledtext.ScrolledText(self.janela, height=12, width=86, font=("Arial", 8))

            # Insere o Frame no grid.
            frame_texto.grid(row=3, column=0)

            for item in fila_processamento:
                # Busca o resultado da requisição.
                req = self.api.busca_cotacao(item)

                texto1 = f"{item[1]} {item[2]} para {item[3]} na cotação do dia {item[4]}\n"

                if req['morigem_tax'] == 'erro_data_cotacao' or req['mconvert_tax'] == 'erro_data_cotacao':
                    texto2 = ('Sem taxa de conversão disponível. Tente novamente mais tarde!\n', 'erro')
                else:
                    # Seta as variáveis.
                    morigem_tax = float(req['morigem_tax'])
                    mconvert_tax = float(req['mconvert_tax'])
                    quantia = float(req['quantia'])

                    # Faz o cálculo da conversão unitária.
                    calc_unitario = morigem_tax / mconvert_tax
                    calc_unitario = round(calc_unitario, 4)

                    # Faz o cálculo da conversão pela quantia.
                    calc_quantia = (morigem_tax * quantia) / mconvert_tax
                    calc_quantia = round(calc_quantia, 4)

                    msg = f"1 {req['morigem']} = {calc_unitario} {req['mconvert']}\n"
                    msg += f"Resultado da conversão: {calc_quantia} {req['mconvert']}\n"
                    if req['retorno'] == 'api':
                        msg += 'Dados gerados a partir da taxa de conversão fornecida pela API do BCB.\n'
                    else:
                        msg += 'Dados gerados a partir da taxa de conversão armazenada no Cache do sistema.\n'

                    texto2 = (msg, 'ok')

                texto3 = f"{129 * '-'}\n"

                frame_texto.insert("end", texto1)
                frame_texto.insert("end", texto2[0], texto2[1])
                frame_texto.insert("end", texto3)
                frame_texto.tag_config('erro', foreground='red')  # Linha vermelha em caso de erro.
                frame_texto.tag_config('ok', foreground='blue')   # Linha azul em caso de sucesso.
                frame_texto.update()                              # Atualiza o insert linha por linha.

            # Esvazia a fila.
            self.fila.limpa_fila()

        # Configura os Paddings.
        padx = 5
        pady = 5
        ipady = 2

        # Busca a listagem com as moedas disponíveis para conversão.
        moedas = self.api.busca_moedas()

        # Configura a fonte para ser usada nos Labels.
        fonte = font.Font(family='Arial', size=10, weight='bold')

        self.janela.title("Conversão de Moedas")

        # Frame Data de Cotação.
        frame_data = Frame(self.janela)

        # Labels.
        lbl_data = Label(frame_data, text="Data da Cotação", font=fonte)
        lbl_data.grid(column=0, row=0, sticky=W, padx=padx, pady=pady)
        lbl_espaco = Label(frame_data, width=15, text="", font=fonte)
        lbl_espaco.grid(column=2, row=0, sticky=W, padx=padx, pady=pady)
        lbl_prioridade = Label(frame_data, text="Prioridade", font=fonte)
        lbl_prioridade.grid(column=3, row=0, sticky=W, padx=padx, pady=pady)

        # Inputs.
        dt_hoje = str(datetime.now().strftime("%d/%m/%Y"))[:10]
        entry_data = Entry(frame_data, width=11, borderwidth=1)
        entry_data.insert(END, dt_hoje)
        entry_data.grid(column=1, row=0, sticky=W, padx=padx, pady=pady, ipady=ipady)
        self.selecionado = StringVar()  # Inicializa a variável para usar no RadioButton de prioridade.
        self.selecionado.set('Normal')  # Seta o valor 'Normal' como default.
        radio1 = Radiobutton(frame_data, text='Normal', value='Normal', variable=self.selecionado)
        radio1.grid(column=4, row=0, sticky=W, padx=padx, pady=pady, ipady=ipady)
        radio2 = Radiobutton(frame_data, text='Alta', value='Alta', variable=self.selecionado)
        radio2.grid(column=5, row=0, sticky=W, padx=padx, pady=pady, ipady=ipady)

        # Frame Conversão de Moedas.
        frame_moedas = Frame(self.janela)

        # Labels.
        lbl_quantia = Label(frame_moedas, text="Quantia", font=fonte)
        lbl_quantia.grid(column=0, row=1, sticky=W, padx=padx, pady=pady)
        lbl_morigem = Label(frame_moedas, text="Converter de", font=fonte)
        lbl_morigem.grid(column=1, row=1, sticky=W, padx=padx, pady=pady)
        lbl_mconvert = Label(frame_moedas, text="Para", font=fonte)
        lbl_mconvert.grid(column=2, row=1, sticky=W, padx=padx, pady=pady)

        # Inputs.
        entry_quantia = Entry(frame_moedas, width=12, borderwidth=1)
        entry_quantia.insert(END, 0)
        entry_quantia.grid(column=0, row=2, sticky=W, padx=padx, pady=pady, ipady=ipady)

        combo_morigem = Combobox(frame_moedas, width=30, state="readonly")
        combo_morigem['values'] = moedas
        combo_morigem.current(0)
        combo_morigem.grid(column=1, row=2, sticky=W, padx=padx, pady=pady, ipady=ipady)

        combo_mconvert = Combobox(frame_moedas, width=30, state="readonly")
        combo_mconvert['values'] = moedas
        combo_mconvert.current(0)
        combo_mconvert.grid(column=2, row=2, sticky=W, padx=padx, pady=pady, ipady=ipady)

        # Botões.
        btn = Button(frame_moedas, text="Converter", bg="blue", fg="white", command=acao_agendamento)
        btn.grid(column=3, row=2, sticky=W)

        # Insere os grids no Frame pai (janela).
        self.janela.grid()
        frame_data.grid(row=0, column=0, sticky=W)
        frame_moedas.grid(row=1, column=0, sticky=W, pady=15)
