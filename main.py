import tkinter as tk
from agenda_app import AgendaApp

# Criar a janela principal
root = tk.Tk()
root.title("Agenda")
root.geometry('220x325')

# Criar a instância do aplicativo de agenda
app = AgendaApp(root)

# Iniciar o loop principal da aplicação
root.mainloop()

