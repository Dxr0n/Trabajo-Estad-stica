import tkinter as tk
from tkinter import ttk, messagebox
from gui.interfaz import construir_interfaz
from gui.estilos import aplicar_estilos
from logica.archivo import seleccionar_archivo, cargar_archivo
from logica.analisis import (
    mostrar_tabla_previa,
    actualizar_lista_columnas,
    obtener_columna_seleccionada,
    checkboxes_globales,
)
from logica.estadisticas import (
    mostrar_estadisticas,
    actualizar_precision_estadisticas,
    actualizar_redondeo_amplitud,
)
from logica.tabla import generar_tabla_frecuencia
from logica.graficos import generar_grafico
from logica.medidas import calcular_medidas_tendencia_central

# === Inicialización de app ===
root = tk.Tk()
root.title("Análisis de Datos - Excel")
root.state("zoomed")
root.configure(bg="#ffffff")

# === Construcción de la interfaz ===
frames = construir_interfaz(root)
notebook = frames["notebook"]
frame_info_archivo = frames["frame_info_archivo"]
frame_nombre_archivo = frames["frame_nombre_archivo"]
frame_columnas = frames["frame_columnas"]
frame_datos = frames["frame_datos"]
frame_estadisticas = frames["frame_estadisticas"]
frame_datos_frecuencias = frames["frame_datos_frecuencias"]
frame_tendencias_texto = frames["frame_tendencias_texto"]
frame_graficos = frames["frame_graficos"]
frame_ver_datos = frames["frame_ver_datos"]
frame_frecuencias_root = frames["frame_frecuencias_root"]

# === Variables Globales ===
archivo = ""
df_actual = None
grafico_canvas_frame = None  # 🆕 canvas dedicado al gráfico
frame_estadisticas_resultado = None  # se crea en post_carga
lista_hojas = tk.StringVar()
precision_decimales = tk.IntVar(value=2)
opcion_redondeo = tk.StringVar(value="0.1")
aplicar_redondeo_var = tk.BooleanVar(value=True)
tipo_grafico = tk.StringVar(value="Histograma")

# === Widgets para carga de archivo ===
ttk.Label(frame_info_archivo, text="Seleccione un archivo Excel para analizar:").pack(
    anchor="w", pady=(5, 2)
)
ttk.Button(
    frame_info_archivo,
    text="🟢 Seleccionar archivo",
    command=lambda: accion_seleccionar(),
).pack(anchor="w")
ttk.Label(frame_info_archivo, text="Seleccione una hoja:").pack(anchor="w", pady=(10, 2))
lista_desplegable = ttk.OptionMenu(frame_info_archivo, lista_hojas, "")
lista_desplegable.pack(anchor="w")
ttk.Button(
    frame_info_archivo, text="📥 Cargar hoja", command=lambda: accion_cargar()
).pack(pady=10)


# === Funciones ===
def accion_seleccionar():
    global archivo
    archivo, _ = seleccionar_archivo(lista_hojas, lista_desplegable)
    frame_nombre_archivo.delete("all")
    if archivo:
        nombre = archivo.split("/")[-1]
        frame_nombre_archivo.create_text(
            10,
            12,
            anchor="w",
            text=f"Archivo cargado: {nombre}",
            fill="#333333",
            font=("Helvetica", 10, "bold"),
        )


def accion_cargar():
    global df_actual
    hoja = lista_hojas.get()
    df_actual = cargar_archivo(archivo, hoja, post_carga)


def post_carga(df):
    global frame_estadisticas_resultado
    if df is None:
        return

    mostrar_tabla_previa(df, frame_datos)

    actualizar_lista_columnas(
        df,
        frame_columnas,
        manejar_seleccion_columna,
        precision_decimales,
        opcion_redondeo,
        aplicar_redondeo_var,
        actualizar_precision_estadisticas_callback,
        actualizar_redondeo_callback,
        procesar_columna_seleccionada,
    )

    # Frame de resultados estadísticos bajo checkboxes
    frame_estadisticas_resultado = tk.Frame(frame_columnas, bg="#ffffff")
    frame_estadisticas_resultado.pack(fill="x", padx=10, pady=(10, 5))

    # Redibujar controles de precisión / redondeo en panel derecho
    for widget in frame_estadisticas.winfo_children():
        widget.destroy()

    tk.Label(
        frame_estadisticas,
        text="Precisión de decimales:",
        font=("Helvetica", 10),
        bg="#ffffff",
    ).pack(anchor="w", padx=10, pady=(5, 2))
    ttk.OptionMenu(
        frame_estadisticas,
        precision_decimales,
        precision_decimales.get(),
        *range(0, 7),
    ).pack(anchor="w", padx=10)
    ttk.Button(
        frame_estadisticas,
        text="Actualizar Precisión",
        command=actualizar_precision_estadisticas_callback,
    ).pack(anchor="w", padx=10, pady=(5, 10))

    tk.Label(
        frame_estadisticas,
        text="Redondear amplitud a:",
        font=("Helvetica", 10),
        bg="#ffffff",
    ).pack(anchor="w", padx=10)
    opciones_redondeo = ["1", "0.1", "0.01", "0.001", "0.0001"]
    ttk.OptionMenu(
        frame_estadisticas,
        opcion_redondeo,
        opcion_redondeo.get(),
        *opciones_redondeo,
    ).pack(anchor="w", padx=10)
    tk.Checkbutton(
        frame_estadisticas,
        text="Aplicar redondeo",
        variable=aplicar_redondeo_var,
        bg="#ffffff",
        font=("Helvetica", 10),
    ).pack(anchor="w", padx=10)
    ttk.Button(
        frame_estadisticas,
        text="Actualizar Redondeo",
        command=actualizar_redondeo_callback,
    ).pack(anchor="w", padx=10, pady=(5, 10))

    ttk.Button(
        frame_estadisticas,
        text="Generar Tabla de Frecuencias",
        command=procesar_columna_seleccionada,
    ).pack(anchor="center", pady=10)

    # Selector de tipo de gráfico
    mostrar_selector_tipo_grafico()
    notebook.select(frame_ver_datos)


# === Callbacks aux ===
def actualizar_precision_estadisticas_callback():
    columna = obtener_columna_seleccionada()
    if columna:
        actualizar_precision_estadisticas(
            df_actual, columna, precision_decimales, frame_estadisticas_resultado
        )


def actualizar_redondeo_callback():
    columna = obtener_columna_seleccionada()
    if columna:
        actualizar_redondeo_amplitud(
            df_actual,
            opcion_redondeo,
            aplicar_redondeo_var,
            frame_estadisticas_resultado,
            columna,
        )


# === Manejo de selección de columnas ===
def manejar_seleccion_columna(columna, var):
    if var.get():
        for chk in checkboxes_globales:
            if chk.columna != columna:
                chk.var.set(False)

        mostrar_estadisticas(
            df_actual,
            columna,
            precision_decimales,
            aplicar_redondeo_var,
            frame_estadisticas_resultado,
            opcion_redondeo,
        )
        if grafico_canvas_frame:
            generar_grafico(
                df_actual,
                columna,
                precision_decimales,
                grafico_canvas_frame,
                tipo_grafico.get(),
            )
    else:
        for widget in frame_estadisticas_resultado.winfo_children():
            widget.destroy()


# === Procesar columna seleccionada ===
def procesar_columna_seleccionada():
    columna = obtener_columna_seleccionada()
    if columna:
        generar_tabla_frecuencia(
            df_actual, columna, frame_datos_frecuencias
        )
        if grafico_canvas_frame:
            generar_grafico(
                df_actual,
                columna,
                precision_decimales,
                grafico_canvas_frame,
                tipo_grafico.get(),
            )
        calcular_medidas_tendencia_central(
            df_actual, columna, frame_tendencias_texto
        )
        notebook.select(frame_frecuencias_root)
    else:
        messagebox.showwarning("Advertencia", "Seleccione una columna primero.")

def actualizar_grafico_sin_redirigir():
    columna = obtener_columna_seleccionada()
    if columna and grafico_canvas_frame:
        generar_grafico(df_actual, columna, precision_decimales, grafico_canvas_frame, tipo_grafico.get())

# === Selector y canvas del gráfico ===
def mostrar_selector_tipo_grafico():
    global grafico_canvas_frame

    # Limpiar todo pero mantener el selector
    for widget in frame_graficos.winfo_children():
        widget.destroy()

    selector_frame = ttk.LabelFrame(frame_graficos, text="🎨 Tipo de gráfico")
    selector_frame.pack(fill="x", padx=10, pady=5)

    ttk.Label(selector_frame, text="Seleccione tipo de gráfico:").pack(
        side="left", padx=(10, 5)
    )
    opciones = ["Histograma", "Polígono de Frecuencias", "Ojiva"]
    ttk.OptionMenu(
        selector_frame,
        tipo_grafico,
        tipo_grafico.get(),
        *opciones,
        command=lambda _: actualizar_grafico_sin_redirigir(),
    ).pack(side="left", padx=5)

    # Canvas dedicado (para no borrar el selector cada vez)
    grafico_canvas_frame = ttk.Frame(frame_graficos)
    grafico_canvas_frame.pack(fill="both", expand=True)

    if df_actual is not None and obtener_columna_seleccionada():
        generar_grafico(
            df_actual,
            obtener_columna_seleccionada(),
            precision_decimales,
            grafico_canvas_frame,
            tipo_grafico.get(),
        )

# === Aplicar estilos y ejecutar ===
aplicar_estilos()
root.mainloop()
