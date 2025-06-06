import tkinter as tk
from tkinter import messagebox
from logica.utilidades import obtener_valor_redondeo, calcular_numero_intervalos, redondear_amplitud

ultima_amplitud_utilizada = 0

def aplicar_redondeo_amplitud(amplitud_original, aplicar_redondeo_var, opcion_redondeo):
    if aplicar_redondeo_var.get():
        paso = obtener_valor_redondeo(opcion_redondeo.get())
        return redondear_amplitud(amplitud_original, paso)
    return amplitud_original

def actualizar_redondeo_amplitud(df, opcion_redondeo, aplicar_redondeo_var, frame_estadisticas, columna):
    if columna:
        mostrar_estadisticas(df, columna, None, aplicar_redondeo_var, frame_estadisticas, opcion_redondeo)
    else:
        messagebox.showinfo("Información", "Seleccione una columna primero.")

def actualizar_precision_estadisticas(df, columna, precision_decimales, frame_estadisticas):
    if columna:
        mostrar_estadisticas(df, columna, precision_decimales, None, frame_estadisticas)
    else:
        messagebox.showinfo("Información", "Seleccione una columna.")

def mostrar_estadisticas(df, columna, precision_decimales, aplicar_redondeo_var, frame_estadisticas, opcion_redondeo=None):
    for widget in frame_estadisticas.winfo_children():
        widget.destroy()

    datos = df[columna].dropna()
    if datos.empty:
        return

    minimo = datos.min()
    maximo = datos.max()
    rango = maximo - minimo
    intervalos = calcular_numero_intervalos(len(datos))
    amplitud_base = rango / intervalos if intervalos > 0 else 1

    if aplicar_redondeo_var:
        amplitud = aplicar_redondeo_amplitud(amplitud_base, aplicar_redondeo_var, opcion_redondeo)
    else:
        amplitud = amplitud_base

    precision = precision_decimales.get() if hasattr(precision_decimales, "get") else 2
    amplitud_str = f"{amplitud:.{precision}f}"

    global ultima_amplitud_utilizada
    ultima_amplitud_utilizada = amplitud

    contenedor = tk.Frame(frame_estadisticas, bg="#ffffff")
    contenedor.pack(fill="x")

    tk.Label(contenedor, text="Estadísticas Descriptivas:", font=("Helvetica", 10, "bold"), bg="#ffffff").pack(anchor="w")

    izq = tk.Frame(contenedor, bg="#ffffff")
    izq.pack(side="left", fill="both", expand=True)
    tk.Label(izq, text=f"Mínimo: {minimo}", bg="#ffffff").pack(anchor="w")
    tk.Label(izq, text=f"Máximo: {maximo}", bg="#ffffff").pack(anchor="w")
    tk.Label(izq, text=f"Rango: {rango}", bg="#ffffff").pack(anchor="w")

    der = tk.Frame(contenedor, bg="#ffffff")
    der.pack(side="right", fill="both", expand=True)
    tk.Label(der, text=f"Intervalos: {intervalos}", bg="#ffffff").pack(anchor="w")
    tk.Label(der, text=f"Amplitud: {amplitud_str}", bg="#ffffff").pack(anchor="w")
