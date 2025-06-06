# === estilos.py ===
from tkinter import ttk

def aplicar_estilos():
    style = ttk.Style()
    style.theme_use("clam")

    # Frame y Labels
    style.configure("TFrame", background="#f7f7f7")
    style.configure("TLabel", background="#f7f7f7", foreground="#333", font=("Helvetica", 11))
    style.configure("TLabelframe", background="#f7f7f7", foreground="#333333", font=("Helvetica", 11, "bold"))
    style.configure("TLabelframe.Label", background="#f7f7f7", font=("Helvetica", 11, "bold"))

    # Botones
    style.configure("TButton", background="#4CAF50", foreground="white", font=("Helvetica", 11, "bold"), padding=6)
    style.map("TButton", background=[("active", "#45a049")])

    # Treeview
    style.configure("Treeview",
                    background="#ffffff",
                    foreground="#333333",
                    rowheight=25,
                    fieldbackground="#ffffff",
                    font=("Helvetica", 10))
    style.configure("Treeview.Heading",
                    background="#4CAF50",
                    foreground="white",
                    font=("Helvetica", 11, "bold"))
    style.map("Treeview", background=[("selected", "#a1d99b")])

    style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
