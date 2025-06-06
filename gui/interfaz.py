# === interfaz.py ===
import tkinter as tk
from tkinter import ttk

def construir_interfaz(root):
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # Crear frames para cada pestaña
    frame_cargar = ttk.Frame(notebook)
    frame_ver_datos = ttk.Frame(notebook)
    frame_frecuencias_root = ttk.Frame(notebook)
    frame_tendencias = ttk.Frame(notebook)
    frame_graficos_root = ttk.Frame(notebook)

    notebook.add(frame_cargar, text="📂 Cargar Datos")
    notebook.add(frame_ver_datos, text="📊 Ver Datos")
    notebook.add(frame_frecuencias_root, text="📈 Tabla de Frecuencias")
    notebook.add(frame_tendencias, text="📐 Medidas Estadísticas")
    notebook.add(frame_graficos_root, text="📉 Gráficos")

    # === CARGAR ARCHIVO ===
    frame_info_archivo = ttk.LabelFrame(frame_cargar, text="📁 Cargar Archivo Excel")
    frame_info_archivo.pack(padx=10, pady=10, fill="x")

    frame_nombre_archivo = tk.Canvas(frame_cargar, height=25, bg="white", bd=0, highlightthickness=0)
    frame_nombre_archivo.pack(fill="x", padx=10)

    # === VER DATOS ===
    top_frame = ttk.LabelFrame(frame_ver_datos, text="🛠️ Selección y Configuración de Variables")
    top_frame.pack(fill="x", padx=10, pady=(10, 5))

    main_split = ttk.PanedWindow(frame_ver_datos, orient="horizontal")
    main_split.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    frame_columnas = ttk.Frame(main_split)
    main_split.add(frame_columnas, weight=1)

    frame_estadisticas = ttk.LabelFrame(main_split, text="⚙️ Opciones de Precisión / Redondeo")
    main_split.add(frame_estadisticas, weight=1)

    frame_datos = ttk.LabelFrame(frame_ver_datos, text="👁️ Vista Previa de Datos")
    frame_datos.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # === TABLA DE FRECUENCIAS ===
    frame_frecuencias = ttk.LabelFrame(frame_frecuencias_root, text="📊 Tabla de Frecuencias")
    frame_frecuencias.pack(fill="both", expand=True, padx=10, pady=10)
    frame_datos_frecuencias = ttk.Frame(frame_frecuencias)
    frame_datos_frecuencias.pack(fill="both", expand=True)

    # === MEDIDAS ESTADÍSTICAS ===
    frame_tendencias_texto = tk.Text(frame_tendencias, height=20, font=("Courier New", 11), bg="#f9f9f9")
    frame_tendencias_texto.pack(fill="both", expand=True, padx=10, pady=10)

    # === GRÁFICOS ===
    frame_graficos = ttk.Frame(frame_graficos_root)
    frame_graficos.pack(fill="both", expand=True)

    return {
        "notebook": notebook,
        "frame_info_archivo": frame_info_archivo,
        "frame_nombre_archivo": frame_nombre_archivo,
        "frame_columnas": frame_columnas,
        "frame_datos": frame_datos,
        "frame_estadisticas": frame_estadisticas,
        "frame_datos_frecuencias": frame_datos_frecuencias,
        "frame_tendencias_texto": frame_tendencias_texto,
        "frame_graficos": frame_graficos,
        "frame_ver_datos": frame_ver_datos,
        "frame_frecuencias_root": frame_frecuencias_root,
    }
