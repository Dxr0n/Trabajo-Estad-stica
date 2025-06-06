import tkinter as tk

def calcular_medidas_tendencia_central(df, columna, frame_salida):
    datos = df[columna].dropna()

    for widget in frame_salida.winfo_children():
        widget.destroy()

    if datos.empty:
        tk.Label(frame_salida, text="No hay datos válidos.",
                 fg="red", font=("Helvetica", 10, "italic")).pack(pady=10)
        return

    valores_unicos = datos.nunique()
    info = {}

    if datos.dtypes == 'object' or valores_unicos < 10:
        info["Moda"] = datos.mode()[0] if not datos.mode().empty else "No disponible"
    else:
        info.update({
            "Promedio": round(datos.mean(), 2),
            "Mediana": round(datos.median(), 2),
            "Moda": datos.mode()[0] if not datos.mode().empty else "No disponible",
            "Mínimo": round(datos.min(), 2),
            "Máximo": round(datos.max(), 2),
            "Rango": round(datos.max() - datos.min(), 2),
            "Varianza": round(datos.var(), 2),
            "Desviación estándar": round(datos.std(), 2),
            "Coef. de variación": f"{round((datos.std() / datos.mean()) * 100, 2)}%" if datos.mean() != 0 else "0%"
        })

    for key, val in info.items():
        card = tk.Frame(frame_salida, bg="#ffffff", relief="solid", bd=1)
        card.pack(fill="x", padx=20, pady=5)

        tk.Label(card, text=f"{key}:", font=("Helvetica", 10, "bold"),
                 bg="#ffffff", fg="#2d3436", anchor="w").pack(side="left", padx=10, pady=5)

        tk.Label(card, text=str(val), font=("Helvetica", 10),
                 bg="#ffffff", fg="#0984e3", anchor="e").pack(side="right", padx=10)
