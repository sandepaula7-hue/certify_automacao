import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class FormularioProgramaY:
    def __init__(self, root):
        self.root = root
        self.root.title("Programa Y - Formulário de Cadastro")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Título
        title_label = tk.Label(root, text="FORMULÁRIO DE CADASTRO", 
                               font=("Arial", 16, "bold"), fg="#2c3e50")
        title_label.pack(pady=20)
        
        # Frame principal
        main_frame = tk.Frame(root, padx=40, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Campos do formulário
        self.campos = {}
        
        # Nome
        self.criar_campo(main_frame, "Nome Completo:", "nome", 0)
        
        # CPF
        self.criar_campo(main_frame, "CPF:", "cpf", 1)
        
        # Data de Nascimento
        self.criar_campo(main_frame, "Data Nascimento (DD/MM/AAAA):", "data_nasc", 2)
        
        # Endereço
        self.criar_campo(main_frame, "Endereço:", "endereco", 3)
        
        # Telefone
        self.criar_campo(main_frame, "Telefone:", "telefone", 4)
        
        # Email
        self.criar_campo(main_frame, "E-mail:", "email", 5)
        
        # Observações
        tk.Label(main_frame, text="Observações:", font=("Arial", 10)).grid(
            row=6, column=0, sticky="w", pady=(10, 5)
        )
        self.observacoes = tk.Text(main_frame, height=4, width=40, font=("Arial", 10))
        self.observacoes.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # Botões
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=8, column=0, columnspan=2, pady=20)
        
        self.btn_limpar = tk.Button(btn_frame, text="Limpar", command=self.limpar_formulario,
                                   bg="#95a5a6", fg="white", font=("Arial", 10, "bold"),
                                   padx=20, pady=5)
        self.btn_limpar.pack(side="left", padx=10)
        
        self.btn_salvar = tk.Button(btn_frame, text="Salvar", command=self.salvar_dados,
                                   bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
                                   padx=20, pady=5)
        self.btn_salvar.pack(side="left", padx=10)
        
        self.btn_carregar = tk.Button(btn_frame, text="Carregar", command=self.carregar_dados,
                                     bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                                     padx=20, pady=5)
        self.btn_carregar.pack(side="left", padx=10)
        
        # Status
        self.status_label = tk.Label(root, text="Aguardando preenchimento...", 
                                    fg="#7f8c8d", font=("Arial", 9))
        self.status_label.pack(pady=10)
        
        # Variável para contar preenchimentos
        self.contador_preenchimentos = 0
        
    def criar_campo(self, parent, label_text, campo_id, row):
        """Cria um campo do formulário"""
        tk.Label(parent, text=label_text, font=("Arial", 10)).grid(
            row=row, column=0, sticky="w", pady=5
        )
        
        entry = tk.Entry(parent, font=("Arial", 10), width=40)
        entry.grid(row=row, column=1, sticky="w", pady=5, padx=(10, 0))
        
        self.campos[campo_id] = entry
        
    def limpar_formulario(self):
        """Limpa todos os campos"""
        for entry in self.campos.values():
            entry.delete(0, tk.END)
        self.observacoes.delete(1.0, tk.END)
        self.status_label.config(text="Formulário limpo", fg="#e74c3c")
        
    def salvar_dados(self):
        """Salva os dados em um arquivo JSON"""
        dados = {}
        for campo_id, entry in self.campos.items():
            dados[campo_id] = entry.get()
        dados['observacoes'] = self.observacoes.get(1.0, tk.END).strip()
        
        # Salvar em arquivo
        with open('dados_salvos.json', 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
            
        self.status_label.config(text="Dados salvos com sucesso!", fg="#2ecc71")
        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
        
    def carregar_dados(self):
        """Carrega dados de um arquivo JSON"""
        try:
            with open('dados_salvos.json', 'r', encoding='utf-8') as f:
                dados = json.load(f)
                
            for campo_id, valor in dados.items():
                if campo_id == 'observacoes':
                    self.observacoes.delete(1.0, tk.END)
                    self.observacoes.insert(1.0, valor)
                elif campo_id in self.campos:
                    self.campos[campo_id].delete(0, tk.END)
                    self.campos[campo_id].insert(0, valor)
                    
            self.status_label.config(text="Dados carregados!", fg="#3498db")
            
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo não encontrado!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar: {e}")
    
    def preencher_automaticamente(self, dados):
        """Método para ser chamado pelo Programa X"""
        try:
            for campo_id, valor in dados.items():
                if campo_id in self.campos:
                    entry = self.campos[campo_id]
                    entry.delete(0, tk.END)
                    entry.insert(0, valor)
                elif campo_id == 'observacoes':
                    self.observacoes.delete(1.0, tk.END)
                    self.observacoes.insert(1.0, valor)
            
            self.contador_preenchimentos += 1
            self.status_label.config(
                text=f"✅ Preenchido automaticamente! ({self.contador_preenchimentos})",
                fg="#27ae60"
            )
            return True
        except Exception as e:
            self.status_label.config(text=f"❌ Erro: {str(e)}", fg="#e74c3c")
            return False

def main():
    root = tk.Tk()
    app = FormularioProgramaY(root)
    root.mainloop()

if __name__ == "__main__":
    main()