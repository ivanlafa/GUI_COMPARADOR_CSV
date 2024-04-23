from tkinter import *
from tkinter import ttk

ventana = Tk()
ventana.title("COMPARADOR FUNCIONAL DE ARCHIVOS CSV")

# Dimensiones de la ventana
ancho_ventana = 800
alto_ventana = 400

# Dimensiones de la pantalla
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

# Posicionamiento de la ventana en el centro de la pantalla
x_pos = (ancho_pantalla / 2) - (ancho_ventana / 2)
y_pos = (alto_pantalla / 2) - (alto_ventana / 2)

ventana.geometry(f'{ancho_ventana}x{alto_ventana}+{int(x_pos)}+{int(y_pos)}')

# Variable para almacenar la fase seleccionada
fase_seleccionada = StringVar()
fase_seleccionada.set(None)  # Ninguna fase seleccionada inicialmente

# Frame para los radiobuttons de fase
frame_fases = Frame(ventana)
frame_fases.place(relx=0.08, rely=0.6, anchor=SW)
frame_fases_label = Label(frame_fases, text="Fases a escoger")
frame_fases_label.pack()

# Radiobuttons para las fases
fases = ["FASE 1", "FASE 2", "FASE 3", "FASE 4"]
for fase in fases:
    radio = Radiobutton(frame_fases, text=fase, variable=fase_seleccionada, value=fase)
    radio.pack(side=LEFT)

# Botón para descargar
boton_descargar = Button(frame_fases, text="Descargar CSV con diferencias")
boton_descargar.pack(pady=5)

# Frame para los archivos enviados y cargados
frame_archivos = Frame(ventana)
frame_archivos.place(relx=0.5, rely=0.85, anchor=S)
frame_archivos_label = Label(frame_archivos, text="Archivos Enviados y Cargados")
frame_archivos_label.pack()

# Frame para los archivos enviados
frame_enviados = Frame(frame_archivos)
frame_enviados.pack(side=LEFT, padx=10)
frame_enviados_label = Label(frame_enviados, text="Enviados")
frame_enviados_label.pack()
boton_enviado = Button(frame_enviados, text="Enviado")
boton_enviado.pack()

# Frame para los archivos cargados
frame_cargados = Frame(frame_archivos)
frame_cargados.pack(side=LEFT, padx=10)
frame_cargados_label = Label(frame_cargados, text="Cargados")
frame_cargados_label.pack()
boton_cargado = Button(frame_cargados, text="Cargado")
boton_cargado.pack()

# Frame para mostrar el estado de los archivos
frame_estado_archivos = Frame(ventana)
frame_estado_archivos.place(relx=0.5, rely=0.95, anchor=S)
texto_estado = StringVar()
texto_estado.set("True")  # Valor inicial, puede ser "True" o "False"
label_estado = Label(frame_estado_archivos, text="Archivos son iguales: ")
label_estado.pack(side=LEFT)
campo_estado = Entry(frame_estado_archivos, textvariable=texto_estado, state='readonly')
campo_estado.pack(side=LEFT)

# Frame para la lista desplegable de iteración
frame_iteracion = Frame(ventana, bd=2, relief="groove")
frame_iteracion.place(relx=0.25, rely=0.4, anchor=CENTER)
frame_iteracion_label = Label(frame_iteracion, text="Lista de Iteración")
frame_iteracion_label.pack()
# Lista desplegable de iteración
lista_despegable_iteracion = ttk.Combobox(frame_iteracion, width=17)
lista_despegable_iteracion.pack()


# Frame para la lista desplegable de entidades
frame_entidades = Frame(ventana, bd=2, relief="groove")
frame_entidades.place(relx=0.75, rely=0.4, anchor=CENTER)
frame_entidades_label = Label(frame_entidades, text="Lista de Entidades")
frame_entidades_label.pack()
# Lista desplegable de entidades
lista_despegable_entidades = ttk.Combobox(frame_entidades, width=17)
lista_despegable_entidades.pack()


# LISTA DE ITERACION 
opciones_iteracion = ["ITERACION 3.1", "DELTA","DELTA2"]
# INSERTAR VALORES
lista_despegable_iteracion['values']=opciones_iteracion


# LISTA DE ENTIDADES
opciones_entidades = ["entidad1", "entidad2", "entidad3"]
# INSERCCIONES DE LAS ENTIDADES
lista_despegable_entidades["values"]=opciones_entidades

ventana.mainloop()
