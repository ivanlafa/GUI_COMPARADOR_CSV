import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from datetime import datetime

class ComparadorCSV:
    def __init__(self, master):
        self.master = master
        self.master.title("Comparador de CSVs")

        self.frame = ttk.Frame(self.master, padding="20")
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_columnconfigure(1, weight=1)  # Columna 1 con tamaño adaptable

        self.label_iteracion = ttk.Label(self.frame, text="Iteración: ")
        self.label_iteracion.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.iteracion = ttk.Entry(self.frame)
        self.iteracion.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.iteracion.insert(0, "DELTA")

        self.label_fase = ttk.Label(self.frame, text="Fase:")
        self.label_fase.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.fase = ttk.Entry(self.frame)
        self.fase.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.fase.insert(0, "FASE ")

        self.label_entidad = ttk.Label(self.frame, text="Entidad: ")
        self.label_entidad.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entidad = ttk.Entry(self.frame)
        self.entidad.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.label_enviado = ttk.Label(self.frame, text="Archivo Enviado: ")
        self.label_enviado.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.enviado = ttk.Entry(self.frame)
        self.enviado.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.boton_enviado = ttk.Button(self.frame, text="Seleccionar", command=self.cargar_archivo_enviado)
        self.boton_enviado.grid(row=3, column=2, padx=10, pady=5)
        self.boton_enviado.configure(style="Custom.TButton")  # Aplicar estilo personalizado

        self.label_cargado = ttk.Label(self.frame, text="Archivo Cargado: ")
        self.label_cargado.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.cargado = ttk.Entry(self.frame)
        self.cargado.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        self.boton_cargado = ttk.Button(self.frame, text="Seleccionar", command=self.cargar_archivo_cargado)
        self.boton_cargado.grid(row=4, column=2, padx=10, pady=5)
        self.boton_cargado.configure(style="Custom.TButton")  # Aplicar estilo personalizado

        self.boton_comparar = ttk.Button(self.master, text="Comparar", command=self.comparar_archivos)
        self.boton_comparar.grid(row=1, column=0, pady=10)
        self.boton_comparar.configure(style="Accent.TButton")  # Aplicar estilo personalizado

        # Definir estilos personalizados
        self.style = ttk.Style()
        self.style.configure("Custom.TButton", background="#4CAF50", foreground="black", padding=10, width=15) #color verde
        self.style.configure("Accent.TButton", background="#2196F3", foreground="black", padding=10, width=15) #color amarillo

    def cargar_archivo_enviado(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            self.enviado.delete(0, tk.END)
            self.enviado.insert(0, filename)

    def cargar_archivo_cargado(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            self.cargado.delete(0, tk.END)
            self.cargado.insert(0, filename)

    def comparar_archivos(self):
        archivo_enviado = self.enviado.get()
        archivo_cargado = self.cargado.get()

        if not archivo_enviado or not archivo_cargado:
            messagebox.showerror("Error", "Por favor, seleccione ambos archivos necesarios.")
            return

        try:
            config = {"delimiter": ","}
            columnas_a_ignorar = ["created_date", "novedad", "assetgroup", "assettype", "shape_area", "fuente", "PARQUE"]

            df1 = pd.read_csv(archivo_enviado, dtype=str, encoding='latin-1', **config)
            df2 = pd.read_csv(archivo_cargado, dtype=str, encoding='latin-1', **config)

            # Normalizar los valores en las columnas seleccionadas antes de comparar
            df1 = df1.apply(lambda col: col.map(self.normalizar_valor) if col.name not in columnas_a_ignorar else col)
            df2 = df2.apply(lambda col: col.map(self.normalizar_valor) if col.name not in columnas_a_ignorar else col)

            df1.columns = df1.columns.str.lower()
            df2.columns = df2.columns.str.lower()

            # Eliminar las columnas a ignorar
            df1.drop(columns=columnas_a_ignorar, errors='ignore', inplace=True)
            df2.drop(columns=columnas_a_ignorar, errors='ignore', inplace=True)

            diccionario_assets = {fila["assetid"]: fila for _, fila in df1.iterrows()}

            lista_info_assetid = []
            for assetid, fila in diccionario_assets.items():
                asset_info = {"assetid": assetid}
                diferencias_asset = False
                if assetid in df2["assetid"].values:
                    for columna in df1.columns:
                        if columna != "assetid":
                            if columna in fila and columna in df2.columns:
                                valor1 = fila[columna]
                                valor2 = df2.loc[df2["assetid"] == assetid, columna].values[0]
                                iguales = self.comparar_valores(valor1, valor2)
                                if not iguales:
                                    asset_info[columna] = {"ENVIADO": valor1, "CARGADO": valor2, "iguales": False}
                                    diferencias_asset = True
                            else:
                                asset_info[columna] = {"ENVIADO": fila[columna], "CARGADO": None, "iguales": False}
                                diferencias_asset = True
                else:
                    for columna in df1.columns:
                        if columna != "assetid":
                            asset_info[columna] = {"ENVIADO": fila[columna], "CARGADO": None, "iguales": False}
                            diferencias_asset = True

                if diferencias_asset:
                    lista_info_assetid.append(asset_info)

            df_info = pd.DataFrame(lista_info_assetid)

            if not df_info.empty:
                columnas_ok = [columna for columna in df_info.columns if all(df_info[columna] == "ok")]
                df_info.drop(columns=columnas_ok, inplace=True)

                # Guardar el DataFrame df_info en un archivo CSV
                archivo_resultado = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
                if archivo_resultado:
                    df_info.to_csv(archivo_resultado, index=False, sep=config["delimiter"])
                    messagebox.showinfo("Éxito", f"CSV generado con éxito en {archivo_resultado}")
                else:
                    messagebox.showinfo("Advertencia", "No se seleccionó un nombre de archivo. No se ha guardado el CSV.")

            else:
                messagebox.showinfo("Sin diferencias", "No se encontraron diferencias. No se generó ningún archivo CSV.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al comparar archivos CSV: {str(e)}")

    @staticmethod
    def normalizar_valor(valor):
        if isinstance(valor, str):
            valor = valor.replace(",", ".")
            if '.' in valor:
                try:
                    float_valor = float(valor)
                    int_valor = int(float_valor)
                    if float_valor == int_valor:
                        return int_valor
                    return float_valor
                except ValueError:
                    pass
            elif valor.strip() == '0':
                return 0
        return valor

    @staticmethod
    def comparar_valores(valor1, valor2):
        def parse_fecha(fecha_str):
            try:
                return datetime.strptime(str(fecha_str), '%d/%m/%Y')
            except ValueError:
                return None

        fecha1 = parse_fecha(valor1)
        fecha2 = parse_fecha(valor2)

        if fecha1 and fecha2 and fecha1 == fecha2:
            return True

        if (pd.isna(valor1) and pd.isna(valor2)) or (str(valor1).strip() == '' and str(valor2).strip() == ''):
            return True

        elif (isinstance(valor1, (int, float)) or isinstance(valor2, (int, float))) and valor1 == valor2:
            return True

        elif valor1 == 0 and valor2 == 0:
            return True

        return valor1 == valor2

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x300")  # Tamaño inicial de la ventana
    app = ComparadorCSV(root)
    root.mainloop()
