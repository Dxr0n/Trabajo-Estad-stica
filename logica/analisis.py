import tkinter as tk
from tkinter import ttk
import pandas as pd

checkboxes_globales = []

def mostrar_tabla_previa(df, frame_datos):
    for widget in frame_datos.winfo_children():
        widget.destroy()

    df_preview = df.head(200)
    cols = list(df_preview.columns)

    contenedor = tk.Frame(frame_datos, bg="#ffffff", relief="ridge", bd=2)
    contenedor.pack(fill="both", expand=True, padx=10, pady=10)

    scroll_x = ttk.Scrollbar(contenedor, orient="horizontal")
    scroll_y = ttk.Scrollbar(contenedor, orient="vertical")
    scroll_x.pack(side="bottom", fill="x")
    scroll_y.pack(side="right", fill="y")

    tree = ttk.Treeview(contenedor, columns=cols, show='headings',
                        yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, style="Treeview")
    scroll_x.config(command=tree.xview)
    scroll_y.config(command=tree.yview)

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    for i, row in df_preview.iterrows():
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        tree.insert("", "end", values=list(row), tags=(tag,))
    tree.tag_configure("evenrow", background="#f9f9f9")  #ajustar color 
    tree.tag_configure("oddrow", background="#ecf0f1")   #ajustar color 
    tree.pack(fill="both", expand=True)

    if len(df) > 200:
        ttk.Label(frame_datos,
                  text=f"Mostrando las primeras 200 filas de {len(df)} total",
                  foreground="#636e72", font=("Helvetica", 9, "italic")).pack(pady=5)

def actualizar_lista_columnas(df, frame_columnas, manejar_callback,
                               precision_var, redondeo_var, aplicar_redondeo_var,
                               actualizar_precision_fn, actualizar_redondeo_fn,
                               procesar_fn):
    global checkboxes_globales
    checkboxes_globales.clear()

    for widget in frame_columnas.winfo_children():
        widget.destroy()

    tipos = {
        "Variables Cualitativas (Categóricas)": 
        [col for col in df.columns if df[col].dtype == "object"],
        "Variables Cuantitativas (<10 valores únicos)": 
        [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col]) and df[col].nunique() < 10],
        "Variables Cuantitativas (≥10 valores únicos)": 
        [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col]) and df[col].nunique() >= 10]
    }

    colores = {
        "Variables Cualitativas (Categóricas)": "#00cec9",
        "Variables Cuantitativas (<10 valores únicos)": "#6c5ce7",
        "Variables Cuantitativas (≥10 valores únicos)": "#e17055"
    }

    for titulo, columnas in tipos.items():
        marco = tk.LabelFrame(frame_columnas, text=titulo, bg="#ffffff", fg=colores[titulo],
                              font=("Helvetica", 10, "bold"), padx=10, pady=5, relief="ridge", bd=2)
        marco.pack(fill="x", padx=10, pady=5)

        frame_checkboxes = tk.Frame(marco, bg="#ffffff")
        frame_checkboxes.pack(fill="x")

        izq = tk.Frame(frame_checkboxes, bg="#ffffff")
        der = tk.Frame(frame_checkboxes, bg="#ffffff")
        izq.pack(side="left", expand=True, fill="both")
        der.pack(side="right", expand=True, fill="both")

        for i, col in enumerate(columnas):
            var = tk.BooleanVar(value=False)
            destino = izq if i % 2 == 0 else der
            chk = tk.Checkbutton(destino, text=col, variable=var,
                                 command=lambda c=col, v=var: manejar_callback(c, v),
                                 bg="#ffffff", fg="#2d3436", font=("Helvetica", 10),
                                 anchor="w", activebackground="#ffeaa7")
            chk.var = var
            chk.columna = col
            chk.pack(anchor="w", pady=1)
            checkboxes_globales.append(chk)

def obtener_columna_seleccionada():
    for chk in checkboxes_globales:
        if chk.var.get():
            return chk.columna
    return None
