import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

def crear_campos_expediente(contenido):
    campos = {}

    # Estilo para Combobox con fuente Arial 12
    estilo = ttk.Style()
    estilo.configure("Estilo.TCombobox", font=("Arial", 12))

    # Línea 1
    campos["combo_clave"] = ttk.Combobox(contenido, state="readonly", width=25, style="Estilo.TCombobox")
    campos["entry_anio"] = tk.Entry(contenido, width=10, font=("Arial", 12))
    campos["combo_fondo"] = ttk.Combobox(contenido, state="readonly", width=25, style="Estilo.TCombobox")
    campos["entry_numero"] = tk.Entry(contenido, width=15, font=("Arial", 12))

    tk.Label(contenido, text="Clave CGCA:", font=("Arial", 12), bg="#F5F5F5").grid(row=0, column=0, sticky="e")
    campos["combo_clave"].grid(row=0, column=1)
    tk.Label(contenido, text="Año apertura:", font=("Arial", 12), bg="#F5F5F5").grid(row=0, column=2, sticky="e")
    campos["entry_anio"].grid(row=0, column=3)
    tk.Label(contenido, text="Fondo:", font=("Arial", 12), bg="#F5F5F5").grid(row=0, column=4, sticky="e")
    campos["combo_fondo"].grid(row=0, column=5)
    tk.Label(contenido, text="Número expediente:", font=("Arial", 12), bg="#F5F5F5").grid(row=0, column=6, sticky="e")
    campos["entry_numero"].grid(row=0, column=7)

    # Línea 2
    campos["combo_unidad"] = ttk.Combobox(contenido, state="readonly", width=50, style="Estilo.TCombobox")
    campos["combo_area"] = ttk.Combobox(contenido, state="readonly", width=50, style="Estilo.TCombobox")

    tk.Label(contenido, text="Unidad Administrativa:", font=("Arial", 12), bg="#F5F5F5").grid(row=1, column=0, sticky="e")
    campos["combo_unidad"].grid(row=1, column=1, columnspan=3)
    tk.Label(contenido, text="Área Generadora:", font=("Arial", 12), bg="#F5F5F5").grid(row=1, column=4, sticky="e")
    campos["combo_area"].grid(row=1, column=5, columnspan=3)

    # Línea 3
    campos["entry_descripcion"] = tk.Text(contenido, width=100, height=4, font=("Arial", 12))
    tk.Label(contenido, text="Descripción del expediente / Asunto:", font=("Arial", 12), bg="#F5F5F5").grid(row=2, column=0, sticky="ne")
    campos["entry_descripcion"].grid(row=2, column=1, columnspan=7)

    # Línea 4
    campos["entry_fecha_apertura"] = DateEntry(contenido, width=20, date_pattern="yyyy-mm-dd", font=("Arial", 12))
    campos["entry_fecha_cierre"] = DateEntry(contenido, width=20, date_pattern="yyyy-mm-dd", font=("Arial", 12))

    tk.Label(contenido, text="Fecha de apertura:", font=("Arial", 12), bg="#F5F5F5").grid(row=3, column=0, sticky="e")
    campos["entry_fecha_apertura"].grid(row=3, column=1)
    tk.Label(contenido, text="Fecha de cierre:", font=("Arial", 12), bg="#F5F5F5").grid(row=3, column=2, sticky="e")
    campos["entry_fecha_cierre"].grid(row=3, column=3)

    # Línea 5
    campos["entry_legajo"] = tk.Entry(contenido, width=15, font=("Arial", 12))
    campos["entry_total_legajos"] = tk.Entry(contenido, width=10, font=("Arial", 12))
    campos["entry_folios_legajo"] = tk.Entry(contenido, width=10, font=("Arial", 12))
    campos["entry_folios_expediente"] = tk.Entry(contenido, width=10, font=("Arial", 12))

    tk.Label(contenido, text="Legajo:", font=("Arial", 12), bg="#F5F5F5").grid(row=4, column=0, sticky="e")
    campos["entry_legajo"].grid(row=4, column=1)
    tk.Label(contenido, text="Total de legajos:", font=("Arial", 12), bg="#F5F5F5").grid(row=4, column=2, sticky="e")
    campos["entry_total_legajos"].grid(row=4, column=3)
    tk.Label(contenido, text="Folios por legajo:", font=("Arial", 12), bg="#F5F5F5").grid(row=4, column=4, sticky="e")
    campos["entry_folios_legajo"].grid(row=4, column=5)
    tk.Label(contenido, text="Folios del expediente:", font=("Arial", 12), bg="#F5F5F5").grid(row=4, column=6, sticky="e")
    campos["entry_folios_expediente"].grid(row=4, column=7)

    # Línea 6
    campos["entry_archivo"] = tk.Entry(contenido, width=50, font=("Arial", 12))
    campos["entry_estanteria"] = tk.Entry(contenido, width=15, font=("Arial", 12))
    campos["entry_caja"] = tk.Entry(contenido, width=15, font=("Arial", 12))

    tk.Label(contenido, text="Archivo:", font=("Arial", 12), bg="#F5F5F5").grid(row=5, column=0, sticky="e")
    campos["entry_archivo"].grid(row=5, column=1, columnspan=3)
    tk.Label(contenido, text="Estantería:", font=("Arial", 12), bg="#F5F5F5").grid(row=5, column=4, sticky="e")
    campos["entry_estanteria"].grid(row=5, column=5)
    tk.Label(contenido, text="Caja:", font=("Arial", 12), bg="#F5F5F5").grid(row=5, column=6, sticky="e")
    campos["entry_caja"].grid(row=5, column=7)

    return campos
