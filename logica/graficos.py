import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
from pandas.api.types import is_numeric_dtype
from logica.utilidades import calcular_numero_intervalos

def generar_grafico(df, columna, precision_decimales, frame_graficos, tipo_grafico="Histograma"):
    for widget in frame_graficos.winfo_children():
        widget.destroy()

    if columna not in df.columns:
        messagebox.showerror("Error", f"La columna '{columna}' no existe en el DataFrame.")
        return

    datos = df[columna].dropna()
    if datos.empty:
        messagebox.showinfo("Información", "La columna seleccionada no contiene datos válidos.")
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('white')

    titulo = columna.replace("_", " ").title()
    valores_unicos = datos.nunique()

    if not is_numeric_dtype(datos) or valores_unicos < 10:
        conteo = datos.value_counts().sort_index()
        etiquetas = conteo.index.tolist()
        colores = [
            "#f8b195", "#f67280", "#c06c84", "#6c5b7b", "#355c7d",
            "#a8e6cf", "#dcedc1", "#ffd3b6", "#ffaaa5", "#ff8b94"
        ]
        ax.bar(etiquetas, conteo.values, color=colores[:len(etiquetas)],
               edgecolor="#2d3436", width=0.6)
        ax.set_title(f"Frecuencia de {titulo}", fontsize=14, fontweight="bold")
        ax.set_ylabel("Frecuencia", fontsize=11)
        ax.tick_params(axis='x', rotation=45)
    else:
        precision = precision_decimales.get() if hasattr(precision_decimales, "get") else 2
        minimo, maximo = datos.min(), datos.max()
        rango = maximo - minimo
        k = calcular_numero_intervalos(len(datos))
        amplitud = round(rango / k, precision) if k > 0 else 1
        bins = [minimo + i * amplitud for i in range(k + 1)]

        if tipo_grafico == "Histograma":
            ax.hist(datos, bins=bins, color="#00b894", edgecolor="#2d3436", alpha=0.85)
            ax.set_title(f"Histograma de {titulo}", fontsize=14, fontweight="bold")
            ax.set_ylabel("Frecuencia", fontsize=11)
            ax.set_xlabel(titulo, fontsize=11)

        elif tipo_grafico == "Polígono de Frecuencias":
            conteo, bins_ = np.histogram(datos, bins=bins)
            puntos_x = (bins_[:-1] + bins_[1:]) / 2
            ax.plot(puntos_x, conteo, marker="o", linestyle='-', linewidth=2, color="#6c5ce7")
            ax.set_title(f"Polígono de Frecuencias de {titulo}", fontsize=14, fontweight="bold")
            ax.set_ylabel("Frecuencia", fontsize=11)
            ax.set_xlabel(titulo, fontsize=11)

        elif tipo_grafico == "Ojiva":
            datos_ordenados = np.sort(datos)
            acumulada = np.arange(1, len(datos_ordenados) + 1) / len(datos_ordenados)
            ax.plot(datos_ordenados, acumulada, color="#fd79a8", linewidth=2)
            ax.set_title(f"Ojiva de {titulo}", fontsize=14, fontweight="bold")
            ax.set_ylabel("Frecuencia Acumulada", fontsize=11)
            ax.set_xlabel(titulo, fontsize=11)

        else:
            ax.text(0.5, 0.5, "Tipo de gráfico no soportado",
                    ha="center", va="center", fontsize=14, color="red")

    ax.grid(True, linestyle='--', alpha=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.close(fig)

    canvas = FigureCanvasTkAgg(fig, master=frame_graficos)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
