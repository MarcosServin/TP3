import tkinter as tk
from tkinter import ttk
from tkinter import Text
import tkinter.font as tkFont
from tkinter import filedialog
from datetime import datetime
import csv

ventana = tk.Tk()
ventana.title("Editor de Texto")

fuente_modificada = tkFont.Font(family="Verdana", size=12)
fuente_original = tkFont.nametofont("TkDefaultFont")

def cambiar_logo():
    try:
        icon_image = tk.PhotoImage(file="cfl_logo.png")  # Replace "cfl-logo.png" with your image file name
        ventana.iconphoto(False, icon_image)
    except:
        pass
cambiar_logo()

def remplazar_dato_de_columna(index_columna, nueva_data):
    ruta_archivo="opciones.csv"
    try:
        with open(ruta_archivo, 'r', newline='') as file:
            rows = list(csv.reader(file))
        
        for row in rows:
            if 0 <=index_columna < len(row):
                row[index_columna] = nueva_data
        
        with open(ruta_archivo, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        
        return True  # Successful update
    except Exception as e:
        print(f"Error: {e}")
        return False  # Update failed

fuente_modificada = tkFont.Font(family="Verdana", size=12)
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
    ruta_archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if ruta_archivo:
        try:
            with open(ruta_archivo, 'w') as file:
                text_content = block_de_texto.get("1.0", "end-1c")
                file.write(text_content)
            mensaje_de_pantalla.config(text=f"File saved: {ruta_archivo}")
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
        remplazar_dato_de_columna(1,tamaño_actual)

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
    remplazar_dato_de_columna(0,familia)

menu_formato.add_command(label="Arial", command=lambda: cambiar_fuente("Arial"))
menu_formato.add_command(label="Times New Roman", command=lambda: cambiar_fuente("Times New Roman"))
menu_formato.add_command(label="Courier New", command=lambda: cambiar_fuente('Courier New'))
menu_formato.add_command(label="Verdana", command=lambda: cambiar_fuente('Verdana'))
menu_formato.add_command(label="Calibri", command=lambda: cambiar_fuente('Calibri'))
menu_formato.add_command(label="Helvetica", command=lambda: cambiar_fuente('Helvetica'))
menu_formato.add_command(label="Georgia", command=lambda: cambiar_fuente('Georgia'))
menu_formato.add_command(label="Comic Sans MS", command=lambda: cambiar_fuente('Comic Sans MS'))
menu_formato.add_command(label="Tahoma", command=lambda: cambiar_fuente('Tahoma'))
menu_formato.add_command(label="Trebuchet MS", command=lambda: cambiar_fuente('Trebuchet MS'))


menu_tamaño = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Tamaño", menu=menu_tamaño)
menu_tamaño.add_command(label="Aumentar Tamaño de Fuente", command=lambda: cambiar_tamaño_fuente(2))
menu_tamaño.add_command(label="Disminuir Tamaño de Fuente", command=lambda: cambiar_tamaño_fuente(-2))

def cambiar_tema(tema_color):
    if tema_color=="claro":
        cambiar_tema_claro()
    if tema_color=="oscuro":
        cambiar_tema_oscuro()
    if tema_color=="verde":
        cambiar_tema_verde()
    remplazar_dato_de_columna(2,tema_color)
    

def cambiar_tema_claro():
    block_de_texto.configure(bg="#fffbfd", fg="#262626")
    barra_estado.configure(bg="#fffbfd", fg="#262626")
    menu_formato.configure(bg="#fffbfd", fg="#262626")
    menu_tema.configure(bg="#fffbfd", fg="#262626")
    menu_archivo.configure(bg="#fffbfd", fg="#262626")
    menu_edicion.configure(bg="#fffbfd", fg="#262626")

def cambiar_tema_oscuro():
    block_de_texto.configure(bg="#262626", fg="#fffbfd")
    barra_estado.configure(bg="#262626", fg="#fffbfd")
    menu_formato.configure(bg="#262626", fg="#fffbfd")
    menu_tema.configure(bg="#262626", fg="#fffbfd")
    menu_archivo.configure(bg="#262626", fg="#fffbfd")
    menu_edicion.configure(bg="#262626", fg="#fffbfd")

def cambiar_tema_verde():
    block_de_texto.configure(bg="#e6ffe6", fg="#216421")
    barra_estado.configure(bg="#b4ffb4", fg="#316431")
    menu_formato.configure(bg="#b4ffb4", fg="#316431")
    menu_tamaño.configure(bg="#b4ffb4", fg="#316431")
    menu_tema.configure(bg="#b4ffb4", fg="#316431")
    menu_archivo.configure(bg="#b4ffb4", fg="#316431")
    menu_edicion.configure(bg="#b4ffb4", fg="#316431")

menu_tema = tk.Menu(barra_menu,tearoff=0)
barra_menu.add_cascade(label="Tema",menu=menu_tema)
menu_tema.add_command(label="Claro",command=lambda:cambiar_tema("claro"))
menu_tema.add_command(label="Oscuro",command=lambda:cambiar_tema("oscuro"))
menu_tema.add_command(label="CFL",command=lambda:cambiar_tema("verde"))


barra_estado = tk.Label(ventana, text="", padx=20, pady=10)
barra_estado.grid(row=1, column=0, sticky="ew")
barra_estado.config(font=("Arial", 10))

def actualizar_barra_estado():
    cantidad_caracteres = len(block_de_texto.get("1.0", "end-1c"))
    tamaño_fuente = fuente_modificada.actual("size")
    nombre_fuente = fuente_modificada.actual("family")
    hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    texto_estado = f"Caracteres: {cantidad_caracteres} | Tamaño de Fuente: {tamaño_fuente} | Fuente: {nombre_fuente} | Hora: {hora_actual}"
    barra_estado.config(text=texto_estado)
    ventana.after(20, actualizar_barra_estado)


def leer_configuracion():
    config_file = "opciones.csv"
    fuente=""
    tamaño=12
    tema="claro"
    archivo_configuracion = {
        "fuente": "Arial",
        "tamaño": "12",
        "tema": "claro"
                        }
    try:
        with open(config_file, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 3:
                    font_family, font_size, theme = row
            fuente=font_family
            tamaño=int(font_size)
            tema=theme
            fuente_modificada.configure(size=tamaño,family=fuente)
            block_de_texto.configure(font=fuente_modificada)
        cambiar_tema(tema)                                    

        
    except FileNotFoundError:
        # Create the configuration file with default values if it doesn't exist
        with open(config_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([archivo_configuracion["fuente"], archivo_configuracion["tamaño"], archivo_configuracion["tema"]])
leer_configuracion()

def remplazar_dato_de_columna(index_columna, nueva_data):
    ruta_archivo="opciones.csv"
    try:
        with open(ruta_archivo, 'r', newline='') as file:
            rows = list(csv.reader(file))
        
        for row in rows:
            if 0 <=index_columna < len(row):
                row[index_columna] = nueva_data
        
        with open(ruta_archivo, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        
        return True  # Successful update
    except Exception as e:
        print(f"Error: {e}")
        return False  # Update failed

actualizar_barra_estado()

ventana.mainloop()

