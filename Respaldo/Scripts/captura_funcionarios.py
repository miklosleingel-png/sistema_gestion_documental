#Captura de funcionarios

import tkinter as tk
from tkinter import ttk, messagebox
from Modulos.encabezado_institucional import insertar_encabezado
from Modulos.conexion_bd import conectar_bd

# Crear ventana
ventana = tk.Tk()
ventana.title("Formulario de Captura")
ventana.state("zoomed")  # Pantalla completa
ventana.configure(bg="#F5F5F5")

# Encabezado institucional
ruta_base = r"C:\Users\miklo\OneDrive\Documentos\Sistema de Gestión documental\Imagenes"
insertar_encabezado(ventana, ruta_base, "Captura de funcionarios")

# -------------------------------------------------------------------------
# 🔽 Aquí puedes insertar los campos del formulario

contenido = tk.Frame(ventana, bg="#F5F5F5")
contenido.pack(pady=20)

tk.Label(contenido, text="Campo de ejemplo:", font=("Arial", 12), bg="#F5F5F5").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entrada_ejemplo = tk.Entry(contenido, width=50)
entrada_ejemplo.grid(row=0, column=1, padx=10, pady=5)

# -------------------------------------------------------------------------
# 🔽 Aquí defines la función para guardar los datos en PostgreSQL

def guardar_datos():
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        valor = entrada_ejemplo.get()
        cursor.execute("INSERT INTO tabla_ejemplo (campo) VALUES (%s)", (valor,))
        conn.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()

# -------------------------------------------------------------------------
# 🔽 Aquí defines la función para limpiar los campos del formulario

def limpiar_campos():
    entrada_ejemplo.delete(0, tk.END)

# -------------------------------------------------------------------------
# 🔽 Aquí agregas los botones “Guardar y cerrar” y “Siguiente”

botones = tk.Frame(ventana, bg="#F5F5F5")
botones.pack(pady=30)

def guardar_y_cerrar():
    try:
        guardar_datos()
        messagebox.showinfo("Éxito", "Registro guardado correctamente.")
        ventana.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

def guardar_y_continuar():
    try:
        guardar_datos()
        messagebox.showinfo("Éxito", "Registro guardado. Puedes capturar otro.")
        limpiar_campos()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

btn_guardar_cerrar = tk.Button(botones, text="Guardar y cerrar", font=("Arial", 12),
                               bg="#81C784", fg="#000000", width=18,
                               command=guardar_y_cerrar)
btn_guardar_cerrar.pack(side="left", padx=10)

btn_siguiente = tk.Button(botones, text="Siguiente", font=("Arial", 12),
                          bg="#AED581", fg="#000000", width=18,
                          command=guardar_y_continuar)
btn_siguiente.pack(side="left", padx=10)

# Ejecutar ventana
ventana.mainloop()