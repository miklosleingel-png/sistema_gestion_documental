# -*- coding: utf-8 -*-
import sys

# Validar argumento de usuario ANTES de importar tkinter
if len(sys.argv) < 2 or not sys.argv[1].strip():
    print("⚠️ No se recibió el nombre del usuario como argumento.")
    sys.exit()

# Obtener nombre de usuario desde argumentos
nombre_usuario = sys.argv[1].strip()

# Consultar rol y unidad administrativa desde la base de datos
import psycopg2

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

# Importar módulos de interfaz
import tkinter as tk
print("🧪 Tkinter default root:", tk._default_root)
tk.NoDefaultRoot()
from tkinter import ttk
from Modulos.encabezado_institucional import insertar_encabezado
from modulo_campos_expediente import crear_campos_expediente
from modulo_guardado_expediente import guardar_expediente

# Ruta base para imágenes
ruta_base = r"C:\Users\miklo\OneDrive\Documentos\Sistema de Gestión documental\Imagenes"

# Crear ventana principal
ventana = tk.Toplevel()
ventana.title("Captura de Expedientes")
ventana.state("zoomed")
ventana.configure(bg="#F5F5F5")

# Crear estilo para Combobox (después de crear la ventana)
estilo = ttk.Style()
estilo.configure("Estilo.TCombobox", font=("Arial", 12))

# Insertar encabezado institucional
insertar_encabezado(ventana, ruta_base, "Captura de Expedientes", nombre_usuario, rol_usuario, unidad_admin)

# Mensaje introductorio
tk.Label(ventana, text="Ahora puede capturar la descripción del expediente",
         font=("Arial", 14), bg="#F5F5F5", fg="#333333").pack(pady=(10, 0))

# Crear marco de contenido
contenido = tk.Frame(ventana, bg="#F5F5F5")
contenido.pack(padx=20, pady=10)

# Crear campos del expediente
campos = crear_campos_expediente(contenido)

# Crear botones de acción
botones_frame = tk.Frame(ventana, bg="#F5F5F5")
botones_frame.pack(pady=20)

btn_guardar_cerrar = tk.Button(botones_frame, text="Guardar y cerrar", font=("Arial", 12),
                                command=lambda: guardar_expediente(campos, nombre_usuario, "cerrar", ventana))
btn_guardar_cerrar.pack(side="left", padx=10)

btn_siguiente = tk.Button(botones_frame, text="Siguiente", font=("Arial", 12),
                          command=lambda: guardar_expediente(campos, nombre_usuario, "continuar", ventana))
btn_siguiente.pack(side="left", padx=10)

# Ejecutar ventana
ventana.mainloop()