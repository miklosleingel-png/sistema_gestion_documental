from tkinter import messagebox
from Modulos.conexion_bd import conectar_bd
import tkinter as tk
from tkinter import ttk

def guardar_expediente(campos, nombre_usuario, accion, ventana):
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO inventario (
                clave_cgca, anio_apertura, fondo, numero,
                unidad_administrativa, area_generadora,
                descripcion_expediente, fecha_apertura, fecha_cierre,
                legajo, total_legajos, folios_legajo, folios_expediente,
                archivo, estanteria, caja,
                registrado_por
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            campos["combo_clave"].get(),
            int(campos["entry_anio"].get()) if campos["entry_anio"].get().isdigit() else None,
            campos["combo_fondo"].get(),
            campos["entry_numero"].get(),
            campos["combo_unidad"].get(),
            campos["combo_area"].get(),
            campos["entry_descripcion"].get("1.0", "end").strip(),
            campos["entry_fecha_apertura"].get_date(),
            campos["entry_fecha_cierre"].get_date(),
            campos["entry_legajo"].get(),
            int(campos["entry_total_legajos"].get()) if campos["entry_total_legajos"].get().isdigit() else None,
            int(campos["entry_folios_legajo"].get()) if campos["entry_folios_legajo"].get().isdigit() else None,
            int(campos["entry_folios_expediente"].get()) if campos["entry_folios_expediente"].get().isdigit() else None,
            campos["entry_archivo"].get(),
            campos["entry_estanteria"].get(),
            campos["entry_caja"].get(),
            nombre_usuario
        ))
        conn.commit()
        cursor.close()
        conn.close()

        if accion == "cerrar":
            messagebox.showinfo("Éxito", "Expediente guardado correctamente.")
            ventana.destroy()
        else:
            messagebox.showinfo("Éxito", "Expediente guardado. Puedes capturar otro.")
            for campo in campos.values():
                if isinstance(campo, tk.Entry):
                    campo.delete(0, tk.END)
                elif isinstance(campo, tk.Text):
                    campo.delete("1.0", tk.END)
                elif isinstance(campo, ttk.Combobox):
                    campo.set("")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar:\n{e}")