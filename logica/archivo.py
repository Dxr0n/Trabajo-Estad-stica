import pandas as pd
import traceback
from tkinter import filedialog, messagebox

def seleccionar_archivo(lista_hojas_var, lista_desplegable_widget):
    try:
        archivo = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx *.xls")])
        if not archivo:
            messagebox.showwarning("Advertencia", "No se seleccionó ningún archivo.")
            return None, None

        hojas = pd.ExcelFile(archivo).sheet_names
        if not hojas:
            messagebox.showerror("Error", "No se encontraron hojas en el archivo.")
            return None, None

        # Establecer primera hoja como predeterminada
        lista_hojas_var.set(hojas[0])
        menu = lista_desplegable_widget["menu"]
        menu.delete(0, "end")
        for hoja in hojas:
            menu.add_command(label=hoja, command=lambda value=hoja: lista_hojas_var.set(value))

        return archivo, hojas[0]

    except Exception as e:
        traceback.print_exc()
        messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")
        return None, None


def cargar_archivo(archivo, hoja, callback_post_carga, quitar_columna_id=True):
    try:
        if not archivo or not hoja:
            messagebox.showwarning("Advertencia", "Debe seleccionar un archivo y una hoja.")
            return None

        df = pd.read_excel(archivo, sheet_name=hoja)

        if df.empty:
            messagebox.showerror("Error", "La hoja seleccionada está vacía.")
            return None

        if quitar_columna_id and 'id' in df.columns:
            df = df.drop(columns=['id'])

        callback_post_carga(df)
        return df

    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo no se encontró.")
    except ValueError as e:
        traceback.print_exc()
        messagebox.showerror("Error", f"Error al leer el archivo:\n{e}")
    except Exception as e:
        traceback.print_exc()
        messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{e}")

    return None
