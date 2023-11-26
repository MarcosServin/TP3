import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog
from datetime import datetime
import csv
from gtts import gTTS
from playsound import playsound
import os 

ventana = tk.Tk()
ventana.title("Editor de Texto")

# lector = pyttsx3.init()

def cambiar_logo():#intenta cargar cfl_logo y usarlo como icono
    try:
        icon_image = tk.PhotoImage(file="cfl_logo.png")
        ventana.iconphoto(False, icon_image)
    except:
        pass
cambiar_logo()

#intenta abrir el archivo de opciones y cambia el valor(nueva_data) en la columna (index_columna)
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
        
        return True
    except:
        leer_configuracion()

#crea una fuente nueva para poder modificarla con las opciones
fuente_modificada = tkFont.Font(family="Verdana", size=14)
#guarda la fuente original para ser usada por los widgets
fuente_original = tkFont.nametofont("TkDefaultFont")

#crea el frame en donde el widget de texto se va a pegar
frame_de_texto = tk.Frame(ventana)
frame_de_texto.grid(row=0, column=0, sticky="nsew")
ventana.columnconfigure(0, weight=1)
ventana.rowconfigure(0, weight=1)

#crea el widget de texto con la fuente modifcada arriba
block_de_texto = tk.Text(frame_de_texto, wrap='word', undo=True, autoseparators=True, font=fuente_modificada)
block_de_texto.grid(row=0, column=0, sticky="nsew")

frame_de_texto.columnconfigure(0, weight=1)
frame_de_texto.rowconfigure(0, weight=1)
frame_de_texto.grid_propagate(False)

#crea la barra de scroll vertical
barra_navegacion_y = tk.Scrollbar(frame_de_texto, command=block_de_texto.yview)
barra_navegacion_y.grid(row=0, column=1, sticky="ns")

#asigna la barra al widget de texto
block_de_texto.config(yscrollcommand=barra_navegacion_y.set)

#crea la barra de menu
barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

#agrega el menu de archivo a la barra 
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
            mensaje_de_pantalla.config(text=f"Archivo guardado: {ruta_archivo}")
        except Exception as e:
            mensaje_de_pantalla.config(text=f"Error: {str(e)}")
        actualizar_barra_estado()

#mensaje de error por si no se puede guardar
mensaje_de_pantalla = tk.Label(ventana, text="", padx=20, pady=10)
mensaje_de_pantalla.grid(row=1, column=0, sticky="ew")

#opciones que aparecen en el menu archivo
def crear_opciones_de_archivo():
    try:
        menu_archivo.add_command(label="Abrir", command=abrir_archivo)
        menu_archivo.add_command(label="Guardar", command=guardar_archivo)
        menu_archivo.add_command(label="Salir", command=ventana.destroy)
    except Exception as e:
        mensaje_de_pantalla.config(text=f"Error: {str(e)}")
crear_opciones_de_archivo()
#crea un nuevo menu para la edicion de texto
menu_edicion = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Edición", menu=menu_edicion)



#block de eventos para editar textos
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

#opciones del menu edicion
def crear_comandos_de_edicion():
    try:
        menu_edicion.add_command(label="Cortar", command=cortar_texto)
        menu_edicion.add_command(label="Copiar", command=copiar_texto)
        menu_edicion.add_command(label="Pegar", command=pegar_texto)
        menu_edicion.add_command(label="Seleccionar Todo", command=seleccionar_todo)
        menu_edicion.add_command(label="Deshacer", command=deshacer)
        menu_edicion.add_command(label="Rehacer", command=rehacer)
    except Exception as e:
        mensaje_de_pantalla.config(text=f"Error: {str(e)}")
crear_comandos_de_edicion()

#configura la fuente modificada para que use la familia ingresada,despues cambia la fuente de el widget de texto por la fuente que se modificó
def cambiar_fuente(familia):
    try:
        fuente_modificada.configure(family=familia)
        block_de_texto.configure(font=fuente_modificada)
        actualizar_configuracion(0,familia)
    except Exception as a:
        print(f"Error:{a}")
#crea el menu formato
def buscar_fuentes_locales():#busca fuentes en el sistema y las muestra como opciones
    try:
        fuente_familia = tkFont.families()
        lista_familia_eleccion=[]
        for f in fuente_familia:
            lista_familia_eleccion.append(f)
        lista_familia_eleccion=sorted(lista_familia_eleccion)
        return lista_familia_eleccion
    except Exception as e:
        mensaje_de_pantalla.config(text=f"Error: {str(e)}")

lista_fuentes = buscar_fuentes_locales()

def obtener_index(lista):
    abc=0
    try:
        abc=lista.curselection()
        abc=list(abc)
        if abc==False: 
            abc=0
        else :
            abc=abc[0]
    except Exception as a:
        print(a)
        abc=0
    cambiar_fuente(lista_fuentes[abc])
#crea una nueva ventana cuando se intente cambiar de fuente
def ventana_de_fuentes():
    fondo,letras=block_de_texto.cget("background"),block_de_texto.cget('foreground')
    window = tk.Toplevel()    
    try:
        icon_image = tk.PhotoImage(file="cfl_logo.png")
        window.iconphoto(False, icon_image)
    except:
        pass
    window.geometry('200x400')
    frame = tk.Frame(window)
    frame.grid(row=0, column=0, sticky="nsew")
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    listabox = tk.Listbox(frame,height=100,width=150)
    listabox.config(fg=letras,bg=fondo)
    listabox.grid(row=0,column=0,sticky="nw")
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)
    frame_de_texto.grid_propagate(False)
    barra_navegacion_y = tk.Scrollbar(window, command=listabox.yview)
    barra_navegacion_y.grid(row=0, column=1, sticky="ns")
    listabox.config(yscrollcommand=barra_navegacion_y.set)
    for e in range(len(lista_fuentes)):
        listabox.insert(e,lista_fuentes[e])
    boton_seleccion=tk.Button(window,text='Cambiar fuente',fg=letras,bg=fondo,command=lambda:obtener_index(listabox))
    boton_seleccion.grid(row=1,column=0,sticky="we")

barra_menu.add_command(label="Cambiar fuente", command=ventana_de_fuentes)

def cambiar_tamaño_fuente(numero):#aumenta o disminuye el tamaño de la fuente por 2
    try:
        tamaño_actual = fuente_modificada.actual("size")
        if (tamaño_actual+numero>=10) or (numero>1):
            tamaño_actual += numero
            fuente_modificada.configure(size=tamaño_actual)
            block_de_texto.configure(font=fuente_modificada)
            actualizar_configuracion(1,tamaño_actual)
    except Exception as e:
            mensaje_de_pantalla.config(text=f"Error: {str(e)}")

barra_menu.add_command(label="A ↑", command=lambda: cambiar_tamaño_fuente(2))
barra_menu.add_command(label="a ↓", command=lambda: cambiar_tamaño_fuente(-2))

def lector_de_texto():
    try:
        abs_path = os.path.abspath("audio.mp3")
        os.remove(abs_path)
    except OSError as e:
        print(f"Error: {e.strerror}")
    texto = block_de_texto.get("1.0", "end-1c")
    if len(texto)==0:
        texto="Sin texto"
    audio = 'audio.mp3'
    language = 'es'
    acento = 'com.mx'
    texto = texto
    try:
        sp = gTTS(text=texto, lang=language, tld=acento, slow=False)
        sp.save(audio)
        playsound(audio)
    except Exception as e:
        mensaje_de_pantalla.config(text=f"Error: {str(e)}")

menu_audio=tk.Menu(barra_menu,tearoff=0)
barra_menu.add_cascade(label="Audio", menu=menu_audio)
menu_audio.add_command(label="Lector de texto",command=lector_de_texto)

def cambiar_tema(tema_color):#Corre una función distinta para cada tema
    try:
        if tema_color=="claro":
            cambiar_tema_claro()
        elif tema_color=="oscuro":
            cambiar_tema_oscuro()
        elif tema_color=="verde":
            cambiar_tema_verde()
        elif tema_color=="negro":
            cambiar_tema_negro()
        actualizar_configuracion(2,tema_color)#Actualiza el archivo de configuraciónes con el tema elegído
    except Exception as e:
        mensaje_de_pantalla.config(text=f"Error: {str(e)}")
#cambia el color de fondo,caracteres,cursor de texto,fondo seleccionado,caracter seleccionado
def cambiar_tema_claro():
    try:
        block_de_texto.configure(bg="#fffbfd", fg="#262626",insertbackground="black",selectbackground="grey",selectforeground="#fffbfd")
        barra_estado.configure(bg="#fffbfd", fg="#262626")
        # menu_formato.configure(bg="#fffbfd", fg="#262626")
        menu_tema.configure(bg="#fffbfd", fg="#262626")
        menu_archivo.configure(bg="#fffbfd", fg="#262626")
        menu_archivo.configure(bg="#fffbfd", fg="#262626")
        menu_audio.configure(bg="#fffbfd", fg="#262626")
    except Exception as e:
        mensaje_de_pantalla.config(text=f"Error: {str(e)}")

def cambiar_tema_oscuro():
    try:
        block_de_texto.configure(bg="#262626", fg="#fffbfd",insertbackground="grey",selectbackground="grey")
        barra_estado.configure(bg="#262626", fg="#fffbfd")
        # menu_formato.configure(bg="#262626", fg="#fffbfd")
        menu_tema.configure(bg="#262626", fg="#fffbfd")
        menu_archivo.configure(bg="#262626", fg="#fffbfd")
        menu_edicion.configure(bg="#262626", fg="#fffbfd")
        menu_audio.configure(bg="#262626", fg="#fffbfd")
    except Exception as e:
        mensaje_de_pantalla.config(text=f"Error: {str(e)}")

def cambiar_tema_negro():
    try:
        block_de_texto.configure(bg="black", fg="#fffbfd",insertbackground="grey",selectbackground="grey")
        barra_estado.configure(bg="black", fg="#fffbfd")
        # menu_formato.configure(bg="black", fg="#fffbfd")
        menu_tema.configure(bg="black", fg="#fffbfd")
        menu_archivo.configure(bg="black", fg="#fffbfd")
        menu_edicion.configure(bg="black", fg="#fffbfd")
        menu_audio.configure(bg="black", fg="#fffbfd")
    except Exception as e:
        mensaje_de_pantalla.config(text=f"Error: {str(e)}")

def cambiar_tema_verde():
    try:
        block_de_texto.configure(bg="#e6ffe6", fg="#216421",insertbackground="green",selectbackground="#216421",selectforeground="#e6ffe6")
        barra_estado.configure(bg="#b4ffb4", fg="#316431")
        # menu_formato.configure(bg="#b4ffb4", fg="#316431")
        menu_tema.configure(bg="#b4ffb4", fg="#316431")
        menu_archivo.configure(bg="#b4ffb4", fg="#316431")
        menu_edicion.configure(bg="#b4ffb4", fg="#316431")
        menu_audio.configure(bg="#b4ffb4", fg="#316431")
    except Exception as e:
        mensaje_de_pantalla.config(text=f"Error: {str(e)}")
#crea el menu tema con un boton para cada tema
menu_tema = tk.Menu(barra_menu,tearoff=0)
barra_menu.add_cascade(label="Tema",menu=menu_tema)
menu_tema.add_command(label="Claro",command=lambda:cambiar_tema("claro"))
menu_tema.add_command(label="Oscuro",command=lambda:cambiar_tema("oscuro"))
menu_tema.add_command(label="CFL",command=lambda:cambiar_tema("verde"))
menu_tema.add_command(label="Negro",command=lambda:cambiar_tema("negro"))

#crea una barra en la parte mas baja de la ventana
barra_estado = tk.Label(ventana, text="", padx=20, pady=10)
barra_estado.grid(row=1, column=0, sticky="ew")
barra_estado.config(font=("Arial", 10))

#cada 500 milisegundos la barra de estado se actualiza con datos del texto,fuente u hora
def actualizar_barra_estado():
    try:
        cantidad_caracteres = len(block_de_texto.get("1.0", "end-1c"))
        tamaño_fuente = fuente_modificada.actual("size")
        nombre_fuente = fuente_modificada.actual("family")
        hora_actual = datetime.now().strftime("%H:%M:%S %d-%m-%Y ")
        texto_estado = f"Caracteres: {cantidad_caracteres} | Tamaño de Fuente: {tamaño_fuente} | Fuente: {nombre_fuente} | Hora: {hora_actual}"
        barra_estado.config(text=texto_estado)
        ventana.after(500, actualizar_barra_estado)
    except Exception as e:
        mensaje_de_pantalla.config(text=f"Error: {str(e)}")
    
#crea abre el menu_edicion en pantalla cuando se usa el boton derecho
def mostrar_menu_contextual(event):
    try:
        menu_edicion.post(event.x_root, event.y_root)
    except Exception as e:
        mensaje_de_pantalla.config(text=f"Error: {str(e)}")
block_de_texto.bind("<Button-3>", mostrar_menu_contextual)

def aumentar(event):
    try:
        cambiar_tamaño_fuente(2)
    except Exception as e:
        mensaje_de_pantalla.config(text=f"Error: {str(e)}")
def disminuir(event):
    try:
        cambiar_tamaño_fuente(-2)
    except Exception as e:
        mensaje_de_pantalla.config(text=f"Error: {str(e)}")
    
block_de_texto.bind("<Control-minus>",disminuir)
block_de_texto.bind("<Control-plus>",aumentar)

#si el archivo opciones existe,carga los datos relacionados a la fuente,si no existe lo crea
def leer_configuracion():
    archivo_de_configuracion = "opciones.csv"
    fuente = "Verdana"
    tamaño = 14
    tema = "claro"
    ancho = 800
    alto = 600
    modo = False
    try:
        with open(archivo_de_configuracion, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 4:
                    r_familia, r_tamaño, r_tema, modo= row
                    fuente = r_familia
                    tamaño = int(r_tamaño)
                    tema = r_tema
                    fuente_modificada.configure(size=tamaño, family=fuente)
                    block_de_texto.configure(font=fuente_modificada)
                    cambiar_tema(tema)
        ventana.geometry(f"{ancho}x{alto}")
    except:
        with open(archivo_de_configuracion, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([fuente, tamaño, tema, modo])
            leer_configuracion()

leer_configuracion()

#cada vez que un dato se cambia en el archivo opciones ,se guarda True si la ventana está maximizada of False si no lo está
def actualizar_configuracion(x,y):
    try:
        modo = (ventana.state() == 'zoomed')
        remplazar_dato_de_columna(x,y)
        remplazar_dato_de_columna(3,modo)
    except Exception as e:
        mensaje_de_pantalla.config(text=f"Error: {str(e)}")

actualizar_barra_estado()
ventana.mainloop()