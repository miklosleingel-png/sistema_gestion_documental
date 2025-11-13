# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
import psycopg2
import hashlib
import unicodedata
import subprocess
import sys

# Conexión a la base de datos
try:
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="Sistema de Gestión Documental",
        user="postgres",
        password="18brumario"
    )
    print("✅ Conexión exitosa a la base de datos.")
except Exception as e:
    print("❌ Error al conectar:", e)
    messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos:\n{e}")
    exit()

# Función para verificar acceso
def iniciar_sesion():
    nombre = entry_nombre.get().strip()
    contraseña = entry_contraseña.get().strip()

    if not nombre or not contraseña:
        messagebox.showwarning("Campos incompletos", "Por favor, completa ambos campos.")
        return

    # Normaliza y encripta la contraseña ingresada
    contraseña_normalizada = unicodedata.normalize('NFKC', contraseña)
    contraseña_hash = hashlib.sha256(contraseña_normalizada.encode('utf-8')).hexdigest()

    try:
        cursor = conn.cursor()
        cursor.execute("""
             SELECT rol, unidad_admin FROM usuarios
             WHERE nombre_usuario = %s AND contraseña_hash = %s
        """, (nombre, contraseña_hash))
        resultado = cursor.fetchone()
        cursor.close()

        if resultado:
            rol = resultado[0]
            unidad = resultado[1]

            print(f"✅ Acceso concedido a '{nombre}' con rol '{rol}'.")
            messagebox.showinfo("Bienvenido", f"Acceso concedido a '{nombre}'\nRol: {rol}")

            # Abrir formulario principal y pasar el nombre como argumento
            try:
                ruta_principal = r"C:\Users\miklo\OneDrive\Documentos\Sistema de Gestión documental\Scripts\formulario_principal.py"
                print("🟢 Ejecutando:", ruta_principal)

                ruta_python = sys.executable
                if "WindowsApps" in ruta_python or not ruta_python.lower().endswith("python.exe"):
                    ruta_python = r"C:\Users\miklo\AppData\Local\Programs\Python\Python312\python.exe"

                subprocess.Popen([ruta_python, ruta_principal, nombre])
                ventana.destroy()

            except Exception as e:
                print("❌ Error al abrir el formulario principal:", e)
                messagebox.showerror("Error", f"No se pudo abrir el formulario principal:\n{e}")
        else:
            print("❌ Credenciales incorrectas.")
            messagebox.showerror("Acceso denegado", "Nombre de usuario o contraseña incorrectos.")

    except Exception as e:
        print("❌ Error al verificar acceso:", e)
        messagebox.showerror("Error", f"Ocurrió un error:\n{e}")

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Acceso al Sistema")
ventana.configure(bg="#F5F5F5")
ventana.geometry("400x200")

tk.Label(ventana, text="Nombre de usuario:", font=("Arial", 11), bg="#F5F5F5").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_nombre = tk.Entry(ventana, font=("Arial", 11))
entry_nombre.grid(row=0, column=1, padx=10, pady=10)

tk.Label(ventana, text="Contraseña:", font=("Arial", 11), bg="#F5F5F5").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_contraseña = tk.Entry(ventana, font=("Arial", 11), show="*")
entry_contraseña.grid(row=1, column=1, padx=10, pady=10)

btn_acceder = tk.Button(ventana, text="Iniciar sesión", font=("Arial", 11),
                        bg="#81D4FA", fg="#000000", width=20,
                        command=iniciar_sesion)
btn_acceder.grid(row=2, column=0, columnspan=2, pady=20)

ventana.mainloop()
