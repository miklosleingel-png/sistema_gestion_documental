from flask import Flask, render_template, request, redirect, session, make_response
from xhtml2pdf import pisa
from datetime import datetime
import psycopg2

# Función auxiliar para convertir HTML a PDF usando xhtml2pdf
def convertir_html_a_pdf(html_string):
    from io import BytesIO
    from xhtml2pdf import pisa
    resultado = BytesIO()
    pisa_status = pisa.CreatePDF(html_string, dest=resultado)
    if pisa_status.err:
        return None
    return resultado.getvalue()

app = Flask(__name__)
app.secret_key = "clave_segura_2025"

# 🔧 Configuración de conexión a PostgreSQL
DB_CONFIG = {
    "dbname": "Sistema de Gestión Documental",
    "user": "postgres",
    "password": "18brumario",
    "host": "localhost",
    "port": "5432"
}

# ---------------------- AUTENTICACIÓN ----------------------

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave = request.form["clave"]
        if usuario == "alejandro" and clave == "18brumario":
            session["usuario"] = usuario
            session["rol"] = "Administrador"
            session["unidad"] = "Archivo Central"
            return redirect("/menu")
        else:
            return render_template("login.html", error="Usuario o contraseña incorrectos")
    return render_template("login.html")

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")

# ---------------------- MENÚ PRINCIPAL ----------------------

@app.route("/menu")
def menu():
    return render_template("menu.html",
        usuario=session.get("usuario"),
        rol=session.get("rol"),
        unidad=session.get("unidad")
    )

# ---------------------- CAPTURA DE EXPEDIENTES ----------------------

@app.route("/captura_expediente", methods=["GET"])
def captura_expediente():
    return render_template("captura_expediente.html",
        usuario=session.get("usuario"),
        rol=session.get("rol"),
        unidad=session.get("unidad")
    )

@app.route("/guardar_expediente", methods=["POST"])
def guardar_expediente():
    datos = request.form.to_dict()
    datos["registrado_por"] = session.get("usuario")

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO inventario (
            clave_cgca, anio_apertura, fondo, numero,
            unidad_administrativa, area_generadora, descripcion_expediente,
            fecha_apertura, fecha_cierre, legajo, total_legajos,
            folios_legajo, folios_expediente, archivo,
            estanteria, caja, registrado_por
        ) VALUES (
            %(clave_cgca)s, %(anio_apertura)s, %(fondo)s, %(numero_expediente)s,
            %(unidad_administrativa)s, %(area_generadora)s, %(descripcion)s,
            %(fecha_apertura)s, %(fecha_cierre)s, %(legajo)s, %(total_legajos)s,
            %(folios_legajo)s, %(folios_expediente)s, %(archivo_resguardo)s,
            %(estanteria)s, %(caja)s, %(registrado_por)s
        )
    """, datos)
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/menu")

# ---------------------- CONSULTA DE INVENTARIO ----------------------

@app.route("/consulta_inventario", methods=["GET"])
def consulta_inventario():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Menús desplegables
    def obtener_distintos(campo):
        cur.execute(f"SELECT DISTINCT {campo} FROM inventario_expedientes ORDER BY {campo}")
        return [row[0] for row in cur.fetchall()]

    claves = obtener_distintos("clave_cgca")
    unidades = obtener_distintos("unidad_administrativa")
    areas = obtener_distintos("area_generadora")
    cajas = obtener_distintos("caja")
    usuarios = obtener_distintos("registrado_por")

    # Filtros
    filtros = []
    valores = {}
    campos = {
        "clave_cgca": "clave_cgca",
        "unidad_administrativa": "unidad_administrativa",
        "area_generadora": "area_generadora",
        "caja": "caja",
        "registrado_por": "registrado_por"
    }

    for campo, columna in campos.items():
        valor = request.args.get(campo)
        if valor:
            filtros.append(f"{columna} ILIKE %({campo})s")
            valores[campo] = f"%{valor}%"

    fecha_desde = request.args.get("fecha_desde")
    fecha_hasta = request.args.get("fecha_hasta")
    if fecha_desde:
        filtros.append("fecha_apertura >= %(fecha_desde)s")
        valores["fecha_desde"] = fecha_desde
    if fecha_hasta:
        filtros.append("fecha_cierre <= %(fecha_hasta)s")
        valores["fecha_hasta"] = fecha_hasta

    where_clause = "WHERE " + " AND ".join(filtros) if filtros else ""

    cur.execute(f"""
        SELECT clave_cgca, anio_apertura, fondo, numero,
               unidad_administrativa, area_generadora,
               descripcion_expediente, fecha_apertura, fecha_cierre,
               legajo, total_legajos, folios_legajo, folios_expediente,
               archivo, estanteria, caja
        FROM inventario_expedientes
        {where_clause}
        ORDER BY fecha_apertura DESC
    """, valores)
    expedientes = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("consulta_inventario.html",
        expedientes=expedientes,
        claves=claves,
        unidades=unidades,
        areas=areas,
        cajas=cajas,
        usuarios=usuarios
    )

# ---------------------- GENERACIÓN DE PDF ----------------------

@app.route("/generar_pdf", methods=["GET"])
def generar_pdf():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    filtros = []
    valores = {}
    filtros_visibles = []
    campos = {
        "clave_cgca": "clave_cgca",
        "unidad_administrativa": "unidad_administrativa",
        "area_generadora": "area_generadora",
        "caja": "caja",
        "registrado_por": "registrado_por"
    }

    for campo, columna in campos.items():
        valor = request.args.get(campo)
        if valor:
            filtros.append(f"{columna} ILIKE %({campo})s")
            valores[campo] = f"%{valor}%"
            filtros_visibles.append(f"{campo.replace('_', ' ').title()}: {valor}")

    fecha_desde = request.args.get("fecha_desde")
    fecha_hasta = request.args.get("fecha_hasta")
    if fecha_desde:
        filtros.append("fecha_apertura >= %(fecha_desde)s")
        valores["fecha_desde"] = fecha_desde
        filtros_visibles.append(f"Fecha desde: {fecha_desde}")
    if fecha_hasta:
        filtros.append("fecha_cierre <= %(fecha_hasta)s")
        valores["fecha_hasta"] = fecha_hasta
        filtros_visibles.append(f"Fecha hasta: {fecha_hasta}")

    where_clause = "WHERE " + " AND ".join(filtros) if filtros else ""

    cur.execute(f"""
        SELECT clave_cgca, anio_apertura, fondo, numero,
               unidad_administrativa, area_generadora,
               descripcion_expediente, fecha_apertura, fecha_cierre,
               legajo, total_legajos, folios_legajo, folios_expediente,
               archivo, estanteria, caja
        FROM inventario_expedientes
        {where_clause}
        ORDER BY fecha_apertura DESC
    """, valores)
    expedientes = cur.fetchall()
    cur.close()
    conn.close()

    unidad = request.args.get("unidad_administrativa", "")
    area = request.args.get("area_generadora", "")

    html_string = render_template("pdf_inventario.html",
        expedientes=expedientes,
        filtros=filtros_visibles,
        filtros_unidad=unidad,
        filtros_area=area,
        now=datetime.now()
    )

    pdf = convertir_html_a_pdf(html_string)
    if pdf is None:
        return "Error al generar el PDF"

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=inventario_expedientes.pdf"
    return response
if __name__ == "__main__":
    app.run(debug=True)