import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import psycopg2
from datetime import date
import os

# Conexión a PostgreSQL
def conectar_bd():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="Sistema de Gestión Documental",
        user="postgres",
        password="18brumario"
    )

def cargar_siglas_dependencia():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT siglas_dependencia FROM dependencia")
    resultados = cursor.fetchall()
    conn.close()
    return [r[0] for r in resultados]

# Función para limpiar campos
def limpiar_campos():
    for campo in [entry_clave, entry_anio, entry_numero, entry_unidad, entry_area,
                  entry_legajo, entry_total_legajos, entry_folios_legajo, entry_folios_expediente,
                  entry_archivo, entry_estanteria, entry_caja,
                  entry_id_serie, entry_id_dependencia, entry_id_area, entry_id_cdd]:
        campo.delete(0, tk.END)
    entry_descripcion.delete("1.0", tk.END)
    combo_fondo.set("")
    entry_fecha_apertura.set_date(date.today())
    entry_fecha_cierre.set_date(date.today())
    entry_clave.focus()

# Función extendida para guardar y decidir acción
def guardar_expediente_accion(accion):
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO inventario (
                clave_cgca, anio_apertura, fondo, numero,
                unidad_administrativa, area_generadora, fecha_apertura, fecha_cierre,
                descripcion_expediente, legajo, total_legajos, folios_legajo, folios_expediente,
                archivo, estanteria, caja,
                id_serie, id_dependencia, id_area, id_cdd,
                registrado_por
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            entry_clave.get(),
            int(entry_anio.get()) if entry_anio.get().isdigit() else None,
            combo_fondo.get(),
            entry_numero.get(),
            entry_unidad.get(),
            entry_area.get(),
            entry_fecha_apertura.get_date(),
            entry_fecha_cierre.get_date(),
            entry_descripcion.get("1.0", "end").strip(),
            entry_legajo.get(),
            int(entry_total_legajos.get()) if entry_total_legajos.get().isdigit() else None,
            int(entry_folios_legajo.get()) if entry_folios_legajo.get().isdigit() else None,
            int(entry_folios_expediente.get()) if entry_folios_expediente.get().isdigit() else None,
            entry_archivo.get(),
            entry_estanteria.get(),
            entry_caja.get(),
            int(entry_id_serie.get()) if entry_id_serie.get().isdigit() else None,
            int(entry_id_dependencia.get()) if entry_id_dependencia.get().isdigit() else None,
            int(entry_id_area.get()) if entry_id_area.get().isdigit() else None,
            int(entry_id_cdd.get()) if entry_id_cdd.get().isdigit() else None,
            "Alejandro"
        ))
        conn.commit()
        cursor.close()
        conn.close()

        if accion == "cerrar":
            messagebox.showinfo("Éxito", "Expediente guardado correctamente.")
            ventana.destroy()
        elif accion == "siguiente":
            messagebox.showinfo("Éxito", "Expediente guardado. Puedes ingresar otro.")
            limpiar_campos()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el expediente:\n{e}")

# Ventana principal
ventana = tk.Tk()
ventana.title("Captura de Expediente - Archivos Verdes")
ventana.geometry("1000x700")
ventana.grid_rowconfigure(0, weight=1)
ventana.grid_columnconfigure(0, weight=1)

# Cargar logos institucionales
ruta_base = r"C:\Users\miklo\OneDrive\Documentos\Sistema de Gestión documental\Imagenes"

def cargar_logo(nombre_archivo, escala):
    ruta_completa = os.path.join(ruta_base, nombre_archivo)
    try:
        return tk.PhotoImage(file=ruta_completa).subsample(escala, escala)
    except Exception as e:
        print(f"No se pudo cargar {nombre_archivo}: {e}")
        return None

logo_gobierno = cargar_logo("logo_gobierno.png", 4)
logo_archivos = cargar_logo("logo_archivos.png", 8)
logo_smadsot = cargar_logo("logo_smadsot.png", 4)

encabezado = tk.Frame(ventana, bg="#F5F5F5")
encabezado.pack(pady=10)

for logo in [logo_gobierno, logo_archivos, logo_smadsot]:
    if logo:
        tk.Label(encabezado, image=logo, bg="#F5F5F5").pack(side="left", padx=10)

ventana.logo_gobierno = logo_gobierno
ventana.logo_archivos = logo_archivos
ventana.logo_smadsot = logo_smadsot

# Canvas con scrollbar
canvas = tk.Canvas(ventana)
scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
canvas.grid(row=1, column=0, sticky="nsew")
scrollbar.grid(row=1, column=1, sticky="ns")

scrollable_frame = tk.Frame(canvas)
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Leyenda institucional
fila = 1
tk.Label(scrollable_frame, text="Captura de expedientes", font=("Arial", 14, "bold")).grid(row=fila, column=0, columnspan=2, pady=(5, 0))
fila += 1
ttk.Separator(scrollable_frame, orient="horizontal").grid(row=fila, column=0, columnspan=2, sticky="ew", pady=(0, 10))
fila += 1

fuente = ("Arial", 12)

# Fila 1: Clave CGCA, Año, Fondo, Número
fila_identificacion = tk.Frame(scrollable_frame)
fila_identificacion.grid(row=fila, column=0, columnspan=2, pady=10)

entry_clave = tk.Entry(fila_identificacion, font=fuente, width=15)
entry_anio = tk.Entry(fila_identificacion, font=fuente, width=10)
opciones_fondo = cargar_siglas_dependencia()
combo_fondo = ttk.Combobox(fila_identificacion, values=opciones_fondo, font=fuente, width=15)
entry_numero = tk.Entry(fila_identificacion, font=fuente, width=15)

for label, widget in [("Clave CGCA:", entry_clave),
                      ("Año de apertura:", entry_anio),
                      ("Fondo documental:", combo_fondo),
                      ("Número de expediente:", entry_numero)]:
    tk.Label(fila_identificacion, text=label, font=fuente).pack(side="left", padx=5)
    widget.pack(side="left", padx=5)

fila += 1

# Fila 2: Unidad administrativa + Área generadora
fila_ua_area = tk.Frame(scrollable_frame)
fila_ua_area.grid(row=fila, column=0, columnspan=2, pady=10)

entry_unidad = tk.Entry(fila_ua_area, font=fuente, width=30)
entry_area = tk.Entry(fila_ua_area, font=fuente, width=30)

for label, widget in [("Unidad administrativa:", entry_unidad),
                      ("Área generadora:", entry_area)]:
    tk.Label(fila_ua_area, text=label, font=fuente).pack(side="left", padx=5)
    widget.pack(side="left", padx=5)

fila += 1

# Fila 3: Fecha de apertura + Fecha de cierre
fila_fechas = tk.Frame(scrollable_frame)
fila_fechas.grid(row=fila, column=0, columnspan=2, pady=10)

entry_fecha_apertura = DateEntry(fila_fechas, date_pattern="dd-mm-yyyy", font=fuente, width=12)
entry_fecha_cierre = DateEntry(fila_fechas, date_pattern="dd-mm-yyyy", font=fuente, width=12)

for label, widget in [("Fecha de apertura:", entry_fecha_apertura),
                      ("Fecha de cierre:", entry_fecha_cierre)]:
    tk.Label(fila_fechas, text=label, font=fuente).pack(side="left", padx=5)
    widget.pack(side="left", padx=5)

fila += 1

# Descripción del expediente
tk.Label(scrollable_frame, text="Descripción del expediente:", font=fuente).grid(row=fila, column=0, sticky="nw", pady=5, padx=10)
entry_descripcion = tk.Text(scrollable_frame, height=5, width=80, font=fuente)
entry_descripcion.grid(row=fila, column=1, pady=5, padx=10)

fila += 1

# Fila: Legajo, Total de legajos, Folios del legajo, Folios del expediente
fila_legajos = tk.Frame(scrollable_frame)
fila_legajos.grid(row=fila, column=0, columnspan=2, pady=10)

entry_legajo = tk.Entry(fila_legajos, font=fuente, width=15)
entry_total_legajos = tk.Entry(fila_legajos, font=fuente, width=15)
entry_folios_legajo = tk.Entry(fila_legajos, font=fuente, width=15)
entry_folios_expediente = tk.Entry(fila_legajos, font=fuente, width=15)

for label, widget in [("Legajo:", entry_legajo),
                      ("Total de legajos:", entry_total_legajos),
                      ("Folios del legajo:", entry_folios_legajo),
                      ("Folios del expediente:", entry_folios_expediente)]:
    tk.Label(fila_legajos, text=label, font=fuente).pack(side="left", padx=5)
    widget.pack(side="left", padx=5)

fila += 1

# Fila: Archivo de resguardo, Estantería, Caja
fila_ubicacion = tk.Frame(scrollable_frame)
fila_ubicacion.grid(row=fila, column=0, columnspan=2, pady=10)

entry_archivo = tk.Entry(fila_ubicacion, font=fuente, width=30)
entry_estanteria = tk.Entry(fila_ubicacion, font=fuente, width=15)
entry_caja = tk.Entry(fila_ubicacion, font=fuente, width=15)

for label, widget in [("Archivo de resguardo:", entry_archivo),
                      ("Estantería:", entry_estanteria),
                      ("Caja:", entry_caja)]:
    tk.Label(fila_ubicacion, text=label, font=fuente).pack(side="left", padx=5)
    widget.pack(side="left", padx=5)

fila += 1

# Sección: Clasificación institucional
tk.Label(scrollable_frame, text="Clasificación institucional", font=("Arial", 13, "bold")).grid(row=fila, column=0, columnspan=2, pady=(20, 5))
fila += 1

fila_clasificacion = tk.Frame(scrollable_frame)
fila_clasificacion.grid(row=fila, column=0, columnspan=2, pady=10)

entry_id_serie = tk.Entry(fila_clasificacion, font=fuente, width=10)
entry_id_dependencia = tk.Entry(fila_clasificacion, font=fuente, width=10)
entry_id_area = tk.Entry(fila_clasificacion, font=fuente, width=10)
entry_id_cdd = tk.Entry(fila_clasificacion, font=fuente, width=10)

for label, widget in [("ID Serie:", entry_id_serie),
                      ("ID Dependencia:", entry_id_dependencia),
                      ("ID Área:", entry_id_area),
                      ("ID CDD:", entry_id_cdd)]:
    tk.Label(fila_clasificacion, text=label, font=fuente).pack(side="left", padx=5)
    widget.pack(side="left", padx=5)

fila += 1

# Botones finales
botones_finales = tk.Frame(scrollable_frame)
botones_finales.grid(row=fila, column=0, columnspan=2, pady=20)

btn_guardar_cerrar = tk.Button(botones_finales, text="Guardar y cerrar", font=fuente,
                                bg="#81C784", fg="#000000", width=20,
                                command=lambda: guardar_expediente_accion("cerrar"))
btn_guardar_cerrar.pack(side="left", padx=10)

btn_siguiente = tk.Button(botones_finales, text="Siguiente", font=fuente,
                          bg="#AED581", fg="#000000", width=20,
                          command=lambda: guardar_expediente_accion("siguiente"))
btn_siguiente.pack(side="left", padx=10)

# Ejecutar ventana
ventana.mainloop()

