from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timezone, date 
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from . import db
from .models import (
    Usuario, Rol, 
    CatCGCA, CatDependencia, CatUnidadesAdministrativas, 
    CatAreasProductoras, CatFuncionarios, CatFunciones, 
    CatLeyes, CatArchivo, CatAreasExternas, 
    CatSoporteDocumental, CatProcedimientos, CatActividades, 
    EnlaceArchivo, CatClaveCGCA, ClaveCGCAFunciones, 
    ClaveCGCAAreaProd, ClaveCGCAAreaRel, ClaveCGCAFundamentos, 
    ClaveCGCAProcedimientos, ClaveCGCASoporte, ClaveCGCAResponsable, 
    ClaveCGCAArchivo, ClaveCGCAAcceso, ClaveCGCAFechas, 
    CondicionAcceso, Expediente, ClaveCGCACDD,
    GuiaSoporteVinculo, ClaveCGCAGuia
)

main = Blueprint('main', __name__)

@main.app_context_processor
def inject_now():
    from datetime import datetime
    return {'now': datetime.now}

# -------------------------- 
# RUTA DE LOGIN (ACCESO) ---
#---------------------------
@main.route('/')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('main/login.html')

@main.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = Usuario.query.filter_by(username=username).first()

    if not user or user.password.strip() != password.strip():
        flash('Usuario o contraseña incorrectos.')
        return redirect(url_for('main.login'))

    if not user.activo:
        flash('Esta cuenta está desactivada.')
        return redirect(url_for('main.login'))

    user.ultimo_acceso = datetime.now(timezone.utc)
    db.session.commit()
    login_user(user)
    return redirect(url_for('main.dashboard'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre').upper()
        u_name = request.form.get('username').lower()
        email = request.form.get('email').lower()
        passw = request.form.get('password')

        if Usuario.query.filter((Usuario.username == u_name) | (Usuario.correo == email)).first():
            flash('El usuario o el correo ya están registrados.', 'danger')
            return redirect(url_for('main.register'))

        nuevo = Usuario(
            username=u_name,
            nombre_completo=nombre,
            correo=email,
            password=passw,
            role_id=1,
            activo=True  
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Registro exitoso. Usa tu nombre de usuario para entrar.', 'success')
        
        return redirect(url_for('main.login'))

    return render_template('main/register.html')

# ------------------ 
# --- Navegación ---
#-------------------
@main.route('/dashboard')
@login_required
def dashboard():
    """Esta es la función principal que carga el menú de catálogos."""
    return render_template('main/menu.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


# ------------------------------------------------ 
# --- SECCIÓN: EXPEDIENTES (CAPTURA Y EDICIÓN) ---
#-------------------------------------------------
@main.route('/cap_expedientes')
@login_required
def cap_expedientes():
    # Agregamos la consulta de archivos para el dropdown del formulario
    archivos = CatArchivo.query.all()
    expedientes = Expediente.query.order_by(Expediente.id_expediente.desc()).all()
    return render_template('main/cap_expedientes.html', 
                           expedientes=expedientes, 
                           archivos=archivos) # <-- Importante

@main.route('/guardar_expediente', methods=['POST'])
@login_required
def guardar_expediente():
    def limpiar_fecha(f): 
        return datetime.strptime(f, '%Y-%m-%d').date() if f else None
    
    def limpiar_int(v): 
        try:
            return int(v) if v and str(v).strip() != "" else 0
        except ValueError:
            return 0

    clave_texto = request.form.get('clave_cgca').strip()
    
    # BUSQUEDA EN TABLA MAESTRA: Obtenemos el ID correspondiente a la máscara
    maestra = CatClaveCGCA.query.filter_by(clave_cgca=clave_texto).first()

    if not maestra:
        flash(f'La clave {clave_texto} no existe en el catálogo maestro. Regístrala primero.', 'danger')
        return redirect(url_for('main.cap_expedientes'))

    try:
        nuevo_exp = Expediente(
            id_cgca=maestra.id_cgca,  # <-- Guardamos el ID numérico
            clave_cgca=clave_texto,    # <-- Guardamos la máscara para visualización rápida
            descripcion=request.form.get('descripcion'),
            fecha_inicio=limpiar_fecha(request.form.get('fecha_inicio')),
            fecha_final=limpiar_fecha(request.form.get('fecha_final')),
            fojas_expediente=limpiar_int(request.form.get('fojas_expediente')),
            fojas_legajo=limpiar_int(request.form.get('fojas_legajo')),
            legajo=limpiar_int(request.form.get('legajo')),
            total_legajos=limpiar_int(request.form.get('total_legajos')),
            id_archivo=limpiar_int(request.form.get('id_archivo')),
            estanteria=request.form.get('estanteria'),
            cbox=request.form.get('caja')
        )
        db.session.add(nuevo_exp)
        db.session.commit()
        flash('Expediente guardado con éxito.')
    except Exception as e:
        db.session.rollback()
        print(f"DEBUG: Error: {e}")
        flash(f'Error al guardar: {e}')
    
    if request.form.get('accion') == 'otro':
        return redirect(url_for('main.cap_expedientes'))
    return redirect(url_for('main.dashboard'))

@main.route('/editar_expediente/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_expediente(id):
    exp = Expediente.query.get_or_404(id)
    archivos = CatArchivo.query.all()
    
    if request.method == 'POST':
        clave_texto = request.form.get('clave_cgca').strip()
        maestra = CatClaveCGCA.query.filter_by(clave_cgca=clave_texto).first()

        if not maestra:
            flash(f'Clave {clave_texto} no válida.', 'danger')
            return redirect(url_for('main.editar_expediente', id=id))

        try:
            exp.id_cgca = maestra.id_cgca # Actualizamos el ID
            exp.clave_cgca = clave_texto   # Actualizamos la máscara
            exp.descripcion = request.form.get('descripcion')
            # ... (el resto de tus limpiadores de fecha e int igual que antes) ...
            db.session.commit()
            return redirect(url_for('main.cap_expedientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}')
    return render_template('main/editar_expediente.html', exp=exp, archivos=archivos)

# --- SECCIÓN: CATÁLOGO CGCA (ADMINISTRACIÓN) ---
@main.route('/cat_cgca')
@login_required
def cat_cgca():
    catalogos = CatCGCA.query.order_by(
        CatCGCA.funcion_clave.asc(),
        CatCGCA.seccion_clave.asc(),
        CatCGCA.subseccion_clave.asc(),
        CatCGCA.serie_clave.asc(),
        CatCGCA.subserie_clave.asc()
    ).all()
    
    return render_template('main/cat_cgca.html', catalogos=catalogos)

@main.route('/guardar_cgca', methods=['POST'])
@login_required
def guardar_cgca():
    # 1. Extraer datos del formulario (usando los 'name' de tu HTML)
    s_clave = request.form.get('seccion_clave', '').strip()
    f_clave = request.form.get('funcion_clave', '').strip().upper()
    s_nombre = request.form.get('seccion_nombre', '').strip()
    c_final = request.form.get('clave_cgca', '').strip().upper()

    # 2. Verificar si ya existe la serie
    registro = CatCGCA.query.filter_by(clave_cgca=c_final).first()

    if registro:
        # ACTUALIZAR
        registro.seccion_clave = s_clave
        registro.funcion_clave = f_clave
        registro.seccion_nombre = s_nombre
        # ... actualizar los demás campos ...
        mensaje = 'Registro actualizado.'
    else:
        # CREAR NUEVO
        registro = CatCGCA(
            seccion_clave=s_clave,
            funcion_clave=f_clave,
            seccion_nombre=s_nombre,
            subseccion_clave=request.form.get('subseccion_clave'),
            subseccion_nombre=request.form.get('subseccion_nombre'),
            serie_clave=request.form.get('serie_clave'),
            serie_nombre=request.form.get('serie_nombre'),
            subserie_clave=request.form.get('subserie_clave'),
            subserie_nombre=request.form.get('subserie_nombre'),
            clave_cgca=c_final,
            descripcion=request.form.get('descripcion'),
            observaciones=request.form.get('observaciones')
        )
        db.session.add(registro)
        db.session.flush() # Genera el ID para la tabla maestra

        # 3. SINCRONIZAR CON TABLA MAESTRA (La "Máscara")
        nueva_maestra = CatClaveCGCA(
            id_cgca=registro.id_cgca,
            clave_cgca=c_final,
            nombre_cgca=request.form.get('serie_nombre')
        )
        db.session.add(nueva_maestra)
        mensaje = 'Registro guardado y vinculado.'

    try:
        db.session.commit()
        flash(mensaje, 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {e}', 'danger')

    return redirect(url_for('main.cat_cgca'))
    
@main.route('/editar_cgca/<int:id_cgca>', methods=['GET', 'POST'])
@login_required
def editar_cgca(id_cgca):
    # 1. Buscamos el registro en el catálogo base
    registro = CatCGCA.query.get_or_404(id_cgca)
    # 2. Buscamos su espejo en la tabla maestra (importante para la "máscara")
    maestra = CatClaveCGCA.query.filter_by(id_cgca=id_cgca).first()
    
    if request.method == 'POST':
        s_clave = request.form.get('seccion_clave', '').strip() 
        f_clave = request.form.get('funcion_clave', '').upper().strip()
        nombres_funciones = {'C': 'Común', 'S': 'Sustantiva'}
        
        # Actualización de campos del catálogo
        registro.seccion_clave = s_clave
        registro.seccion_nombre = request.form.get('seccion_nombre')
        registro.funcion_clave = f_clave
        registro.funcion_nombre = nombres_funciones.get(f_clave, request.form.get('funcion_nombre'))
        registro.subseccion_clave = request.form.get('subseccion_clave')
        registro.subseccion_nombre = request.form.get('subseccion_nombre')
        registro.serie_clave = request.form.get('serie_clave')
        registro.serie_nombre = request.form.get('serie_nombre')
        registro.subserie_clave = request.form.get('subserie_clave')
        registro.subserie_nombre = request.form.get('subserie_nombre')
        
        # Guardamos la clave nueva (máscara)
        nueva_clave = request.form.get('clave_cgca', '').strip().upper()
        registro.clave_cgca = nueva_clave
        
        registro.descripcion = request.form.get('descripcion')
        registro.observaciones = request.form.get('observaciones')
        
        # --- SINCRONIZACIÓN CON TABLA MAESTRA ---
        # Si existe el espejo, actualizamos la máscara y el nombre descriptivo
        if maestra:
            maestra.clave_cgca = nueva_clave
            # Usamos el nombre de la serie para que se vea bien en los dropdowns de expedientes
            maestra.nombre_cgca = request.form.get('serie_nombre', 'Serie sin nombre')
        else:
            # Por si acaso no existía (registros viejos), lo creamos
            nueva_maestra = CatClaveCGCA(
                id_cgca=registro.id_cgca,
                clave_cgca=nueva_clave,
                nombre_cgca=request.form.get('serie_nombre', 'Serie sin nombre')
            )
            db.session.add(nueva_maestra)

        try:
            db.session.commit()
            flash('Registro y Tabla Maestra actualizados correctamente', 'success')
            return redirect(url_for('main.cat_cgca'))
        except Exception as e:
            db.session.rollback()
            print(f"Error técnico: {e}")
            flash(f'Error al actualizar: {str(e)}', 'danger')
            
    return render_template('main/editar_cgca.html', registro=registro)

@main.route('/eliminar_cgca/<int:id_cgca>', methods=['POST'])
@login_required
def eliminar_cgca(id_cgca):
    registro = CatCGCA.query.get_or_404(id_cgca)
    # Buscamos su espejo en la tabla maestra
    maestra = CatClaveCGCA.query.filter_by(id_cgca=id_cgca).first()
    
    try:
        if maestra:
            db.session.delete(maestra) # Esto intentará borrar el vínculo
        db.session.delete(registro)
        db.session.commit()
        flash('Registro eliminado del catálogo y de la tabla maestra.', 'success')
    except Exception as e:
        db.session.rollback()
        # Aquí el error te dirá: "Aún hay expedientes usando este ID"
        flash('No se puede eliminar: existen expedientes o fichas vinculadas a esta serie.', 'warning')
    return redirect(url_for('main.cat_cgca'))

# --- SECCIÓN: INSTRUMENTO (VISTA DOCUMENTO CGCA) ---
@main.route('/cgca')
@login_required
def cgca():
    # Diccionario para meses en español (opcional)
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    ahora = datetime.now()
    fecha_hoy = f"{ahora.day} de {meses[ahora.month - 1]} de {ahora.year}"

    catalogo = CatCGCA.query.order_by(
        CatCGCA.seccion_clave.asc(),
        CatCGCA.funcion_clave.asc(),
        CatCGCA.subseccion_clave.asc(),
        CatCGCA.serie_clave.asc(),
        CatCGCA.subserie_clave.asc()
    ).all()

    return render_template('main/cgca.html', 
                           catalogo=catalogo, 
                           fecha_actualizacion=fecha_hoy)

# --------------------------
# -------- Catálogos -------
# --------------------------
@main.route('/catalogos')
@login_required
def mostrar_catalogos():
    return render_template('main/catalogos.html')

#--- Dependencia ------
@main.route('/cat_dependencia', methods=['GET', 'POST'])
@login_required
def cat_dependencia():
    if request.method == 'POST':
        nombre = request.form.get('nombre_dependencia').upper()
        siglas = request.form.get('siglas_dependencia').upper()
        nueva_dep = CatDependencia(nombre_dependencia=nombre, siglas_dependencia=siglas)
        db.session.add(nueva_dep)
        db.session.commit()
        flash('Dependencia registrada', 'success')
        return redirect(url_for('main.cat_dependencia'))
    
    dependencias = CatDependencia.query.all()
    return render_template('main/cat_dependencia.html', dependencias=dependencias)

# --- RUTA DE EDICIÓN ---
@main.route('/editar_dependencia/<int:id_dependencia>', methods=['GET', 'POST'])
@login_required
def editar_dependencia(id_dependencia):
    registro = CatDependencia.query.get_or_404(id_dependencia)
    if request.method == 'POST':
        registro.nombre_dependencia = request.form.get('nombre_dependencia').upper()
        registro.siglas_dependencia = request.form.get('siglas_dependencia').upper()
        db.session.commit()
        flash('Dependencia actualizada', 'success')
        return redirect(url_for('main.cat_dependencia'))
    return render_template('main/editar_dependencia.html', registro=registro)

# --- RUTA DE ELIMINACIÓN ---
@main.route('/eliminar_dependencia/<int:id_dependencia>')
@login_required
def eliminar_dependencia(id_dependencia):
    registro = CatDependencia.query.get_or_404(id_dependencia)
    try:
        db.session.delete(registro)
        db.session.commit()
        flash('Registro eliminado correctamente', 'warning')
    except Exception as e:
        db.session.rollback()
        flash('No se puede eliminar: el registro está en uso por otras áreas', 'danger')
    return redirect(url_for('main.cat_dependencia'))

# --- Unidades Administrativas ---
# --- LISTAR Y GUARDAR -----------
@main.route('/cat_unidades', methods=['GET', 'POST'])
@login_required
def cat_unidades():
    # Filtro opcional por dependencia desde la URL (?dep_id=1)
    dep_id_filter = request.args.get('dep_id', type=int)
    
    if request.method == 'POST':
        nombre = request.form.get('nombre_ua').upper()
        siglas = request.form.get('siglas_ua').upper()
        id_dep = request.form.get('id_dependencia')
        
        nueva_ua = CatUnidadesAdministrativas(
            nombre_ua=nombre, 
            siglas_ua=siglas, 
            id_dependencia=id_dep
        )
        db.session.add(nueva_ua)
        db.session.commit()
        flash('Unidad Administrativa registrada', 'success')
        return redirect(url_for('main.cat_unidades', dep_id=id_dep))
    
    # Lógica de filtrado para la tabla
    query = CatUnidadesAdministrativas.query
    if dep_id_filter:
        unidades = query.filter_by(id_dependencia=dep_id_filter).all()
    else:
        unidades = query.all()
        
    dependencias = CatDependencia.query.all()
    return render_template('main/cat_unidades.html', 
                           unidades=unidades, 
                           dependencias=dependencias, 
                           dep_id_filter=dep_id_filter)

# --- EDITAR ---
@main.route('/editar_ua/<int:id_ua>', methods=['GET', 'POST'])
@login_required
def editar_ua(id_ua):
    registro = CatUnidadesAdministrativas.query.get_or_404(id_ua)
    if request.method == 'POST':
        registro.nombre_ua = request.form.get('nombre_ua').upper()
        registro.siglas_ua = request.form.get('siglas_ua').upper()
        registro.id_dependencia = request.form.get('id_dependencia')
        db.session.commit()
        flash('Unidad actualizada', 'success')
        return redirect(url_for('main.cat_unidades', dep_id=registro.id_dependencia))
    
    dependencias = CatDependencia.query.all()
    return render_template('main/editar_ua.html', registro=registro, dependencias=dependencias)

# --- ELIMINAR ---
@main.route('/eliminar_ua/<int:id_ua>')
@login_required
def eliminar_ua(id_ua):
    registro = CatUnidadesAdministrativas.query.get_or_404(id_ua)
    id_dep_orig = registro.id_dependencia
    db.session.delete(registro)
    db.session.commit()
    flash('Unidad eliminada', 'warning')
    return redirect(url_for('main.cat_unidades', dep_id=id_dep_orig))

# --------- Áreas --------
# --- LISTAR Y GUARDAR ---
@main.route('/cat_areas', methods=['GET', 'POST'])
@login_required
def cat_areas():
    ua_id_filter = request.args.get('ua_id', type=int)
    
    if request.method == 'POST':
        nombre = request.form.get('nombre_area').upper()
        siglas = request.form.get('siglas_area').upper()
        id_ua = request.form.get('id_ua')
        
        # Obtenemos la dependencia automáticamente de la UA seleccionada
        ua_parent = CatUnidadesAdministrativas.query.get(id_ua)
        
        nueva_area = CatAreasProductoras(
            nombre_area=nombre,
            siglas_area=siglas,
            id_ua=id_ua,
            id_dependencia=ua_parent.id_dependencia
        )
        db.session.add(nueva_area)
        db.session.commit()
        flash('Área Productora registrada', 'success')
        return redirect(url_for('main.cat_areas', ua_id=id_ua))

    unidades = CatUnidadesAdministrativas.query.all()
    query = CatAreasProductoras.query
    areas = query.filter_by(id_ua=ua_id_filter).all() if ua_id_filter else query.all()
    
    return render_template('main/cat_areas.html', areas=areas, unidades=unidades, ua_id_filter=ua_id_filter)

# --- EDITAR ---
@main.route('/editar_area/<int:id_area>', methods=['GET', 'POST'])
@login_required
def editar_area(id_area):
    registro = CatAreasProductoras.query.get_or_404(id_area)
    if request.method == 'POST':
        registro.nombre_area = request.form.get('nombre_area').upper()
        registro.siglas_area = request.form.get('siglas_area').upper()
        registro.id_ua = request.form.get('id_ua')
        
        ua_parent = CatUnidadesAdministrativas.query.get(registro.id_ua)
        registro.id_dependencia = ua_parent.id_dependencia
        
        db.session.commit()
        flash('Área actualizada', 'success')
        return redirect(url_for('main.cat_areas', ua_id=registro.id_ua))
    
    unidades = CatUnidadesAdministrativas.query.all()
    return render_template('main/editar_area.html', registro=registro, unidades=unidades)

# --- ELIMINAR ---
@main.route('/eliminar_area/<int:id_area>')
@login_required
def eliminar_area(id_area):
    registro = CatAreasProductoras.query.get_or_404(id_area)
    ua_id_orig = registro.id_ua
    db.session.delete(registro)
    db.session.commit()
    flash('Área eliminada', 'warning')
    return redirect(url_for('main.cat_areas', ua_id=ua_id_orig))

# --- LISTAR Y GUARDAR ---
@main.route('/cat_funcionarios', methods=['GET', 'POST'])
@login_required
def cat_funcionarios():
    if request.method == 'POST':
        # Conversión de fechas
        f_inicio = request.form.get('fecha_designacion_func')
        f_inicio = datetime.strptime(f_inicio, '%Y-%m-%d').date() if f_inicio else None
        
        id_area = request.form.get('id_area')
        area_obj = CatAreasProductoras.query.get(id_area)
        
        nuevo_func = CatFuncionarios(
            nombre_funcionario=request.form.get('nombre_funcionario').upper(),
            cargo_funcionario=request.form.get('cargo_funcionario').upper(),
            fecha_designacion_func=f_inicio,
            id_area=id_area,
            id_ua=area_obj.id_ua,
            id_dependencia=area_obj.id_dependencia
        )
        db.session.add(nuevo_func)
        db.session.commit()
        flash('Funcionario registrado con éxito', 'success')
        return redirect(url_for('main.cat_funcionarios'))

    # Filtro opcional por área
    area_id_filter = request.args.get('area_id', type=int)
    areas = CatAreasProductoras.query.all()
    
    if area_id_filter:
        funcionarios = CatFuncionarios.query.filter_by(id_area=area_id_filter).all()
    else:
        funcionarios = CatFuncionarios.query.all()
        
    return render_template('main/cat_funcionarios.html', 
                           funcionarios=funcionarios, 
                           areas=areas, 
                           area_id_filter=area_id_filter)

# --- EDITAR ---
@main.route('/editar_funcionario/<int:id_func>', methods=['GET', 'POST'])
@login_required
def editar_funcionario(id_func):
    registro = CatFuncionarios.query.get_or_404(id_func)
    
    if request.method == 'POST':
        # 1. Obtener el ID del área del formulario
        area_id = request.form.get('id_area')
        
        # 2. Buscar el objeto del área para heredar su jerarquía
        area_obj = CatAreasProductoras.query.get(area_id)
        
        if area_obj:
            registro.nombre_funcionario = request.form.get('nombre_funcionario')
            registro.cargo_funcionario = request.form.get('cargo_funcionario')
            
            # Sincronizamos toda la cadena jerárquica
            registro.id_area = area_obj.id_area
            registro.id_ua = area_obj.id_ua
            registro.id_dependencia = area_obj.id_dependencia
            
            # Procesamiento de fechas
            f_inicio = request.form.get('fecha_designacion_func')
            f_fin = request.form.get('fecha_fin_func')
            registro.fecha_designacion_func = datetime.strptime(f_inicio, '%Y-%m-%d').date() if f_inicio else None
            registro.fecha_fin_func = datetime.strptime(f_fin, '%Y-%m-%d').date() if f_fin else None

            db.session.commit()
            flash('Datos actualizados con éxito', 'success')
            return redirect(url_for('main.cat_funcionarios'))

    # Crucial: Enviamos las áreas para que el <select> tenga opciones
    areas = CatAreasProductoras.query.all()
    return render_template('main/editar_funcionario.html', registro=registro, areas=areas)
    
# --- ELIMINAR ---
@main.route('/eliminar_funcionario/<int:id_func>')
@login_required
def eliminar_funcionario(id_func):
    registro = CatFuncionarios.query.get_or_404(id_func)
    db.session.delete(registro)
    db.session.commit()
    flash('Funcionario eliminado del catálogo', 'warning')
    return redirect(url_for('main.cat_funcionarios'))

# --- LISTAR Y GUARDAR ---
@main.route('/cat_leyes', methods=['GET', 'POST'])
@login_required
def cat_leyes():
    siglas_filter = request.args.get('siglas', type=str)
    
    if request.method == 'POST':
        nueva_ley = CatLeyes(
            nombre_ley=request.form.get('nombre_ley').upper(),
            siglas_ley=request.form.get('siglas_ley').upper(),
            articulo=request.form.get('articulo'),
            fraccion=request.form.get('fraccion'),
            inciso=request.form.get('inciso'),
            ambito=request.form.get('ambito').upper(),
            texto_ley=request.form.get('texto_ley')
        )
        db.session.add(nueva_ley)
        db.session.commit()
        flash('Fundamento legal registrado', 'success')
        return redirect(url_for('main.cat_leyes', siglas=nueva_ley.siglas_ley))

    # Obtener siglas únicas para el filtro
    todas_siglas = db.session.query(CatLeyes.siglas_ley).distinct().all()
    
    query = CatLeyes.query
    if siglas_filter:
        leyes = query.filter_by(siglas_ley=siglas_filter).all()
    else:
        leyes = query.all()
        
    return render_template('main/cat_leyes.html', leyes=leyes, todas_siglas=todas_siglas, siglas_filter=siglas_filter)

# --- EDITAR ---
@main.route('/editar_ley/<int:id_ley>', methods=['GET', 'POST'])
@login_required
def editar_ley(id_ley):
    registro = CatLeyes.query.get_or_404(id_ley)
    if request.method == 'POST':
        registro.nombre_ley = request.form.get('nombre_ley').upper()
        registro.siglas_ley = request.form.get('siglas_ley').upper()
        registro.articulo = request.form.get('articulo')
        registro.fraccion = request.form.get('fraccion')
        registro.inciso = request.form.get('inciso')
        registro.ambito = request.form.get('ambito').upper()
        registro.texto_ley = request.form.get('texto_ley')
        
        db.session.commit()
        flash('Ley actualizada con éxito', 'success')
        return redirect(url_for('main.cat_leyes', siglas=registro.siglas_ley))
    
    return render_template('main/editar_ley.html', registro=registro)

# --- ELIMINAR ---
@main.route('/eliminar_ley/<int:id_ley>')
@login_required
def eliminar_ley(id_ley):
    registro = CatLeyes.query.get_or_404(id_ley)
    db.session.delete(registro)
    db.session.commit()
    flash('Fundamento legal eliminado', 'warning')
    return redirect(url_for('main.cat_leyes'))

# --- LISTAR Y GUARDAR ---
@main.route('/cat_funciones', methods=['GET', 'POST'])
@login_required
def cat_funciones():
    if request.method == 'POST':
        # Capturamos y convertimos a MAYÚSCULAS para estandarizar
        nombre = request.form.get('nombre_funcion', '').upper()
        desc = request.form.get('descripcion_funcion', '').upper()
        
        # IMPORTANTE: Usamos la clase CatFunciones (plural)
        nueva_f = CatFunciones(nombre_funcion=nombre, descripcion_funcion=desc)
        db.session.add(nueva_f)
        db.session.commit()
        flash('Función registrada correctamente', 'success')
        return redirect(url_for('main.cat_funciones'))

    funciones = CatFunciones.query.all()
    return render_template('main/cat_funciones.html', funciones=funciones)

@main.route('/editar_funcion/<int:id_func>', methods=['GET', 'POST'])
@login_required
def editar_funcion(id_func):
    # 1. Buscamos el registro en la base de datos
    registro = CatFunciones.query.get_or_404(id_func)
    
    if request.method == 'POST':
        # 2. Procesamos el guardado
        registro.nombre_funcion = request.form.get('nombre_funcion', '').upper()
        registro.descripcion_funcion = request.form.get('descripcion_funcion', '').upper()
        db.session.commit()
        flash('Función actualizada', 'success')
        return redirect(url_for('main.cat_funciones'))
    
    # 3. EL ERROR ESTÁ AQUÍ: Debes pasar "registro" explícitamente
    return render_template('main/editar_funcion.html', registro=registro)

@main.route('/eliminar_funcion/<int:id_func>')
@login_required
def eliminar_funcion(id_func):
    registro = CatFunciones.query.get_or_404(id_func)
    try:
        db.session.delete(registro)
        db.session.commit()
        flash('Función eliminada del catálogo', 'warning')
    except Exception:
        db.session.rollback()
        flash('Error: La función no puede eliminarse porque está vinculada a una Serie Documental.', 'danger')
    
    return redirect(url_for('main.cat_funciones'))

# --- LISTAR Y GUARDAR ---
@main.route('/cat_disposicion', methods=['GET', 'POST'])
@login_required
def cat_disposicion():
    if request.method == 'POST':
        v_tramite = int(request.form.get('anios_tramite', 0))
        v_concentra = int(request.form.get('anios_concentracion', 0))
        
        # CORRECCIÓN: Buscamos el ID de la serie seleccionada
        # El formulario ahora debe enviar el ID, no la clave.
        id_serie = request.form.get('id_cgca') 
        
        nueva_dispo = ClaveCGCACDD(
            id_cgca=id_serie, # Usamos el ID numérico
            administrativo='administrativo' in request.form,
            justificacion_admvo=request.form.get('justificacion_admvo'),
            legal='legal' in request.form,
            justificacion_legal=request.form.get('justificacion_legal'),
            fiscal='fiscal' in request.form,
            justificacion_fiscal=request.form.get('justificacion_fiscal'),
            testimonial='testimonial' in request.form,
            justificacion_testimonial=request.form.get('justificacion_testimonial'),
            historico='historico' in request.form,
            justificacion_historico=request.form.get('justificacion_historico'),
            evidencial='evidencial' in request.form,
            justificacion_evidencial=request.form.get('justificacion_extra'), 
            anios_tramite=v_tramite,
            anios_concentracion=v_concentra,
            anio_total=v_tramite + v_concentra,
            tecnica_seleccion=request.form.get('tecnica_seleccion').upper(),
            justificacion_disposicion=request.form.get('justificacion_disposicion')
        )
        
        try:
            db.session.add(nueva_dispo)
            db.session.commit()
            flash('Valores y vigencias asignados correctamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al guardar: {str(e)}', 'danger')
            
        return redirect(url_for('main.cat_disposicion'))

    # CORRECCIÓN: Asegúrate de que 'CatClaveCGCA' es el modelo que tiene las claves maestras
    series_disponibles = CatClaveCGCA.query.order_by(CatClaveCGCA.clave_cgca).all()
    registros_cdd = ClaveCGCACDD.query.all()
    
    return render_template('main/cat_disposicion.html', 
                           registros_cdd=registros_cdd, 
                           series=series_disponibles)

@main.route('/editar_disposicion/<int:id_dispo>', methods=['GET', 'POST'])
@login_required
def editar_disposicion(id_dispo):
    registro = ClaveCGCACDD.query.get_or_404(id_dispo)
    # nombre_serie obtenido via relación
    nombre_serie = registro.maestra.nombre_cgca if registro.maestra else "Serie no encontrada"

    if request.method == 'POST':
        try:
            # Actualización de vigencias
            v_tramite = int(request.form.get('anios_tramite', 0))
            v_concentra = int(request.form.get('anios_concentracion', 0))
            registro.anios_tramite = v_tramite
            registro.anios_concentracion = v_concentra
            registro.anio_total = v_tramite + v_concentra
            
            # Valores Primarios
            registro.administrativo = 'administrativo' in request.form
            registro.justificacion_admvo = request.form.get('justificacion_admvo')
            registro.legal = 'legal' in request.form
            registro.justificacion_legal = request.form.get('justificacion_legal')
            registro.fiscal = 'fiscal' in request.form
            registro.justificacion_fiscal = request.form.get('justificacion_fiscal')
            
            # Valores Secundarios (Sincronizado: justificacion_extra -> justificacion_evidencial)
            registro.testimonial = 'testimonial' in request.form
            registro.justificacion_testimonial = request.form.get('justificacion_testimonial')
            registro.historico = 'historico' in request.form
            registro.justificacion_historico = request.form.get('justificacion_historico')
            registro.evidencial = 'evidencial' in request.form
            registro.justificacion_evidencial = request.form.get('justificacion_extra')
            
            # Técnica y destino
            registro.tecnica_seleccion = request.form.get('tecnica_seleccion').upper()
            registro.justificacion_disposicion = request.form.get('justificacion_disposicion')
            
            db.session.commit()
            flash('Disposición actualizada correctamente', 'success')
            return redirect(url_for('main.cat_disposicion'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar: {str(e)}', 'danger')
    
    return render_template('main/editar_disposicion.html', registro=registro, nombre_serie=nombre_serie)

@main.route('/eliminar_disposicion/<int:id_dispo>')
@login_required
def eliminar_disposicion(id_dispo):
    registro = ClaveCGCACDD.query.get_or_404(id_dispo)
    try:
        db.session.delete(registro)
        db.session.commit()
        flash('El registro de valoración ha sido eliminado', 'warning')
    except Exception as e:
        db.session.rollback()
        flash(f'No se pudo eliminar el registro: {str(e)}', 'danger')
        
    return redirect(url_for('main.cat_disposicion'))

# --- LISTAR Y GUARDAR ---
@main.route('/cat_archivo', methods=['GET', 'POST'])
@login_required
def cat_archivo():
    if request.method == 'POST':
        nuevo_archivo = CatArchivo(
            nombre_archivo=request.form.get('nombre_archivo').upper(),
            ubicacion=request.form.get('ubicacion').upper()
        )
        db.session.add(nuevo_archivo)
        db.session.commit()
        flash('Sede de archivo registrada', 'success')
        return redirect(url_for('main.cat_archivo'))

    archivos = CatArchivo.query.all()
    return render_template('main/cat_archivo.html', archivos=archivos)

# --- EDITAR ---
@main.route('/editar_archivo/<int:id_archivo>', methods=['GET', 'POST'])
@login_required
def editar_archivo(id_archivo):
    registro = CatArchivo.query.get_or_404(id_archivo)
    if request.method == 'POST':
        registro.nombre_archivo = request.form.get('nombre_archivo').upper()
        registro.ubicacion = request.form.get('ubicacion').upper()
        db.session.commit()
        flash('Información de archivo actualizada', 'success')
        return redirect(url_for('main.cat_archivo'))
    
    return render_template('main/editar_archivo.html', registro=registro)

# --- ELIMINAR ---
@main.route('/eliminar_archivo/<int:id_archivo>')
@login_required
def eliminar_archivo(id_archivo):
    registro = CatArchivo.query.get_or_404(id_archivo)
    db.session.delete(registro)
    db.session.commit()
    flash('Sede eliminada del catálogo', 'warning')
    return redirect(url_for('main.cat_archivo'))

# --- LISTAR Y GUARDAR ---
@main.route('/cat_areas_externas', methods=['GET', 'POST'])
@login_required
def cat_areas_externas():
    if request.method == 'POST':
        nueva_ext = CatAreasExternas(
            nombre_area_externa=request.form.get('nombre_area_externa').upper(),
            nombre_institucion=request.form.get('nombre_institucion').upper(),
            siglas_institucion=request.form.get('siglas_institucion').upper()
        )
        db.session.add(nueva_ext)
        db.session.commit()
        flash('Institución externa registrada', 'success')
        return redirect(url_for('main.cat_areas_externas'))

    externas = CatAreasExternas.query.all()
    return render_template('main/cat_areas_externas.html', externas=externas)

# --- EDITAR ---
@main.route('/editar_area_ext/<int:id_ext>', methods=['GET', 'POST'])
@login_required
def editar_area_ext(id_ext):
    registro = CatAreasExternas.query.get_or_404(id_ext)
    if request.method == 'POST':
        registro.nombre_area_externa = request.form.get('nombre_area_externa').upper()
        registro.nombre_institucion = request.form.get('nombre_institucion').upper()
        registro.siglas_institucion = request.form.get('siglas_institucion').upper()
        db.session.commit()
        flash('Datos externos actualizados', 'success')
        return redirect(url_for('main.cat_areas_externas'))
    
    return render_template('main/editar_area_ext.html', registro=registro)

# --- ELIMINAR ---
@main.route('/eliminar_area_ext/<int:id_ext>')
@login_required
def eliminar_area_ext(id_ext):
    registro = CatAreasExternas.query.get_or_404(id_ext)
    db.session.delete(registro)
    db.session.commit()
    flash('Registro externo eliminado', 'warning')
    return redirect(url_for('main.cat_areas_externas'))

# --- LISTAR Y GUARDAR ---
@main.route('/cat_soporte', methods=['GET', 'POST'])
@login_required
def cat_soporte():
    if request.method == 'POST':
        nuevo_soporte = CatSoporteDocumental(
            soporte=request.form.get('soporte').upper()
        )
        db.session.add(nuevo_soporte)
        db.session.commit()
        flash('Tipo de soporte registrado', 'success')
        return redirect(url_for('main.cat_soporte'))

    soportes = CatSoporteDocumental.query.all()
    return render_template('main/cat_soporte.html', soportes=soportes)

# --- EDITAR ---
@main.route('/editar_soporte/<int:id_soporte>', methods=['GET', 'POST'])
@login_required
def editar_soporte(id_soporte):
    registro = CatSoporteDocumental.query.get_or_404(id_soporte)
    if request.method == 'POST':
        registro.soporte = request.form.get('soporte').upper()
        db.session.commit()
        flash('Soporte actualizado', 'success')
        return redirect(url_for('main.cat_soporte'))
    
    return render_template('main/editar_soporte.html', registro=registro)

# --- ELIMINAR ---
@main.route('/eliminar_soporte/<int:id_soporte>')
@login_required
def eliminar_soporte(id_soporte):
    registro = CatSoporteDocumental.query.get_or_404(id_soporte)
    db.session.delete(registro)
    db.session.commit()
    flash('Registro de soporte eliminado', 'warning')
    return redirect(url_for('main.cat_soporte'))

# --- Catálogo de Procedimientos y Actividades ---
@main.route('/cat_procedimientos', methods=['GET', 'POST'])
@login_required
def cat_procedimientos():
    if request.method == 'POST':
        nombre_proc = request.form.get('nombre_procedimiento').strip().upper()
        
        # 1. Registro en la tabla PADRE
        procedimiento = CatProcedimientos.query.filter_by(nombre_procedimiento=nombre_proc).first()
        if not procedimiento:
            procedimiento = CatProcedimientos(nombre_procedimiento=nombre_proc)
            db.session.add(procedimiento)
            db.session.flush() 
        
        # 2. Captura de listas del formulario
        descripciones = request.form.getlist('descripcion_actividad[]')
        responsables = request.form.getlist('responsable[]')
        productos = request.form.getlist('producto[]')
        
        # Nuevos campos de vinculación formal
        tipos_coord = request.form.getlist('tipo_coord[]') # 'INT' o 'EXT'
        ids_coord = request.form.getlist('id_coord[]')     # ID de la tabla seleccionada

        # 3. Guardado de actividades
        for i in range(len(descripciones)):
            if descripciones[i].strip():
                # Lógica de asignación de llaves foráneas
                ua_id = ids_coord[i] if tipos_coord[i] == 'INT' else None
                ext_id = ids_coord[i] if tipos_coord[i] == 'EXT' else None

                nueva_act = CatActividades(
                    id_procedimiento=procedimiento.id_procedimiento,
                    descripcion_actividad=descripciones[i].upper(),
                    responsable_ejecucion=responsables[i].upper(),
                    tipo_documental_producido=productos[i].upper(),
                    id_ua=ua_id,
                    id_area_ext=ext_id
                )
                db.session.add(nueva_act)
        
        db.session.commit()
        flash('Procedimiento y actividades registrados con éxito', 'success')
        return redirect(url_for('main.cat_procedimientos'))

    # GET: Traemos catálogos para alimentar los selectores
    procedimientos = CatProcedimientos.query.order_by(CatProcedimientos.nombre_procedimiento).all()
    unidades = CatUnidadesAdministrativas.query.order_by(CatUnidadesAdministrativas.nombre_ua).all()
    externas = CatAreasExternas.query.order_by(CatAreasExternas.nombre_area_externa).all()
    
    return render_template('main/cat_procedimientos.html', 
                           procedimientos=procedimientos, 
                           unidades=unidades, 
                           externas=externas)

@main.route('/editar_procedimiento/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_procedimiento(id):
    procedimiento = CatProcedimientos.query.get_or_404(id)
    if request.method == 'POST':
        nuevo_nombre = request.form.get('nombre_procedimiento').strip().upper()
        if nuevo_nombre:
            procedimiento.nombre_procedimiento = nuevo_nombre
            try:
                db.session.commit()
                flash('Nombre del procedimiento actualizado', 'success')
                return redirect(url_for('main.cat_procedimientos'))
            except Exception:
                db.session.rollback()
                flash('Error: El nombre ya existe.', 'danger')
    return render_template('main/editar_procedimiento.html',
                           procedimiento=procedimiento,
                           unidades=CatUnidadesAdministrativas.query.order_by(CatUnidadesAdministrativas.nombre_ua).all(),
                           externas=CatAreasExternas.query.order_by(CatAreasExternas.nombre_institucion).all())

@main.route('/editar_actividad/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_actividad(id):
    actividad = CatActividades.query.get_or_404(id)
    if request.method == 'POST':
        actividad.descripcion_actividad = request.form.get('descripcion_actividad').upper()
        actividad.responsable_ejecucion = request.form.get('responsable').upper()
        actividad.tipo_documental_producido = request.form.get('producto').upper()
        
        # Actualización de vinculación formal
        tipo = request.form.get('tipo_coord')
        id_vinculo = request.form.get('id_coord')
        
        actividad.id_ua = id_vinculo if tipo == 'INT' else None
        actividad.id_area_ext = id_vinculo if tipo == 'EXT' else None
        
        db.session.commit()
        flash('Actividad actualizada', 'success')
        return redirect(url_for('main.cat_procedimientos'))
    
    unidades = CatUnidadesAdministrativas.query.all()
    externas = CatAreasExternas.query.all()
    return render_template('main/editar_actividad.html', 
                           actividad=actividad, 
                           unidades=unidades, 
                           externas=externas)

@main.route('/eliminar_procedimiento/<int:id>')
@login_required
def eliminar_procedimiento(id):
    procedimiento = CatProcedimientos.query.get_or_404(id)
    try:
        db.session.delete(procedimiento)
        db.session.commit()
        flash('Procedimiento y actividades eliminados', 'warning')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'danger')
    return redirect(url_for('main.cat_procedimientos'))

@main.route('/eliminar_actividad/<int:id>')
@login_required
def eliminar_actividad(id):
    actividad = CatActividades.query.get_or_404(id)
    db.session.delete(actividad)
    db.session.commit()
    flash('Actividad eliminada', 'info')
    return redirect(url_for('main.cat_procedimientos'))

# --- Auditoria de Archivos (CGCA-Vinculación) ---
@main.route('/auditoria_archivo', methods=['GET', 'POST'])
@login_required
def auditoria_archivo():
    if request.method == 'POST':
        id_maestro = request.form.get('id_cgca')
        id_leyes = request.form.getlist('id_ley') # Captura array de IDs

        # Evitar duplicidad de adscripción orgánica
        existe = ClaveCGCAAreaProd.query.filter_by(id_cgca=id_maestro).first()
        if existe:
            flash('Esta serie ya tiene una adscripción registrada. Use el botón de editar.', 'warning')
            return redirect(url_for('main.auditoria_archivo'))

        try:
            # 1. Vínculos únicos
            nueva_procedencia = ClaveCGCAAreaProd(
                id_cgca=id_maestro,
                id_dependencia=request.form.get('id_dependencia'),
                id_ua=request.form.get('id_ua'),
                id_area=request.form.get('id_area')
            )
            nueva_funcion = ClaveCGCAFunciones(id_cgca=id_maestro, id_funcion=request.form.get('id_funcion'))
            nuevo_proc = ClaveCGCAProcedimientos(id_cgca=id_maestro, id_procedimiento=request.form.get('id_procedimiento'))
            
            db.session.add(nueva_procedencia)
            db.session.add(nueva_funcion)
            db.session.add(nuevo_proc)

            # 2. Vínculos múltiples (Fundamentos)
            for ley_id in id_leyes:
                nuevo_f = ClaveCGCAFundamentos(id_cgca=id_maestro, id_ley=ley_id)
                db.session.add(nuevo_f)

            db.session.commit()
            flash('Vinculación íntegra generada con éxito.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al vincular: {str(e)}', 'danger')
        return redirect(url_for('main.auditoria_archivo'))

    # GET: Traemos las series que ya tienen al menos un fundamento
    registros_vinculados = CatClaveCGCA.query.join(ClaveCGCAFundamentos).distinct().all()

    return render_template('main/auditoria_archivo.html', 
                            series=CatClaveCGCA.query.all(), 
                            leyes=CatLeyes.query.all(), 
                            funciones=CatFunciones.query.all(), 
                            procedimientos=CatProcedimientos.query.all(),
                            dependencias=CatDependencia.query.all(),
                            unidades=CatUnidadesAdministrativas.query.all(),
                            areas_prod=CatAreasProductoras.query.all(),
                            registros=registros_vinculados)

@main.route('/editar_auditoria/<int:id_maestro>', methods=['GET', 'POST'])
@login_required
def editar_auditoria(id_maestro):
    maestra = CatClaveCGCA.query.get_or_404(id_maestro)
    
    # Objetos actuales para precargar el formulario
    area_prod = ClaveCGCAAreaProd.query.filter_by(id_cgca=id_maestro).first()
    funcion_vinc = ClaveCGCAFunciones.query.filter_by(id_cgca=id_maestro).first()
    proc_vinc = ClaveCGCAProcedimientos.query.filter_by(id_cgca=id_maestro).first()

    if request.method == 'POST':
        try:
            # 1. Actualizar datos únicos
            if area_prod:
                area_prod.id_dependencia = request.form.get('id_dependencia')
                area_prod.id_ua = request.form.get('id_ua')
                area_prod.id_area = request.form.get('id_area')
            
            if funcion_vinc:
                funcion_vinc.id_funcion = request.form.get('id_funcion')
            
            if proc_vinc:
                proc_vinc.id_procedimiento = request.form.get('id_procedimiento')

            # 2. Actualizar Fundamentos (Borrado y Re-inserción)
            ClaveCGCAFundamentos.query.filter_by(id_cgca=id_maestro).delete()
            
            id_leyes = request.form.getlist('id_ley')
            for ley_id in id_leyes:
                nuevo_f = ClaveCGCAFundamentos(id_cgca=id_maestro, id_ley=ley_id)
                db.session.add(nuevo_f)

            db.session.commit()
            flash(f'Expediente {maestra.clave_cgca} actualizado.', 'success')
            return redirect(url_for('main.auditoria_archivo'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

    return render_template('main/editar_auditoria.html', 
                            maestra=maestra, area_prod=area_prod,
                            funcion_vinc=funcion_vinc, proc_vinc=proc_vinc,
                            leyes=CatLeyes.query.all(), funciones=CatFunciones.query.all(),
                            procedimientos=CatProcedimientos.query.all(),
                            dependencias=CatDependencia.query.all(),
                            unidades=CatUnidadesAdministrativas.query.all(),
                            areas_prod=CatAreasProductoras.query.all())

@main.route('/eliminar_auditoria/<int:id_maestro>')
@login_required
def eliminar_auditoria(id_maestro):
    try:
        # Borramos en bloque todas las tablas de vinculación para este ID
        ClaveCGCAAreaProd.query.filter_by(id_cgca=id_maestro).delete()
        ClaveCGCAFundamentos.query.filter_by(id_cgca=id_maestro).delete()
        ClaveCGCAFunciones.query.filter_by(id_cgca=id_maestro).delete()
        ClaveCGCAProcedimientos.query.filter_by(id_cgca=id_maestro).delete()
        
        db.session.commit()
        flash('Se han desvinculado todos los elementos orgánicos y normativos.', 'warning')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar vínculos: {str(e)}', 'danger')
        
    return redirect(url_for('main.auditoria_archivo'))
    
# ----------------------------------------------------------
# -----  Instrumentos de control archivístico---------------
# ----------------------------------------------------------
@main.route('/ver_cdd')
@login_required
def ver_cdd():
    # Usamos id_cgca que es el campo real de unión en tus modelos
    registros = db.session.query(CatCGCA, ClaveCGCACDD).outerjoin(
        ClaveCGCACDD, CatCGCA.id_cgca == ClaveCGCACDD.id_cgca
    ).order_by(
        CatCGCA.funcion_clave.asc(),
        CatCGCA.seccion_clave.asc(),
        CatCGCA.subseccion_clave.asc(),
        CatCGCA.serie_clave.asc(),
        CatCGCA.subserie_clave.asc()
    ).all()
    
    # Generamos la fecha actual para el reporte
    from datetime import datetime
    fecha_hoy = datetime.now().strftime('%d de %B de %Y')
    
    return render_template('main/ver_cdd.html', 
                           catalogo=registros, 
                           fecha_actualizacion=fecha_hoy)

@main.route('/inventario_general')
@login_required
def inventario_general():
    # Contamos cuántos expedientes hay de cada serie, filtrando por el tipo de archivo
    # id_archivo 1 = Trámite, 2 = Concentración (Ajusta los IDs según tu catálogo)
    stats_expedientes = db.session.query(
        Expediente.clave_cgca,
        func.count(db.case((Expediente.id_archivo == 1, 1))).label('tramite'),
        func.count(db.case((Expediente.id_archivo == 2, 1))).label('concentracion'),
        func.count(db.case((Expediente.id_archivo == 3, 1))).label('historico')
    ).group_by(Expediente.clave_cgca).subquery()

    inventario = db.session.query(CatCGCA, stats_expedientes).outerjoin(
        stats_expedientes, CatCGCA.clave_cgca == stats_expedientes.c.clave_cgca
    ).order_by(
        CatCGCA.funcion_clave.asc(),
        CatCGCA.seccion_clave.asc(),
        CatCGCA.subseccion_clave.asc(),
        CatCGCA.serie_clave.asc(),
        CatCGCA.subserie_clave.asc()
    ).all()

    return render_template('main/inventario.html', inventario=inventario)

# --- VISTA UNIFICADA: CAPTURA + TABLA ---
@main.route('/guia_archivos')
@login_required
def guia_archivos():
    from datetime import datetime
    meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
             "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    ahora = datetime.now()
    fecha_hoy = f"{ahora.day} de {meses[ahora.month - 1]} de {ahora.year}"

    # Traer todas las series con su guía vinculada, ordenadas jerárquicamente
    registros = db.session.query(CatCGCA, ClaveCGCAGuia).outerjoin(
        CatClaveCGCA, CatCGCA.id_cgca == CatClaveCGCA.id_cgca
    ).outerjoin(
        ClaveCGCAGuia, CatClaveCGCA.id_cgca == ClaveCGCAGuia.id_cgca
    ).order_by(
        CatCGCA.funcion_clave.asc(),
        CatCGCA.seccion_clave.asc(),
        CatCGCA.subseccion_clave.asc(),
        CatCGCA.serie_clave.asc(),
        CatCGCA.subserie_clave.asc()
    ).all()

    return render_template('main/guia_archivos.html',
                           registros=registros,
                           fecha_actualizacion=fecha_hoy)

@main.route('/condiciones-acceso', methods=['GET'])
@main.route('/condiciones-acceso/<int:id_maestro>', methods=['GET']) # Cambiado a int e id_maestro
@login_required
def condiciones_acceso(id_maestro=None): # Cambiado el nombre del parámetro
    series_catalogo = CatCGCA.query.all()
    registros_guardados = CondicionAcceso.query.all()
    
    condicion_edit = None
    if id_maestro:
        # BUSQUEDA CORRECTA: Por el ID de la clave maestra
        condicion_edit = CondicionAcceso.query.filter_by(id_cgca=id_maestro).first()
    
    return render_template('main/condiciones_acceso.html', 
                           series=series_catalogo, 
                           registros=registros_guardados,
                           condicion=condicion_edit)

# --- GUARDAR / ACTUALIZAR ---
@main.route('/guardar_condiciones', methods=['POST'])
@login_required
def guardar_condiciones():
    id_maestro = request.form.get('id_cgca')
    
    # Buscamos si ya existe una configuración para esta serie
    condicion = CondicionAcceso.query.filter_by(id_cgca=id_maestro).first()
    
    if not condicion:
        condicion = CondicionAcceso(id_cgca=id_maestro)

    # Procesamos los Checkboxes (convertir de 'on' a True/False)
    condicion.es_publica = True if request.form.get('publica') else False
    condicion.es_reservada = True if request.form.get('reservada') else False
    condicion.es_confidencial = True if request.form.get('confidencial') else False

    # Datos específicos de Reserva
    if condicion.es_reservada:
        condicion.anios_reserva = request.form.get('anios_reserva')
        condicion.justificacion_reservada = request.form.get('justificacion_reservada')
    else:
        condicion.anios_reserva = None
        condicion.justificacion_reservada = None

    # Datos específicos de Confidencial
    if condicion.es_confidencial:
        condicion.justificacion_confidencial = request.form.get('justificacion_confidencial')
    else:
        condicion.justificacion_confidencial = None

    try:
        db.session.add(condicion)
        db.session.commit()
        flash("Clasificación legal actualizada correctamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error en la base de datos: {str(e)}", "danger")

    return redirect(url_for('main.condiciones_acceso'))

# --- BORRAR ---
@main.route('/borrar_condiciones/<int:id_condicion>', methods=['GET'])
@login_required
def borrar_condiciones(id_condicion):
    registro = CondicionAcceso.query.get_or_404(id_condicion)
    try:
        db.session.delete(registro)
        db.session.commit()
        flash("Registro eliminado correctamente.", "info")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar: {str(e)}", "danger")
        
    return redirect(url_for('main.condiciones_acceso'))

@main.route('/enlaces-archivo', methods=['GET'])
@main.route('/enlaces-archivo/<int:id_enlace>', methods=['GET'])
@login_required
def enlaces_archivo(id_enlace=None):
    archivos = CatArchivo.query.all()
    enlaces = EnlaceArchivo.query.all()
    
    enlace_edit = None
    if id_enlace:
        enlace_edit = EnlaceArchivo.query.get_or_404(id_enlace)
    
    return render_template('main/enlaces_archivo.html', 
                           archivos=archivos, 
                           enlaces=enlaces, 
                           enlace=enlace_edit)

@main.route('/guardar_enlace', methods=['POST'])
@login_required
def guardar_enlace():
    id_enlace = request.form.get('id_enlace') # Campo oculto para edición
    
    if id_enlace:
        enlace = EnlaceArchivo.query.get(id_enlace)
    else:
        enlace = EnlaceArchivo()

    enlace.nombre_enlace = request.form.get('nombre').upper()
    enlace.id_archivo = request.form.get('id_archivo')
    enlace.fecha_designacion = datetime.strptime(request.form.get('fecha'), '%Y-%m-%d').date()
    enlace.cargo = request.form.get('cargo').upper()
    enlace.correo_electronico = request.form.get('correo').lower()
    enlace.telefono_archivo = request.form.get('telefono')

    try:
        db.session.add(enlace)
        db.session.commit()
        flash("Enlace de archivo guardado correctamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al guardar: {str(e)}", "danger")

    return redirect(url_for('main.enlaces_archivo'))

@main.route('/catalogos/enlaces/borrar/<int:id_enlace>', methods=['GET'])
@login_required
def borrar_enlace(id_enlace):
    enlace = EnlaceArchivo.query.get_or_404(id_enlace)
    try:
        db.session.delete(enlace)
        db.session.commit()
        flash("Enlace eliminado correctamente.", "info")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar: {str(e)}", "danger")
    
    return redirect(url_for('main.enlaces_archivo'))

from sqlalchemy.orm import joinedload

@main.route('/ficha-valoracion', methods=['GET'])
@login_required
def ficha_valoracion():
    clave_busqueda = request.args.get('clave_cgca', '').strip().upper()
    serie_maestra = None
    areas_internas = [] 
    areas_externas = []
    tipos_documentales = []
    soportes_serie = []
    fecha_min = None
    fecha_max = None

    if clave_busqueda:
        # Optimizamos con joinedload para traer los fundamentos y las leyes en una sola consulta
        serie_maestra = CatClaveCGCA.query.options(
            joinedload(CatClaveCGCA.fundamento).joinedload(ClaveCGCAFundamentos.ley)
        ).filter_by(clave_cgca=clave_busqueda).first()
        
        if not serie_maestra:
            flash(f'La clave "{clave_busqueda}" no se encuentra registrada en el Catálogo Maestro.', 'warning')
        else:
            # Lógica de actividades y áreas (se mantiene tu lógica corregida)
            actividades = []
            if serie_maestra.procedimiento_vinculo and serie_maestra.procedimiento_vinculo.procedimiento:
                actividades = serie_maestra.procedimiento_vinculo.procedimiento.actividades

            internas_set = set()
            externas_set = set()

            for act in actividades:
                if act.unidad_interna:
                    internas_set.add(act.unidad_interna)
                if act.area_externa:
                    externas_set.add(act.area_externa)

            # Ordenamiento seguro
            areas_internas = sorted(list(internas_set), key=lambda x: x.nombre_ua)
            areas_externas = sorted(list(externas_set), key=lambda x: x.nombre_area_externa)

            # Tipos documentales: extraídos de actividades, sin duplicados, sin vacíos
            tipos_set = set()
            for act in actividades:
                if act.tipo_documental_producido and act.tipo_documental_producido.strip():
                    tipos_set.add(act.tipo_documental_producido.strip().upper())
            tipos_documentales = sorted(list(tipos_set))

            # Soportes: se obtienen desde la Guía de Archivo vinculada a esta clave CGCA
            soportes_serie = []
            if serie_maestra.guia_vinculo and serie_maestra.guia_vinculo.soportes_rel:
                soportes_serie = serie_maestra.guia_vinculo.soportes_rel

            # Fechas extremas: min y max de los expedientes relacionados
            from sqlalchemy import func
            fecha_min = db.session.query(func.min(Expediente.fecha_inicio)).filter_by(id_cgca=serie_maestra.id_cgca).scalar()
            fecha_max = db.session.query(func.max(Expediente.fecha_final)).filter_by(id_cgca=serie_maestra.id_cgca).scalar()

    # El return envía 'master', que ahora contiene una LISTA de fundamentos
    return render_template('main/ficha_valoracion.html', 
                           master=serie_maestra, 
                           areas_internas_asociadas=areas_internas,
                           areas_externas_asociadas=areas_externas,
                           tipos_documentales=tipos_documentales,
                           soportes_serie=soportes_serie,
                           fecha_min=fecha_min,
                           fecha_max=fecha_max,
                           clave_busqueda=clave_busqueda)

@main.route('/cat_guia', methods=['GET', 'POST'])
@login_required
def cat_guia():
    if request.method == 'POST':
        id_cgca = request.form.get('id_cgca')
        
        # 1. Verificar si ya existe una guía para esta clave
        existente = ClaveCGCAGuia.query.filter_by(id_cgca=id_cgca).first()
        if existente:
            flash('Ya existe una guía para esta serie documental. Intente editar la existente.', 'warning')
            return redirect(url_for('main.cat_guia'))

        # 2. Crear la instancia de la Guía (sin soporte directo)
        nueva_guia = ClaveCGCAGuia(
            id_cgca=id_cgca,
            id_archivo=request.form.get('id_archivo'),
            id_funcionario=request.form.get('id_funcionario'),
            id_enlace=request.form.get('id_enlace')
        )
        
        db.session.add(nueva_guia)
        db.session.flush()  # Para obtener el id_guia antes del commit final

        # 3. Procesar la lista de soportes (vienen del botón +)
        soportes_seleccionados = request.form.getlist('id_soporte[]')
        for soporte_id in soportes_seleccionados:
            if soporte_id:
                vinculo = GuiaSoporteVinculo(
                    id_guia=nueva_guia.id_guia, 
                    id_soporte=soporte_id
                )
                db.session.add(vinculo)

        db.session.commit()
        flash('Guía de Archivo guardada exitosamente.', 'success')
        return redirect(url_for('main.cat_guia'))

    # Datos para los Selects y la Tabla (GET)
    guias_registradas = ClaveCGCAGuia.query.all()
    series = CatClaveCGCA.query.all()
    soportes = CatSoporteDocumental.query.all()
    archivos = CatArchivo.query.all()
    funcionarios = CatFuncionarios.query.all()
    enlaces = EnlaceArchivo.query.all()

    return render_template('main/cat_guia.html', 
                           guias=guias_registradas,
                           series=series,
                           soportes=soportes,
                           archivos=archivos,
                           funcionarios=funcionarios,
                           enlaces=enlaces)

@main.route('/editar_guia/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_guia(id):
    guia = ClaveCGCAGuia.query.get_or_404(id)
    
    if request.method == 'POST':
        # Actualizar datos básicos
        guia.id_archivo = request.form.get('id_archivo')
        guia.id_funcionario = request.form.get('id_funcionario')
        guia.id_enlace = request.form.get('id_enlace')
        
        # Actualizar Soportes: Borramos los anteriores y creamos los nuevos
        GuiaSoporteVinculo.query.filter_by(id_guia=guia.id_guia).delete()
        
        soportes_nuevos = request.form.getlist('id_soporte[]')
        for s_id in soportes_nuevos:
            if s_id:
                nuevo_v = GuiaSoporteVinculo(id_guia=guia.id_guia, id_soporte=s_id)
                db.session.add(nuevo_v)
        
        db.session.commit()
        flash('Guía actualizada correctamente.', 'success')
        return redirect(url_for('main.cat_guia'))

    # Datos para los Selects
    soportes = CatSoporteDocumental.query.all()
    archivos = CatArchivo.query.all()
    funcionarios = CatFuncionarios.query.all()
    enlaces = EnlaceArchivo.query.all()
    
    # Obtener IDs de soportes actuales para marcarlos en el template
    soportes_actuales = [s.id_soporte for s in guia.soportes_rel]

    return render_template('main/editar_guia.html', 
                           guia=guia, 
                           soportes=soportes, 
                           soportes_actuales=soportes_actuales,
                           archivos=archivos, 
                           funcionarios=funcionarios, 
                           enlaces=enlaces)

@main.route('/eliminar_guia/<int:id>')
@login_required
def eliminar_guia(id):
    guia = ClaveCGCAGuia.query.get_or_404(id)
    # Al borrar la guía, GuiaSoporteVinculo se borrará automáticamente 
    # si configuraste cascade="all, delete-orphan" en el modelo.
    db.session.delete(guia)
    db.session.commit()
    flash('Registro eliminado.', 'danger')
    return redirect(url_for('main.cat_guia'))
