#Visualización de Fichas de Valoración

import tkinter as tk
from tkinter import ttk, messagebox
from Modulos.encabezado_institucional import insertar_encabezado
from Modulos.conexion_bd import conectar_bd
import subprocess  # Para abrir otro formulario

# Crear ventana
ventana = tk.Tk()
ventana.title("Visualización de Registros")
ventana.state("zoomed")
ventana.configure(bg="#F5F5F5")

# Encabezado institucional
ruta_base = r"C:\Users\miklo\OneDrive\Documentos\Sistema de Gestión documental\Imagenes"
insertar_encabezado(ventana, ruta_base, "Ficha de Valoración documental")

# -------------------------------------------------------------------------
# 🔽 Aquí se carga la tabla con los datos desde PostgreSQL

tabla = ttk.Treeview(ventana, columns=("col1", "col2", "col3"), show="headings")
tabla.heading("col1", text="Campo 1")
tabla.heading("col2", text="Campo 2")
tabla.heading("col3", text="Campo 3")
tabla.pack(padx=20, pady=20, fill="both", expand=True)

def cargar_datos():
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT campo1, campo2, campo3 FROM tabla_ejemplo")
        registros = cursor.fetchall()
        for fila in registros:
            tabla.insert("", "end", values=fila)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la información:\n{e}")
    finally:
        cursor.close()
        conn.close()

cargar_datos()

# -------------------------------------------------------------------------
# 🔽 Aquí se definen los botones: modificar, imprimir, cerrar

botones = tk.Frame(ventana, bg="#F5F5F5")
botones.pack(pady=20)

def abrir_modificacion():
    try:
        subprocess.Popen(["python", "formulario_modificacion.py"])
        ventana.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el formulario de modificación:\n{e}")

def imprimir_pdf():
    try:
        # Aquí se insertará la lógica para generar PDF
        messagebox.showinfo("PDF", "Generación de PDF en desarrollo.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el PDF:\n{e}")

def cerrar_ventana():
    ventana.destroy()

btn_modificar = tk.Button(botones, text="Modificar", font=("Arial", 12),
                          bg="#FFF176", fg="#000000", width=18,
                          command=abrir_modificacion)
btn_modificar.pack(side="left", padx=10)

btn_imprimir = tk.Button(botones, text="Imprimir", font=("Arial", 12),
                         bg="#81D4FA", fg="#000000", width=18,
                         command=imprimir_pdf)
btn_imprimir.pack(side="left", padx=10)

btn_cerrar = tk.Button(botones, text="Cerrar", font=("Arial", 12),
                       bg="#EF9A9A", fg="#000000", width=18,
                       command=cerrar_ventana)
btn_cerrar.pack(side="left", padx=10)

# Ejecutar ventana
ventana.mainloop()