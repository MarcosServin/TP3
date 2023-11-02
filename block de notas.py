import tkinter as tk
from tkinter import ttk
from tkinter import Text
import tkinter.font as tkFont
from tkinter import filedialog
from datetime import datetime

ventana = tk.Tk()
ventana.title("Editor de Texto")

fuente_modificada = tkFont.Font(family="Verdana", size=10)
fuente_original = tkFont.nametofont("TkDefaultFont")

frame_de_texto = tk.Frame(ventana)
frame_de_texto.grid(row=0, column=0, sticky="nsew")
ventana.columnconfigure(0, weight=1)
ventana.rowconfigure(0, weight=1)

block_de_texto = tk.Text(frame_de_texto, wrap='word', undo=True, autoseparators=True, font=fuente_modificada)
block_de_texto.grid(row=0, column=0, sticky="nsew")
frame_de_texto.columnconfigure(0, weight=1)
frame_de_texto.rowconfigure(0, weight=1)

barra_navegacion_y = tk.Scrollbar(frame_de_texto, command=block_de_texto.yview)
barra_navegacion_y.grid(row=0, column=1, sticky="ns")

block_de_texto.config(yscrollcommand=barra_navegacion_y.set)


barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)
menu_archivo = tk.Menu(barra_menu, tearoff=0)

barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

def abrir_archivo():
    archivo = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if archivo:
        with open(archivo, "r") as archivo_abierto:
            block_de_texto.delete(1.0, "end")
            block_de_texto.insert("insert", archivo_abierto.read())
        actualizar_barra_estado()


def guardar_archivo():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'w') as file:
                text_content = block_de_texto.get("1.0", "end-1c")
                file.write(text_content)
            mensaje_de_pantalla.config(text=f"File saved: {file_path}")
        except Exception as e:
            mensaje_de_pantalla.config(text=f"Error saving file: {str(e)}")
        actualizar_barra_estado()

menu_archivo.add_command(label="Abrir", command=abrir_archivo)
menu_archivo.add_command(label="Guardar", command=guardar_archivo)
menu_archivo.add_command(label="Salir", command=ventana.destroy)

menu_edicion = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Edición", menu=menu_edicion)

mensaje_de_pantalla = tk.Label(ventana, text="", padx=20, pady=10)
mensaje_de_pantalla.grid(row=1, column=0, sticky="ew")


def cortar_texto():
    block_de_texto.event_generate("<<Cut>>")

def copiar_texto():
    block_de_texto.event_generate("<<Copy>>")

def pegar_texto():
    block_de_texto.event_generate("<<Paste>>")

def seleccionar_todo():
    block_de_texto.tag_add("sel", "1.0", "end")

def deshacer():
    block_de_texto.event_generate("<<Undo>>")

def rehacer():
    block_de_texto.event_generate("<<Redo>>")

menu_edicion.add_command(label="Cortar", command=cortar_texto)
menu_edicion.add_command(label="Copiar", command=copiar_texto)
menu_edicion.add_command(label="Pegar", command=pegar_texto)
menu_edicion.add_command(label="Seleccionar Todo", command=seleccionar_todo)
menu_edicion.add_command(label="Deshacer", command=deshacer)
menu_edicion.add_command(label="Rehacer", command=rehacer)


menu_formato = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Formato", menu=menu_formato)


def cambiar_tamaño_fuente(numero):
    tamaño_actual = fuente_modificada.actual("size")
    if tamaño_actual > 9:
        tamaño_actual += numero
        fuente_modificada.configure(size=tamaño_actual)
        block_de_texto.configure(font=fuente_modificada)
    # print(tamaño_actual)

def buscar_fuentes_locales():#busca fuentes en el sistema y las muestra como opciones
    fuente_familia = tkFont.families()
    lista_familia_eleccion=[]
    for f in fuente_familia:
        # print(f)
        lista_familia_eleccion.append(f)
    return lista_familia_eleccion

opciones_de_fuentes=buscar_fuentes_locales()

def cambiar_fuente(familia):
    fuente_modificada.configure(family=familia)
    block_de_texto.configure(font=fuente_modificada)

menu_formato.add_command(label="Arial", command=lambda: cambiar_fuente("Arial"))
menu_formato.add_command(label="Times New Roman", command=lambda: cambiar_fuente("Times New Roman"))
menu_formato.add_command(label="Courier New", command=lambda: cambiar_fuente('Courier New'))
menu_formato.add_command(label="Verdana", command=lambda: cambiar_fuente('Verdana'))
menu_formato.add_command(label="calibri", command=lambda: cambiar_fuente('calibri'))

menu_formato.add_command(label="Aumentar Tamaño de Fuente", command=lambda: cambiar_tamaño_fuente(2))
menu_formato.add_command(label="Disminuir Tamaño de Fuente", command=lambda: cambiar_tamaño_fuente(-2))

def cambiar_tema_claro():
    block_de_texto.configure(bg="#fffbfd",fg="#262626")
def cambiar_tema_oscuro():
    block_de_texto.configure(bg="#262626",fg="#fffbfd")

menu_tema = tk.Menu(barra_menu,tearoff=0)
barra_menu.add_cascade(label="Tema",menu=menu_tema)
menu_tema.add_command(label="Claro",command=lambda:cambiar_tema_claro())
menu_tema.add_command(label="Oscuro",command=lambda:cambiar_tema_oscuro())

barra_estado = ttk.Label(ventana, text="")
barra_estado.grid(row=1, column=0)
barra_estado.config(font=("Arial", 10))

def actualizar_barra_estado():
    cantidad_caracteres = len(block_de_texto.get("1.0", "end-1c"))
    tamaño_fuente = fuente_modificada.actual("size")
    nombre_fuente = fuente_modificada.actual("family")
    hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    texto_estado = f"Caracteres: {cantidad_caracteres} | Tamaño de Fuente: {tamaño_fuente} | Fuente: {nombre_fuente} | Hora: {hora_actual}"
    barra_estado.config(text=texto_estado)
    ventana.after(20, actualizar_barra_estado)

actualizar_barra_estado()

ventana.mainloop()

