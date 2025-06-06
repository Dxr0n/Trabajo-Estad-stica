import math

def obtener_valor_redondeo(valor):
    """Convierte un valor de string a float para redondeo. Si falla, devuelve 0.1 por defecto."""
    try:
        return float(valor)
    except ValueError:
        return 0.1

def formatear_titulo(texto):
    """Formatea una cadena para que se vea como un título."""
    return texto.replace("_", " ").capitalize()

def es_categorica(serie):
    """Devuelve True si la serie es cualitativa o tiene menos de 10 valores únicos."""
    return serie.dtype == "object" or serie.nunique() < 10

def es_cuantitativa(serie):
    """Devuelve True si la serie es numérica y no es categórica."""
    return not es_categorica(serie)

def calcular_numero_intervalos(n):
    """Calcula número de intervalos usando la Regla de Sturges."""
    return math.ceil(1 + 3.322 * math.log10(n)) if n > 0 else 1

def redondear_amplitud(valor, paso=0.1):
    """Redondea una amplitud al múltiplo más cercano del paso definido."""
    return round(round(valor / paso) * paso, 4)
