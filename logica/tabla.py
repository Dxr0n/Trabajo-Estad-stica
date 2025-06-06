import tkinter as tk
from tkinter import messagebox, ttk
import math
import pandas as pd
from logica.analisis import mostrar_tabla_previa
from logica.utilidades import calcular_numero_intervalos

def generar_tabla_frecuencia(df, columna, frame_salida):
    try:
        datos = df[columna].dropna()
        total = len(datos)
        nulos = df[columna].isna().sum()
        valores_unicos = datos.nunique()

        if valores_unicos == 1:
            messagebox.showwarning("Advertencia", f"Todos los valores en '{columna}' son iguales. No se puede generar una tabla válida.")
            return

        if datos.dtypes == 'object' or valores_unicos < 10:
            frecuencia = datos.value_counts().reset_index()
            frecuencia.columns = [columna, "Frecuencia Absoluta"]
            frecuencia = frecuencia.sort_values(by=columna).reset_index(drop=True)
        else:
            minimo, maximo = datos.min(), datos.max()
            rango = maximo - minimo
            k = calcular_numero_intervalos(total)
            amplitud = rango / k if k > 0 else 1

            bins = [minimo + i * amplitud for i in range(k + 1)]
            categorias = pd.cut(datos, bins=bins, include_lowest=True, right=True, duplicates='drop')
            frecuencia = categorias.value_counts(sort=False).reset_index()
            frecuencia.columns = ["Intervalo", "Frecuencia Absoluta"]
            frecuencia.insert(1, "Marca de Clase", [round((intv.left + intv.right) / 2, 2) for intv in frecuencia["Intervalo"]])
            frecuencia = frecuencia.sort_values("Intervalo").reset_index(drop=True)

        frecuencia["Frecuencia Absoluta Acumulada"] = frecuencia["Frecuencia Absoluta"].cumsum()
        frecuencia["Frecuencia Relativa"] = (frecuencia["Frecuencia Absoluta"] / total).round(3)
        frecuencia["Frecuencia Relativa Acumulada"] = frecuencia["Frecuencia Relativa"].cumsum().round(3)
        frecuencia["Frecuencia Relativa Porcentual"] = (frecuencia["Frecuencia Relativa"] * 100).round(3)

        fila_total = {col: "" for col in frecuencia.columns}
        fila_total[frecuencia.columns[0]] = "Total"
        fila_total["Frecuencia Absoluta"] = frecuencia["Frecuencia Absoluta"].sum()
        fila_total["Frecuencia Relativa"] = frecuencia["Frecuencia Relativa"].sum().round(0)
        fila_total["Frecuencia Relativa Porcentual"] = frecuencia["Frecuencia Relativa Porcentual"].sum()
        frecuencia = pd.concat([frecuencia, pd.DataFrame([fila_total])], ignore_index=True)

        mostrar_tabla_frecuencias(frecuencia, frame_salida)

        if nulos > 0:
            tk.Label(frame_salida, text=f"Valores nulos en '{columna}': {nulos}",
                     fg='red', font=("Helvetica", 10, "italic")).pack(pady=5)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar la tabla de frecuencias: {e}")


def mostrar_tabla_frecuencias(df_tabla, frame):
    for widget in frame.winfo_children():
        widget.destroy()

    columnas = list(df_tabla.columns)

    contenedor = tk.Frame(frame, bg="#ffffff", relief="ridge", bd=2)
    contenedor.pack(fill="both", expand=True, padx=10, pady=10)

    scroll_x = ttk.Scrollbar(contenedor, orient="horizontal")
    scroll_y = ttk.Scrollbar(contenedor, orient="vertical")
    scroll_x.pack(side="bottom", fill="x")
    scroll_y.pack(side="right", fill="y")

    tree = ttk.Treeview(
        contenedor, columns=columnas, show='headings',
        yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, style="Treeview"
    )
    scroll_x.config(command=tree.xview)
    scroll_y.config(command=tree.yview)

    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=140, anchor="center")

    for i, row in df_tabla.iterrows():
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        tree.insert("", "end", values=list(row), tags=(tag,))

    tree.tag_configure("evenrow", background="#f9f9f9") #ajustar color 
    tree.tag_configure("oddrow", background="#ecf0f1") #ajustar color 

    tree.pack(fill="both", expand=True)
