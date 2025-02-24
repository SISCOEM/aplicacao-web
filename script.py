import subprocess
import tkinter as tk
from tkinter import messagebox
import os


def activate_and_execute():
    # Caminho do ambiente virtual e do projeto
    venv_activate = os.path.join(os.getcwd(), 'venv', 'Scripts', 'activate.bat')
    project_path = os.path.join(os.getcwd(), 'sicomb')

    try:
        # Comando único com encadeamento
        command = f'cmd /k "{venv_activate} && cd {project_path} && python manage.py runserver"'
        subprocess.run(command, shell=True)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao executar os comandos: {e}")


def on_run():
    # Confirmação antes de executar
    if messagebox.askyesno("Confirmação", "Deseja ativar o ambiente virtual e rodar o servidor Django?"):
        activate_and_execute()


# Criação da janela principal
root = tk.Tk()
root.title("Gerenciador de Ambiente Virtual")
root.geometry("400x200")

# Elementos da interface
label = tk.Label(root, text="Clique no botão para executar os comandos:", font=("Arial", 12))
label.pack(pady=20)

btn_run = tk.Button(root, text="Ativar e Executar", command=on_run, font=("Arial", 12), bg="green", fg="white")
btn_run.pack(pady=10)

btn_exit = tk.Button(root, text="Sair", command=root.quit, font=("Arial", 12), bg="red", fg="white")
btn_exit.pack(pady=10)

# Loop principal da GUI
root.mainloop()
