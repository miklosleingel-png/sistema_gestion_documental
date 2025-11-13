import tkinter as tk
from tkinter import messagebox
import psycopg2
from datetime import date

# Conexión a la base de datos
def conectar_bd():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="Sistema de Gestión Documental",
        user="postgres",
        password="18brumario"
    )

# Función para insertar en la base de datos
def insertar_dependencia(siglas, nombre, registrado_por):
    fecha_actual = date.today()
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO dependencia (siglas_dependencia, nombre_dependencia, registrado_por, fecha_registro, fecha_modificacion)
        VALUES (%s, %s, %s, %s, %s)
    """, (siglas, nombre, registrado_por, fecha_actual, fecha_actual))
    conn.commit()
    conn.close()

# Validación y acción
def validar_y_guardar(accion):
    siglas = entry_siglas.get().strip()
    nombre = entry_nombre.get().strip()
    registrado_por = entry_registrado_por.get().strip()

    if not siglas or not nombre or not registrado_por:
        messagebox.showwarning("Campos incompletos", "Por favor completa los campos obligatorios.")
        return

    try:
        insertar_dependencia(siglas, nombre, registrado_por)
        if accion == "cerrar":
            messagebox.showinfo("Éxito", "Dependencia registrada correctamente.")
            ventana.destroy()
        elif accion == "siguiente":
            messagebox.showinfo("Éxito", "Dependencia registrada. Puedes ingresar otra.")
            limpiar_campos()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar la dependencia:\n{e}")

# Limpiar campos
def limpiar_campos():
    entry_siglas.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_registrado_por.delete(0, tk.END)
    entry_siglas.focus()

# Ventana principal
ventana = tk.Tk()
ventana.title("Captura de Dependencia")
ventana.geometry("600x480")
ventana.configure(bg="#F5F5F5")

# Cargar logos institucionales
try:
    logo_gobierno = tk.PhotoImage(file="Imagenes/logo_gobierno.png").subsample(4, 4)
    logo_archivos = tk.PhotoImage(file="Imagenes/logo_archivos.png").subsample(8, 8)
    logo_smadsot = tk.PhotoImage(file="Imagenes/logo_smadsot.png").subsample(4, 4)
except Exception as e:
    logo_gobierno = logo_archivos = logo_smadsot = None
    print(f"Error al cargar imágenes: {e}")

# Encabezado con logos
encabezado = tk.Frame(ventana, bg="#F5F5F5")
encabezado.pack(pady=10)

if logo_gobierno:
    tk.Label(encabezado, image=logo_gobierno, bg="#F5F5F5").pack(side="left", padx=10)
if logo_archivos:
    tk.Label(encabezado, image=logo_archivos, bg="#F5F5F5").pack(side="left", padx=10)
if logo_smadsot:
    tk.Label(encabezado, image=logo_smadsot, bg="#F5F5F5").pack(side="left", padx=10)

# Evitar que se borren las imágenes
ventana.logo_gobierno = logo_gobierno
ventana.logo_archivos = logo_archivos
ventana.logo_smadsot = logo_smadsot

# Título
tk.Label(ventana, text="Registro de Dependencia", font=("Arial", 16, "bold"),
         bg="#F5F5F5", fg="#2E7D32").pack(pady=10)

# Marco de formulario
formulario = tk.Frame(ventana, bg="#F5F5F5")
formulario.pack(pady=10)

# Campo: Siglas
tk.Label(formulario, text="Siglas *", font=("Arial", 12),
         bg="#F5F5F5").grid(row=0, column=0, sticky="e", padx=10, pady=5)
entry_siglas = tk.Entry(formulario, font=("Arial", 12), width=40)
entry_siglas.grid(row=0, column=1, padx=10, pady=5)

# Campo: Nombre
tk.Label(formulario, text="Nombre de la dependencia *", font=("Arial", 12),
         bg="#F5F5F5").grid(row=1, column=0, sticky="e", padx=10, pady=5)
entry_nombre = tk.Entry(formulario, font=("Arial", 12), width=40)
entry_nombre.grid(row=1, column=1, padx=10, pady=5)

# Campo: Registrado por
tk.Label(formulario, text="Registrado por *", font=("Arial", 12),
         bg="#F5F5F5").grid(row=2, column=0, sticky="e", padx=10, pady=5)
entry_registrado_por = tk.Entry(formulario, font=("Arial", 12), width=40)
entry_registrado_por.grid(row=2, column=1, padx=10, pady=5)

# Botones
botones = tk.Frame(ventana, bg="#F5F5F5")
botones.pack(pady=20)

btn_guardar_cerrar = tk.Button(botones, text="Guardar y cerrar", font=("Arial", 12),
                               bg="#81C784", fg="#000000", width=18,
                               command=lambda: validar_y_guardar("cerrar"))
btn_guardar_cerrar.grid(row=0, column=0, padx=10)

btn_siguiente = tk.Button(botones, text="Siguiente", font=("Arial", 12),
                          bg="#AED581", fg="#000000", width=18,
                          command=lambda: validar_y_guardar("siguiente"))
btn_siguiente.grid(row=0, column=1, padx=10)

ventana.mainloop()