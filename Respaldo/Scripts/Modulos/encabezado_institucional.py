# -*- coding: utf-8 -*-
import tkinter as tk

def insertar_encabezado(ventana, ruta_base, titulo, nombre="", rol="", unidad=""):
    # Crear marco del encabezado
    encabezado_frame = tk.Frame(ventana, bg="#ffffff")
    encabezado_frame.pack(fill="x", padx=20, pady=10)

    # Cargar logos institucionales dentro del contexto activo
    try:
        logo1 = tk.PhotoImage(master=ventana, file=f"{ruta_base}\\logo_smadsot.png").subsample(4, 4)
        logo2 = tk.PhotoImage(master=ventana, file=f"{ruta_base}\\logo_archivos.png").subsample(6, 6)
        logo3 = tk.PhotoImage(master=ventana, file=f"{ruta_base}\\logo_gobierno.png").subsample(4, 4)
    except Exception as e:
        print("❌ Error al cargar logos:", e)
        logo1 = logo2 = logo3 = None

    # Mostrar logos y mantener referencias vivas
    if logo1:
        label1 = tk.Label(encabezado_frame, image=logo1, bg="#ffffff")
        label1.image = logo1
        label1.pack(side="left", padx=10)

    if logo2:
        label2 = tk.Label(encabezado_frame, image=logo2, bg="#ffffff")
        label2.image = logo2
        label2.pack(side="left", padx=10)

    if logo3:
        label3 = tk.Label(encabezado_frame, image=logo3, bg="#ffffff")
        label3.image = logo3
        label3.pack(side="left", padx=10)

    # Título institucional
    tk.Label(encabezado_frame, text=titulo, font=("Arial", 12, "bold"),
             bg="#ffffff", fg="#333333").pack(side="left", padx=20)

    # Saludo personalizado
    saludo = ""
    if nombre:
        saludo += f"Bienvenid@ {nombre}"
    if rol:
        saludo += f"\nRol: {rol}"
    if unidad:
        saludo += f"\nUnidad: {unidad}"

    if saludo:
        tk.Label(encabezado_frame, text=saludo, font=("Arial", 12),
                 bg="#ffffff", fg="#555555", justify="right", anchor="e").pack(side="right", padx=10)

    # Mantener referencias vivas en el frame
    encabezado_frame.logo1 = logo1
    encabezado_frame.logo2 = logo2
    encabezado_frame.logo3 = logo3