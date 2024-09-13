import customtkinter as ctk
from random import randint
from PIL import Image, ImageTk
import os 
import sys

# Função para obter o caminho do arquivo (com suporte para PyInstaller)
def resource_path(relative_path):
    """Retorna o caminho absoluto para o recurso, funciona tanto para desenvolvimento quanto para o PyInstaller"""
    try:
        base_path = sys._MEIPASS  # Quando empacotado com PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")  # No desenvolvimento
    return os.path.join(base_path, relative_path)

# Configuração do tema e aparência
ctk.set_appearance_mode("System")  # Modos: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"

# Inicializa a janela principal
root = ctk.CTk()
root.geometry("520x350")
root.title("Gerador de senha")

# Tenta carregar a imagem do ícone
try:
    icon_path = resource_path("senha1.ico")
    if os.path.exists(icon_path):
        icon_image = Image.open(icon_path)
        icon_photo = ImageTk.PhotoImage(icon_image)
        root.iconphoto(False, icon_photo)
    else:
        raise FileNotFoundError(f"Ícone não encontrado no caminho: {icon_path}")
except Exception as e:
    print(f"Não foi possível carregar o ícone: {e}")

# Função para gerar uma nova senha aleatória
def new_rand():
    pw_entry.delete(0, ctk.END)
    pw_length = int(my_entry.get()) if my_entry.get() else 0
    my_password = ''.join(chr(randint(33, 126)) for _ in range(pw_length))
    pw_entry.insert(0, my_password)
    pw_entry.configure(justify='center')

# Função para copiar a senha gerada para a área de transferência
def clipper():
    root.clipboard_clear()
    root.clipboard_append(pw_entry.get())

# Função para limpar os campos de entrada
def clear_entry():
    my_entry.delete(0, ctk.END)
    pw_entry.delete(0, ctk.END)

# Função para validar o comprimento máximo do input
def validate_length(input):
    if input.isdigit() and len(input) <= 2 and int(input) <= 32:
        return True
    elif input == "":
        return True
    else:
        return False

# Define a regra de validação para o Entry
validate_command = root.register(validate_length)

# Cria o Frame para o input do comprimento da senha
lf = ctk.CTkFrame(root)
lf.pack(pady=20)

# Label para o input do comprimento da senha
ctk.CTkLabel(lf, text="Quantos caracteres (Máximo 32)?", font=("Helvetica", 16)).pack(pady=10)

# Entry para o input do comprimento da senha com validação
my_entry = ctk.CTkEntry(lf, font=("Helvetica", 24), validate="key", validatecommand=(validate_command, '%P'), width=80, justify='center')
my_entry.pack(pady=10)

# Entry para exibir a senha gerada
pw_entry = ctk.CTkEntry(root, font=("Helvetica", 24), justify='center', width=500)
pw_entry.pack(pady=20)

# Frame para organizar os botões
my_frame = ctk.CTkFrame(root)
my_frame.pack(pady=20)

# Carrega as imagens para os botões
try:
    create_image_path = resource_path("create.png")
    copy_image_path = resource_path("copy.png")
    clean_image_path = resource_path("clean.png")

    if os.path.exists(create_image_path) and os.path.exists(copy_image_path) and os.path.exists(clean_image_path):
        create_image = ctk.CTkImage(light_image=Image.open(create_image_path), dark_image=Image.open(create_image_path), size=(20, 20))
        copy_image = ctk.CTkImage(light_image=Image.open(copy_image_path), dark_image=Image.open(copy_image_path), size=(20, 20))
        clean_image = ctk.CTkImage(light_image=Image.open(clean_image_path), dark_image=Image.open(clean_image_path), size=(20, 20))
    else:
        raise FileNotFoundError("Uma ou mais imagens não foram encontradas.")
except Exception as e:
    print(f"Não foi possível carregar uma ou mais imagens dos botões: {e}")
    create_image = copy_image = clean_image = None

# Botão para gerar a senha forte (Verde)
my_button = ctk.CTkButton(my_frame, text="Gerar senha forte", command=new_rand, image=create_image, compound="left", font=("Helvetica", 16), fg_color="#4caf50", hover_color="#45a049")
my_button.grid(row=0, column=0, padx=10)

# Botão para copiar a senha gerada
clip_button = ctk.CTkButton(my_frame, text="Copiar", command=clipper, image=copy_image, compound="left", font=("Helvetica", 16))
clip_button.grid(row=0, column=1, padx=10)

# Botão para limpar os campos (Laranja)
clear_button = ctk.CTkButton(my_frame, text="Limpar", command=clear_entry, image=clean_image, compound="left", font=("Helvetica", 16), fg_color="#ff9800", hover_color="#f57c00")
clear_button.grid(row=0, column=2, padx=10)

# Inicia o loop principal da aplicação
root.mainloop()
