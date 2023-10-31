import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
from datetime import datetime
import tkinter.font as font

ventana = tk.Tk()
ventana.title("Editor de Texto")

block_de_texto = scrolledtext.ScrolledText(ventana, wrap="word")
block_de_texto.pack(fill="both", expand=False)

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
            status_label.config(text=f"File saved: {file_path}")
        except Exception as e:
            status_label.config(text=f"Error saving file: {str(e)}")
        actualizar_barra_estado()

menu_archivo.add_command(label="Abrir", command=abrir_archivo)
menu_archivo.add_command(label="Guardar", command=guardar_archivo)
menu_archivo.add_command(label="Salir", command=ventana.destroy)

menu_edicion = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Edición", menu=menu_edicion)

status_label = tk.Label(ventana, text="", padx=20, pady=10)
status_label.pack()

def cortar_texto():
    block_de_texto.event_generate("<<Cut>>")

def copiar_texto():
    block_de_texto.event_generate("<<Copy>>")

def pegar_texto():
    block_de_texto.event_generate("<<Paste>>")

def seleccionar_todo():
    block_de_texto.tag_add("sel", "1.0", "end")

def deshacer():
    block_de_texto.edit_undo()

def rehacer():
    block_de_texto.edit_redo()

menu_edicion.add_command(label="Cortar", command=cortar_texto)
menu_edicion.add_command(label="Copiar", command=copiar_texto)
menu_edicion.add_command(label="Pegar", command=pegar_texto)
menu_edicion.add_command(label="Seleccionar Todo", command=seleccionar_todo)
menu_edicion.add_command(label="Deshacer", command=deshacer)
menu_edicion.add_command(label="Rehacer", command=rehacer)


menu_formato = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Formato", menu=menu_formato)



fuentes_comunes = ["Arial", "Times New Roman", "Courier New", "Verdana", "Tahoma", "Georgia", "Comic Sans MS", "Trebuchet MS", "Lucida Console", "Impact"]
fuente_seleccionada = tk.StringVar(value=fuentes_comunes[0])

tamaño_fuente_actual = 12 # Selector de tamaño de fuente Tamaño de fuente inicial
def cambiar_tamaño_fuente(numero,tamaño_fuente_actual):
    tamaño_editado=tamaño_fuente_actual+numero
    Desired_font = font.Font( size = tamaño_editado) 
    block_de_texto.configure(font = Desired_font)

def cambiar_fuente():
    pass 

menu_formato.add_cascade(label="Fuente", menu=ttk.OptionMenu(menu_formato, fuente_seleccionada, *fuentes_comunes, command=cambiar_fuente))


menu_formato.add_command(label="Aumentar Tamaño de Fuente", command=lambda: cambiar_tamaño_fuente)
menu_formato.add_command(label="Disminuir Tamaño de Fuente", command=lambda: cambiar_tamaño_fuente)


barra_estado = ttk.Label(ventana, text="")#Crea una barra de estado con el tiempo y datos del texto
barra_estado.pack(side="bottom", fill="x")

def actualizar_barra_estado():
    cantidad_caracteres = len(block_de_texto.get("1.0", "end-1c"))
    info_fuente = block_de_texto.cget("font").split()
    tamaño_fuente = info_fuente[0]
    nombre_fuente = info_fuente[1] if len(info_fuente) > 1 else "N/A"
    hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    texto_estado = f"Caracteres: {cantidad_caracteres} | Tamaño de Fuente: {tamaño_fuente} | Fuente: {nombre_fuente} | Hora: {hora_actual}"
    barra_estado.config(text=texto_estado)
    ventana.after(20, actualizar_barra_estado)

actualizar_barra_estado()

ventana.mainloop()
