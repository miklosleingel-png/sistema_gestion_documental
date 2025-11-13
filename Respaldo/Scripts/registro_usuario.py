# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
import psycopg2
from datetime import date
import hashlib
import unicodedata

# Intentar conectar a la base de datos
try:
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="Sistema de Gestión Documental",
        user="postgres",
        password="18brumario"
    )
    print("✅ Conexión exitosa a la base de datos.")
except psycopg2.OperationalError as e:
    print("❌ Error de conexión con PostgreSQL:")
    print(e)
    messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos:\n{e}")
    exit()
except Exception as e:
    print("❌ Error inesperado al conectar:")
    print(e)
    messagebox.showerror("Error inesperado", f"Ocurrió un error:\n{e}")
    exit()

# Función para registrar usuario
def registrar_usuario():
    nombre = entry_nombre.get().strip()
    contraseña = entry_contraseña.get().strip()
    rol = entry_rol.get().strip()
    fecha = date.today()

    if not nombre or not contraseña or not rol:
        messagebox.showwarning("Campos incompletos", "Por favor, completa todos los campos.")
        return

    # Normaliza y encripta la contraseña
    contraseña_normalizada = unicodedata.normalize('NFKC', contraseña)
    contraseña_hash = hashlib.sha256(contraseña_normalizada.encode('utf-8')).hexdigest()

    try:
        cursor = conn.cursor()

        # Verifica si el usuario ya existe
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE nombre_usuario = %s", (nombre,))
        existe = cursor.fetchone()[0]
        if existe > 0:
            messagebox.showerror("Error", f"El usuario '{nombre}' ya está registrado.")
            cursor.close()
            return

        # Inserta el nuevo usuario con columnas correctas
        cursor.execute("""
            INSERT INTO usuarios (nombre_usuario, contraseña_hash, rol, fecha_registro)
            VALUES (%s, %s, %s, %s)
        """, (nombre, contraseña_hash, rol, fecha))
        conn.commit()
        cursor.close()

        print(f"✅ Usuario '{nombre}' registrado correctamente.")
        messagebox.showinfo("Éxito", f"Usuario '{nombre}' registrado correctamente.")

    except psycopg2.Error as e:
        conn.rollback()
        print("❌ Error al registrar usuario:", e)
        messagebox.showerror("Error de base de datos", f"No se pudo registrar el usuario:\n{e}")
    except Exception as e:
        conn.rollback()
        print("❌ Error inesperado:", e)
        messagebox.showerror("Error inesperado", f"Ocurrió un error:\n{e}")

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Registro de Usuario")

tk.Label(ventana, text="Nombre:").grid(row=0, column=0)
entry_nombre = tk.Entry(ventana)
entry_nombre.grid(row=0, column=1)

tk.Label(ventana, text="Contraseña:").grid(row=1, column=0)
entry_contraseña = tk.Entry(ventana)  # ← sin show="*"
entry_contraseña.grid(row=1, column=1)

tk.Label(ventana, text="Rol:").grid(row=2, column=0)
entry_rol = tk.Entry(ventana)
entry_rol.grid(row=2, column=1)

btn_registrar = tk.Button(ventana, text="Registrar", command=registrar_usuario)
btn_registrar.grid(row=3, column=0, columnspan=2)

ventana.mainloop()