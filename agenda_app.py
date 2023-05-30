import tkinter as tk
import pyodbc

class AgendaApp:
    def __init__(self, root):
        self.root = root
        # Conectando com o SQL SERVER
        self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-RPGOE10\SQLEXPRESS;DATABASE=Agenda_de_Contatos')
        self.cursor = self.conn.cursor()
        self.criar_tabela()
        self.criar_interface()

    def criar_tabela(self):
        # Verificar se a tabela já existe
        tabela_existe = False
        for tabela in self.cursor.tables():
            if tabela.table_name == 'Agenda':
                tabela_existe = True
                break

        # Criar a tabela somente se ela não existir
        if not tabela_existe:
            self.cursor.execute('''
                CREATE TABLE Agenda (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    telefone VARCHAR(20)
                )
            ''')
            self.conn.commit()

    def criar_interface(self):
        label_nome = tk.Label(self.root, text="Nome:")
        label_nome.pack()
        self.entry_nome = tk.Entry(self.root)
        self.entry_nome.pack()

        label_telefone = tk.Label(self.root, text="Telefone:")
        label_telefone.pack()
        self.entry_telefone = tk.Entry(self.root)
        self.entry_telefone.pack()

        btn_adicionar = tk.Button(self.root, text="Adicionar", command=self.adicionar_contato)
        btn_adicionar.pack()

        self.lista_contatos = tk.Listbox(self.root)
        self.lista_contatos.pack()

        self.lista_contatos.bind('<<ListboxSelect>>', self.selecionar_contato)

        btn_atualizar = tk.Button(self.root, text="Atualizar", command=self.atualizar_contato)
        btn_atualizar.pack()

        btn_excluir = tk.Button(self.root, text="Excluir", command=self.excluir_contato)
        btn_excluir.pack()

        self.exibir_contatos()

    def adicionar_contato(self):
        nome = self.entry_nome.get()
        telefone = self.entry_telefone.get()

        self.cursor.execute('INSERT INTO Agenda (nome, telefone) VALUES (?, ?)', (nome, telefone))
        self.conn.commit()
        self.limpar_campos()
        self.exibir_contatos()

    def exibir_contatos(self):
        self.lista_contatos.delete(0, tk.END)
        self.cursor.execute('SELECT id, nome, telefone FROM Agenda')
        contatos = self.cursor.fetchall()
        for contato in contatos:
            self.lista_contatos.insert(tk.END, f'{contato[0]} - {contato[1]} - {contato[2]}')

    def selecionar_contato(self, event):
        indice = self.lista_contatos.curselection()[0]
        contato = self.lista_contatos.get(indice).split(' - ')
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(tk.END, contato[1])
        self.entry_telefone.delete(0, tk.END)
        self.entry_telefone.insert(tk.END, contato[2])

    def atualizar_contato(self):
        indice = self.lista_contatos.curselection()[0]
        contato = self.lista_contatos.get(indice).split(' - ')
        id_contato = contato[0]
        nome = self.entry_nome.get()
        telefone = self.entry_telefone.get()

        self.cursor.execute('UPDATE Agenda SET nome = ?, telefone = ? WHERE id = ?', (nome, telefone, id_contato))
        self.conn.commit()
        self.limpar_campos()
        self.exibir_contatos()

    def excluir_contato(self):
        indice = self.lista_contatos.curselection()[0]
        contato = self.lista_contatos.get(indice).split(' - ')
        id_contato = contato[0]

        self.cursor.execute('DELETE FROM Agenda WHERE id = ?', (id_contato,))
        self.conn.commit()
        self.limpar_campos()
        self.exibir_contatos()

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)


