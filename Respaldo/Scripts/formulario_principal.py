# Formulario Principal

# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # ✅ Corrección
import subprocess  # ✅ Corrección
from Modulos.encabezado_institucional import insertar_encabezado
import psycopg2
import sys

# Capturar nombre del usuario desde argumentos
nombre_usuario = sys.argv[1] if len(sys.argv) > 1 else ""

# Consultar rol y unidad administrativa desde la base de datos
rol_usuario = ""
unidad_admin = ""

try:
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="Sistema de Gestión Documental",
        user="postgres",
        password="18brumario"
    )
    cursor = conn.cursor()
    cursor.execute("""
        SELECT rol, unidad_admin FROM usuarios
        WHERE nombre_usuario = %s
    """, (nombre_usuario,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()

    if resultado:
        rol_usuario = resultado[0]
        unidad_admin = resultado[1]
    else:
        print("⚠️ Usuario no encontrado en la base de datos.")

except Exception as e:
    print("❌ Error al obtener datos del usuario:", e)

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Gestión Documental")
ventana.state("zoomed")
ventana.configure(bg="#F5F5F5")

# Ruta de los logos institucionales
ruta_base = r"C:\Users\miklo\OneDrive\Documentos\Sistema de Gestión documental\Imagenes"

# Encabezado institucional con saludo personalizado
insertar_encabezado(ventana, ruta_base, "Sistema de Gestión Documental", nombre_usuario, rol_usuario, unidad_admin)

# Línea de separación adicional debajo del título
ttk.Separator(ventana, orient="horizontal").pack(fill="x", padx=20, pady=(0, 10))

# -------------------------------------------------------------------------
# 🔽 Carga de íconos para los botones

from tkinter import PhotoImage

def cargar_icono(nombre, escala=12):
    try:
        return PhotoImage(file=f"{ruta_base}\\{nombre}").subsample(escala, escala)
    except:
        return None

iconos = {
    "expedientes": cargar_icono("01icon_expedientes.png"),
    "dependencias": cargar_icono("02icon_dependencias.png"),
    "areas_generadoras": cargar_icono("03icon_areas.png"),
    "areas_externas": cargar_icono("04icon_externas.png"),
    "funciones": cargar_icono("05icon_funciones.png"),
    "procedimientos": cargar_icono("06icon_procedimientos.png"),
    "funcionarios": cargar_icono("07icon_funcionarios.png"),
    "guia": cargar_icono("13icon_guia.png"),
    "inv_general": cargar_icono("12icon_inventario.png"),
    "inv_area": cargar_icono("11icon_inv_area.png"),
    "cdd": cargar_icono("09icon_cdd.png"),
    "cgca": cargar_icono("08icon_cgca.png"),
    "valoracion": cargar_icono("10icon_valoración.png")
}

#--------------------------------------------------------------------------
# Línea de separación adicional debajo del título
ttk.Separator(ventana, orient="horizontal").pack(fill="x", padx=20, pady=(0, 10))

# Contenido principal
contenido = tk.Frame(ventana, bg="#F5F5F5")
contenido.pack(pady=50)

tk.Label(contenido, text="Bienvenido al sistema", font=("Arial", 14), bg="#F5F5F5").pack(pady=10)

# -------------------------------------------------------------------------
# 🔽 Función para abrir formularios desde los botones

def abrir_formulario(nombre_archivo):
    ruta = rf"C:\Users\miklo\OneDrive\Documentos\Sistema de Gestión documental\Scripts\{nombre_archivo}"
    try:
        subprocess.Popen([r"C:\Users\miklo\AppData\Local\Programs\Python\Python312\python.exe", ruta, nombre_usuario])
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el formulario:\n{e}")
# -------------------------------------------------------------------------
# 🔽 Botones para abrir formularios de captura

captura_frame = tk.Frame(contenido, bg="#F5F5F5")
captura_frame.pack(pady=10)

botones_captura = [
    ("Captura de Expedientes", "captura_expedientes.py", iconos["expedientes"]),
    ("Captura de Dependencias", "captura_dependencias.py", iconos["dependencias"]),
    ("Captura de Áreas Generadoras", "captura_areas_generadoras.py", iconos["areas_generadoras"]),
    ("Captura de Áreas Externas", "captura_areas_externas.py", iconos["areas_externas"]),
    ("Captura de Funciones", "captura_funciones.py", iconos["funciones"]),
    ("Captura de Procedimientos", "captura_procedimientos.py", iconos["procedimientos"]),
    ("Captura de Funcionarios", "captura_funcionarios.py", iconos["funcionarios"])
]

for i, (texto, archivo, icono) in enumerate(botones_captura):
    fila = i // 4
    columna = i % 4
    btn = tk.Button(captura_frame, text=texto, font=("Arial", 11), image=icono,
                    compound="left", bg="#AED581", fg="#000000", width=250,
                    anchor="w", padx=10,
                    command=lambda a=archivo: abrir_formulario(a))
    btn.grid(row=fila, column=columna, padx=10, pady=5)

# -------------------------------------------------------------------------
# 🔽 Botones para abrir formularios de visualización

visual_frame = tk.Frame(contenido, bg="#F5F5F5")
visual_frame.pack(pady=10)

botones_visualizacion = [
    ("Vista Guía de Archivo", "vista_guia_arch.py", iconos["guia"]),
    ("Inventario General", "vista_inv_general.py", iconos["inv_general"]),
    ("Inventario por Área", "vista_inv_por_area.py", iconos["inv_area"]),
    ("Vista CDD", "vista_CDD.py", iconos["cdd"]),
    ("Vista CGCA", "vista_CGCA.py", iconos["cgca"]),
    ("Vista Fichas de Valor", "vista_fichas_valor.py", iconos["valoracion"])
]

for i, (texto, archivo, icono) in enumerate(botones_visualizacion):
    fila = i // 4
    columna = i % 4
    btn = tk.Button(visual_frame, text=texto, font=("Arial", 11), image=icono,
                    compound="left", bg="#81D4FA", fg="#000000", width=250,
                    anchor="w", padx=10,
                    command=lambda a=archivo: abrir_formulario(a))
    btn.grid(row=fila, column=columna, padx=10, pady=5)


# -------------------------------------------------------------------------
# 🔽 Otros módulos, configuraciones o el botón de salida

btn_salir = tk.Button(contenido, text="Salir", font=("Arial", 12),
                      bg="#EF9A9A", fg="#000000", width=30,
                      command=ventana.destroy)
btn_salir.pack(pady=30)

firma = tk.Label(ventana,
                 text="© Diseñado y programado por Manuel Alejandro Hernández Maimone",
                 font=("Arial", 6), bg="#F5F5F5", anchor="e", justify="right")
firma.pack(side="bottom", fill="x", padx=10, pady=5)

# Ejecutar ventana
ventana.mainloop()