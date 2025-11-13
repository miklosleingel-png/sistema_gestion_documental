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
ventana.configure(bg="#F5F5F5")

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
canvas = tk.Canvas(ventana, bg="#FFFFFF")
scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

scrollable_frame = tk.Frame(canvas, bg="#FFFFFF")
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Logos institucionales
logo_gobierno = tk.PhotoImage(file=r"C:\Users\miklo\OneDrive\Documentos\Sistema de Gestión documental\Imagenes\logo_gobierno.png").subsample(4, 4)
logo_archivos = tk.PhotoImage(file=r"C:\Users\miklo\OneDrive\Documentos\Sistema de Gestión documental\Imagenes\logo_archivos.png").subsample(8, 8)
logo_smadsot = tk.PhotoImage(file=r"C:\Users\miklo\OneDrive\Documentos\Sistema de Gestión documental\Imagenes\logo_smadsot.png").subsample(4, 4)

encabezado = tk.Frame(scrollable_frame)
encabezado.grid(row=0, column=0, columnspan=2, pady=10)
tk.Label(encabezado, image=logo_gobierno).pack(side="left", padx=10)
tk.Label(encabezado, image=logo_archivos).pack(side="left", padx=10)
tk.Label(encabezado, image=logo_smadsot).pack(side="left", padx=10)

ventana.logo_gobierno = logo_gobierno
ventana.logo_archivos = logo_archivos
ventana.logo_smadsot = logo_smadsot

# Leyenda institucional
fila = 1
tk.Label(scrollable_frame, text="Sistema de Gestión de Expedientes",
         font=("Arial", 18, "bold"), bg="#F5F5F5", fg="#2E7D32").grid(row=fila, column=0, columnspan=2, pady=(5, 0))
fila += 1
ttk.Separator(scrollable_frame, orient="horizontal").grid(row=fila, column=0, columnspan=2, sticky="ew", pady=(0, 20))
fila += 1

# Marcos de botones
captura_frame = tk.LabelFrame(scrollable_frame, text="Captura", font=("Arial", 14, "bold"),
                              bg="#F5F5F5", fg="#2E7D32", padx=10, pady=10)
visualizacion_frame = tk.LabelFrame(scrollable_frame, text="Visualización", font=("Arial", 14, "bold"),
                                    bg="#F5F5F5", fg="#2E7D32", padx=10, pady=10)
captura_frame.grid(row=fila, column=0, padx=20, sticky="n")
visualizacion_frame.grid(row=fila, column=1, padx=20, sticky="n")

# Función para abrir formularios
def abrir_formulario(nombre_archivo):
    subprocess.Popen(["python", nombre_archivo])

# Botones de captura
botones_captura = [
    ("Captura de expedientes", "inventario_formulario.py"),
    ("Captura de dependencias", "formulario_dependencias.py"),
    ("Captura de Áreas generadoras", "formulario_areas_generadoras.py"),
    ("Captura de Áreas Externas Relacionadas", "formulario_areas_externas.py"),
    ("Captura de funciones", "formulario_funciones.py"),
    ("Captura de procedimientos", "formulario_procedimientos.py"),
    ("Captura de funcionarios", "formulario_funcionarios.py")
]

for texto, archivo in botones_captura:
    btn = tk.Button(captura_frame, text=texto,
                    font=("Arial", 12), width=50, anchor="w",
                    bg="#A5D6A7", fg="#000000",
                    command=lambda a=archivo: abrir_formulario(a))
    btn.pack(pady=6)

# Botones de visualización
botones_visualizacion = [
    ("Visualización del Cuadro General de Clasificación Archivística", "visualizar_cgca.py"),
    ("Visualización del Catálogo de Disposición Documental", "visualizar_cdd.py"),
    ("Visualización de Fichas de Valoración Documental", "visualizar_valoracion.py"),
    ("Visualización del Inventario de expedientes por área", "visualizar_inventario_area.py"),
    ("Visualización del Inventario General", "visualizar_inventario_general.py"),
    ("Visualización de la Guía de Archivos", "visualizar_guia_archivos.py")
]

for texto, archivo in botones_visualizacion:
    btn = tk.Button(visualizacion_frame, text=texto,
                    font=("Arial", 12), width=50, anchor="w",
                    bg="#A5D6A7", fg="#000000",
                    command=lambda a=archivo: abrir_formulario(a))
    btn.pack(pady=6)

ventana.mainloop()