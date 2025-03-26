import pandas as pd  # Manipulação de dados
import random
import string
import tkinter as tk
from tkinter import ttk, messagebox

# Definição dos dados
placas = ['RVT-694', 'RVT-695', 'RVT-696', 'RVT-697', 'RVT-698', 'RVT-699', 'RVT-700', 'RVT-701']
cliente = ['cemig' for _ in range(len(placas))]
id = [''.join(random.choices(string.digits, k=15)) for _ in range(len(placas))]
km = [random.randint(0, 700) for _ in range(len(placas))]
time = [('minutos:', random.randint(0, 1440)) for _ in range(len(placas))]

# DataFrame
df = pd.DataFrame({'Placas': placas, 'Time': time, 'Cliente': cliente, 'KM': km, 'ID': id})

# Classe principal
class Comandos1:
    def __init__(self, placas, time):
        self.placas = placas
        self.time = time

    def numero_placas(self):
        return len(self.placas)

    def sec_time(self):
        sec = [x[1] * 60 for x in df['Time']]
        return sec

class Gera_Placa(Comandos1):
    def gera_placa(self):
        return ''.join(random.choices(string.ascii_uppercase, k=3)) + '-' + str(random.randint(100, 999))

    def adicionar_placa_a_df(self, nova_placa):
        novo_id = ''.join(random.choices(string.digits, k=15))
        novo_km = random.randint(0, 700)
        novo_time = ('minutos:', random.randint(0, 1440))
        novo_cliente = 'cemig'
        novo_registro = {'Placas': [nova_placa], 'Time': [novo_time], 'Cliente': [novo_cliente], 'KM': [novo_km], 'ID': [novo_id]}
        global df
        df = pd.concat([df, pd.DataFrame(novo_registro)], ignore_index=True)

# Criando interface Tkinter
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciamento de Placas")
        
        self.frame = ttk.Frame(root, padding=10)
        self.frame.grid()
        
        ttk.Label(self.frame, text="Número de placas:").grid(column=0, row=0)
        self.placas_count = ttk.Label(self.frame, text=str(len(placas)))
        self.placas_count.grid(column=1, row=0)
        
        ttk.Button(self.frame, text="Gerar Nova Placa", command=self.gerar_placa).grid(column=0, row=1)
        self.placa_gerada = ttk.Label(self.frame, text="")
        self.placa_gerada.grid(column=1, row=1)
        
        ttk.Button(self.frame, text="Adicionar ao DataFrame", command=self.adicionar_placa).grid(column=0, row=2)
        
        ttk.Button(self.frame, text="Converter Tempo para Segundos", command=self.converter_segundos).grid(column=0, row=3)
        
        self.tree = ttk.Treeview(self.frame, columns=("Placas", "Time", "Cliente", "KM", "ID"), show="headings")
        for col in ["Placas", "Time", "Cliente", "KM", "ID"]:
            self.tree.heading(col, text=col)
        self.tree.grid(column=0, row=4, columnspan=2)
        self.atualizar_tabela()
    
    def gerar_placa(self):
        self.placa_nova = Gera_Placa(placas, time).gera_placa()
        self.placa_gerada.config(text=self.placa_nova)
    
    def adicionar_placa(self):
        if hasattr(self, 'placa_nova') and self.placa_nova:
            Gera_Placa(placas, time).adicionar_placa_a_df(self.placa_nova)
            self.atualizar_tabela()
            self.placas_count.config(text=str(len(df)))
            messagebox.showinfo("Sucesso", f"Placa {self.placa_nova} adicionada com sucesso!")
    
    def converter_segundos(self):
        df['Time'] = [("segundos:", x[1] * 60) for x in df['Time']]
        self.atualizar_tabela()
        messagebox.showinfo("Conversão Concluída", "Os tempos foram convertidos para segundos!")
    
    def atualizar_tabela(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=tuple(row))

# Executando a aplicação
root = tk.Tk()
app = App(root)
root.mainloop()