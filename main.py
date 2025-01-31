import random
import string
import tkinter as tk
from tkinter import messagebox

def generate_password(length):
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_characters = "@#$%&"
    
    # Garante pelo menos um caractere de cada tipo em ordem aleatória
    types = ['lower', 'upper', 'digit', 'special']
    random.shuffle(types)
    password = []
    for t in types:
        if t == 'lower':
            password.append(random.choice(lowercase))
        elif t == 'upper':
            password.append(random.choice(uppercase))
        elif t == 'digit':
            password.append(random.choice(digits))
        elif t == 'special':
            password.append(random.choice(special_characters))

    # Função para determinar o tipo do caractere
    def get_type(char):
        if char in lowercase: return 'lower'
        if char in uppercase: return 'upper'
        if char in digits: return 'digit'
        if char in special_characters: return 'special'
        return None

    # Adiciona caracteres restantes evitando tipos consecutivos iguais
    while len(password) < length:
        last_type = get_type(password[-1])
        available_types = ['lower', 'upper', 'digit', 'special']
        available_types.remove(last_type)
        selected_type = random.choice(available_types)
        
        if selected_type == 'lower':
            new_char = random.choice(lowercase)
        elif selected_type == 'upper':
            new_char = random.choice(uppercase)
        elif selected_type == 'digit':
            new_char = random.choice(digits)
        else:
            new_char = random.choice(special_characters)
            
        password.append(new_char)

    return ''.join(password)

def on_generate():
    try:
        length = int(length_spinbox.get())
        if length < 4:
            messagebox.showerror("Erro", "O comprimento mínimo é 4!")
            return
        password = generate_password(length)
        result_var.set(password)
    except ValueError:
        messagebox.showerror("Erro", "Digite um número válido!")

def copy_to_clipboard():
    password = result_var.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copiado", "Senha copiada para área de transferência!")
    else:
        messagebox.showerror("Erro", "Nenhuma senha para copiar!")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Gerador de Senhas Seguras")
root.configure(bg="#2D2D2D")
root.resizable(False, False)

# Estilos e cores
main_frame = tk.Frame(root, bg="#2D2D2D", padx=20, pady=20)
main_frame.pack()

tk.Label(main_frame, text="Gerador de Senhas", font=("Arial", 20, "bold"),
         bg="#2D2D2D", fg="#00FF00").grid(row=0, column=0, columnspan=3, pady=10)

tk.Label(main_frame, text="Comprimento:", bg="#2D2D2D", fg="white",
         font=("Arial", 12)).grid(row=1, column=0, pady=5, sticky="e")

length_spinbox = tk.Spinbox(main_frame, from_=4, to=50, width=5,
                            font=("Arial", 12), justify="center")
length_spinbox.grid(row=1, column=1, pady=5, padx=5)

generate_btn = tk.Button(main_frame, text="Gerar Senha", command=on_generate,
                         bg="#006600", fg="white", font=("Arial", 12, "bold"),
                         activebackground="#009900", activeforeground="white")
generate_btn.grid(row=1, column=2, pady=5, padx=5)

result_var = tk.StringVar()
result_entry = tk.Entry(main_frame, textvariable=result_var, font=("Courier", 14),
                        bg="#1C1C1C", fg="#00FF00", width=25, borderwidth=2,
                        relief="flat", justify="center")
result_entry.grid(row=2, column=0, columnspan=2, pady=15, padx=5)

copy_btn = tk.Button(main_frame, text="Copiar", command=copy_to_clipboard,
                     bg="#1E90FF", fg="white", font=("Arial", 12, "bold"),
                     activebackground="#4169E1", activeforeground="white")
copy_btn.grid(row=2, column=2, pady=5, padx=5)

tk.Button(main_frame, text="Sair", command=root.destroy, bg="#8B0000",
          fg="white", font=("Arial", 12, "bold"), activebackground="#FF0000",
          activeforeground="white").grid(row=3, column=0, columnspan=3, pady=10)

root.mainloop()