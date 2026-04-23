from datetime import datetime
from flask_login import UserMixin
from . import db
import sqlalchemy as sa  

class Rol(db.Model):
    __tablename__ = 'roles'  # Esto vincula la clase con tu tabla 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(200))

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'

    # Identificadores y credenciales
    id_usuario = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    nombre_completo = db.Column(db.String(255), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    # Estado y contacto
    activo = db.Column(db.Boolean, default=True)
    telefono = db.Column(db.String(20))

    # Trazabilidad automática
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ultimo_acceso = db.Column(db.DateTime)

    def get_id(self):
        return str(self.id_usuario)

    def __repr__(self):
        return f'<Usuario {self.username}>'

# ----------------------- Catálogos ---------------------
# SUSTITUIR EN TU MODELS.PY:

class CatCGCA(db.Model):
    __tablename__ = 'cat_cgca'

    id_cgca = db.Column(db.Integer, primary_key=True)
    seccion_clave = db.Column(db.String(20))
    seccion_nombre = db.Column(db.String(255))
    funcion_clave = db.Column(db.String(20))
    funcion_nombre = db.Column(db.String(255))
    subseccion_clave = db.Column(db.String(20))
    subseccion_nombre = db.Column(db.String(255))
    serie_clave = db.Column(db.String(20))
    serie_nombre = db.Column(db.String(255))
    subserie_clave = db.Column(db.String(20))
    subserie_nombre = db.Column(db.String(255))
    descripcion = db.Column(db.Text, nullable=True)
    clave_cgca = db.Column(db.String(100), unique=True)
    observaciones = db.Column(db.Text, nullable=True)

    # RELACIÓN NUEVA: Permite acceder a la homologación desde aquí
    homologacion = db.relationship('CatClaveCGCA', backref='datos_maestros', uselist=False)

    def __repr__(self):
        return f'<CGCA {self.clave_cgca}>'

class CatDependencia(db.Model):
    __tablename__ = 'cat_dependencia'
    id_dependencia = db.Column(db.Integer, primary_key=True)
    nombre_dependencia = db.Column(db.String(255), nullable=False)
    siglas_dependencia = db.Column(db.String(50), nullable=False)
    vigente = db.Column(db.Boolean, default=True, nullable=False, server_default='true')

    def __repr__(self):
        return f'<Dependencia {self.siglas_dependencia}>'

class HistoriaInstitucional(db.Model):
    __tablename__ = 'historia_institucional'
    id_historia = db.Column(db.Integer, primary_key=True)
    id_dependencia = db.Column(db.Integer, db.ForeignKey('cat_dependencia.id_dependencia'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # CREACION o SUPRESION
    fecha_decreto = db.Column(db.Date, nullable=True)
    tomo = db.Column(db.String(50), nullable=True)
    numero = db.Column(db.String(50), nullable=True)
    seccion = db.Column(db.String(100), nullable=True)
    titulo_decreto = db.Column(db.Text, nullable=True)

    dependencia = db.relationship('CatDependencia', backref=db.backref('historia', lazy=True))

    def __repr__(self):
        return f'<Historia {self.tipo} {self.id_dependencia}>'

class CatUnidadesAdministrativas(db.Model):
    __tablename__ = 'cat_unidades_administrativas'
    id_ua = db.Column(db.Integer, primary_key=True)
    nombre_ua = db.Column(db.String(255), nullable=False)
    siglas_ua = db.Column(db.String(50), nullable=False)
    id_dependencia = db.Column(db.Integer, db.ForeignKey('cat_dependencia.id_dependencia'), nullable=False)
    vigente = db.Column(db.Boolean, default=True, nullable=False, server_default='true')

    # Relación para obtener datos de la dependencia padre
    dependencia = db.relationship('CatDependencia', backref=db.backref('unidades', lazy=True))

class CatAreasProductoras(db.Model):
    __tablename__ = 'cat_areas_productoras'
    id_area = db.Column(db.Integer, primary_key=True)
    nombre_area = db.Column(db.String(255), nullable=False)
    siglas_area = db.Column(db.String(50), nullable=False)
    id_ua = db.Column(db.Integer, db.ForeignKey('cat_unidades_administrativas.id_ua'), nullable=False)
    id_dependencia = db.Column(db.Integer, db.ForeignKey('cat_dependencia.id_dependencia'), nullable=False)
    vigente = db.Column(db.Boolean, default=True, nullable=False, server_default='true')

    # Relaciones para navegar la jerarquía
    unidad = db.relationship('CatUnidadesAdministrativas', backref=db.backref('areas', lazy=True))
    dependencia = db.relationship('CatDependencia', backref=db.backref('areas_todas', lazy=True))

class CatFuncionarios(db.Model):
    __tablename__ = 'cat_funcionarios'
    id_funcionarios = db.Column(db.Integer, primary_key=True)
    nombre_funcionario = db.Column(db.String(255), nullable=False)
    cargo_funcionario = db.Column(db.String(255), nullable=False)
    fecha_designacion_func = db.Column(db.Date, nullable=True)
    fecha_fin_func = db.Column(db.Date, nullable=True)
    id_dependencia = db.Column(db.Integer, db.ForeignKey('cat_dependencia.id_dependencia'))
    id_ua = db.Column(db.Integer, db.ForeignKey('cat_unidades_administrativas.id_ua'))
    id_area = db.Column(db.Integer, db.ForeignKey('cat_areas_productoras.id_area'))

    # Relaciones
    area = db.relationship('CatAreasProductoras', backref=db.backref('titulares', lazy=True))

class CatFunciones(db.Model):
    __tablename__ = 'cat_funcion'
    id_funcion = db.Column(db.Integer, primary_key=True)
    nombre_funcion = db.Column(db.String(255), nullable=False)
    descripcion_funcion = db.Column(db.Text)

    def __repr__(self):
        return f'<Funcion {self.nombre_funcion}>'

class CatLeyes(db.Model):
    __tablename__ = 'cat_leyes'
    id_ley = db.Column(db.Integer, primary_key=True)
    nombre_ley = db.Column(db.Text, nullable=False)
    siglas_ley = db.Column(db.String(50))
    articulo = db.Column(db.String(50))
    fraccion = db.Column(db.String(50))
    inciso = db.Column(db.String(50))
    ambito = db.Column(db.String(100)) # Federal, Estatal, Municipal
    texto_ley = db.Column(db.Text)

    def __repr__(self):
        return f'<Ley {self.siglas_ley} Art. {self.articulo}>'

class CatArchivo(db.Model):
    __tablename__ = 'cat_archivo'
    id_archivo = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    ubicacion = db.Column(db.Text)

    def __repr__(self):
        return f'<Archivo {self.nombre_archivo}>'

class CatAreasExternas(db.Model):
    __tablename__ = 'cat_areas_externas'
    id_area_ext = db.Column(db.Integer, primary_key=True)
    nombre_area_externa = db.Column(db.String(255), nullable=False)
    nombre_institucion = db.Column(db.String(255), nullable=False)
    siglas_institucion = db.Column(db.String(50))

    def __repr__(self):
        return f'<AreaExt {self.siglas_institucion}>'

class CatSoporteDocumental(db.Model):
    __tablename__ = 'cat_soporte_documental'
    id_soporte = db.Column(db.Integer, primary_key=True)
    soporte = db.Column(db.String(100), nullable=False) # Ej. PAPEL, ELECTRÓNICO, HÍBRIDO

    def __repr__(self):
        return f'<Soporte {self.soporte}>'

class CatProcedimientos(db.Model):
    __tablename__ = 'cat_procedimientos'
    id_procedimiento = db.Column(db.Integer, primary_key=True)
    nombre_procedimiento = db.Column(db.String(255), nullable=False, unique=True)
    
    # Relación con las actividades: 
    actividades = db.relationship('CatActividades', 
                                 backref='procedimiento', 
                                 lazy=True, 
                                 cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Procedimiento {self.nombre_procedimiento}>'

class CatActividades(db.Model):
    __tablename__ = 'cat_actividades'
    id_actividad = db.Column(db.Integer, primary_key=True)
    descripcion_actividad = db.Column(db.Text, nullable=False)
    responsable_ejecucion = db.Column(db.String(255))
    tipo_documental_producido = db.Column(db.String(255))
    
    # Llave foránea para Áreas Internas (SMADSOT)
    id_ua = db.Column(db.Integer, db.ForeignKey('cat_unidades_administrativas.id_ua'), nullable=True)
    
    # Llave foránea para Áreas Externas (Otras dependencias)
    id_area_ext = db.Column(db.Integer, db.ForeignKey('cat_areas_externas.id_area_ext'), nullable=True)
    
    # Clave foránea que conecta con el padre
    id_procedimiento = db.Column(db.Integer, db.ForeignKey('cat_procedimientos.id_procedimiento'), nullable=False)

    # Relaciones para acceder a los objetos fácilmente desde el template
    # Esto te permitirá hacer: actividad.unidad_interna.nombre_ua
    unidad_interna = db.relationship('CatUnidadesAdministrativas', backref='actividades_vinculadas')
    area_externa = db.relationship('CatAreasExternas', backref='actividades_vinculadas')

    def __repr__(self):
        return f'<Actividad {self.descripcion_actividad[:20]}...>'

class EnlaceArchivo(db.Model):
    __tablename__ = 'enlaces_archivo'
    id_enlace = db.Column(db.Integer, primary_key=True)
    nombre_enlace = db.Column(db.String(255), nullable=False)
    fecha_designacion = db.Column(db.Date, nullable=False)
    cargo = db.Column(db.String(255))
    correo_electronico = db.Column(db.String(255))
    telefono_archivo = db.Column(db.String(50))
    
    # Relación con CatArchivo
    id_archivo = db.Column(db.Integer, db.ForeignKey('cat_archivo.id_archivo'), nullable=False)
    archivo = db.relationship('CatArchivo', backref=db.backref('enlaces', lazy=True))

    def __repr__(self):
        return f'<Enlace {self.nombre_enlace}>'

# ==========================================
# MODELO MAESTRO (CENTRALIZADOR)
# ==========================================
class CatClaveCGCA(db.Model):
    __tablename__ = 'cat_clave_cgca'
    id_cgca = db.Column(db.Integer, db.ForeignKey('cat_cgca.id_cgca'), primary_key=True)
    clave_cgca = db.Column(db.String(100), unique=True, nullable=False)
    nombre_cgca = db.Column(db.Text, nullable=False)

    # --- CAMBIO AQUÍ: Eliminamos uselist=False ---
    fundamento = db.relationship('ClaveCGCAFundamentos', back_populates='maestra') 
    
    # Estos se quedan igual si solo admiten uno por serie
    funcion = db.relationship('ClaveCGCAFunciones', back_populates='maestra', uselist=False)
    procedimiento_vinculo = db.relationship('ClaveCGCAProcedimientos', back_populates='maestra', uselist=False)    
    disposiciones = db.relationship('ClaveCGCACDD', back_populates='maestra', lazy=True)
    condiciones = db.relationship('CondicionAcceso', back_populates='maestra_entidad', lazy=True)
    
    # --- Relaciones Orgánicas ---
    areas_productoras = db.relationship('ClaveCGCAAreaProd', back_populates='maestra', lazy=True)
    areas_relacionadas = db.relationship('ClaveCGCAAreaRel', back_populates='maestra', lazy=True)
    
    # --- Otros ---
    expedientes_relacionados = db.relationship('Expediente', backref='serie_maestra', lazy=True)

    def __repr__(self):
        return f'<MasterCGCA {self.clave_cgca}>'

# ==========================================
# VINCULACIONES (CLASES HIJAS)
# ==========================================

class ClaveCGCAFunciones(db.Model):
    __tablename__ = 'clavecgca_funcion'
    id_clavecgca_funcion = db.Column(db.Integer, primary_key=True)
    id_cgca = db.Column(db.Integer, db.ForeignKey('cat_clave_cgca.id_cgca'), nullable=False)
    id_funcion = db.Column(db.Integer, db.ForeignKey('cat_funcion.id_funcion'), nullable=False)
    
    # Relaciones
    maestra = db.relationship('CatClaveCGCA', back_populates='funcion')
    funcion_cat = db.relationship('CatFunciones', backref='series_vinculadas')

class ClaveCGCAAreaProd(db.Model):
    __tablename__ = 'clavecgca_area_prod'
    id_clavecgca_area_prod = db.Column(db.Integer, primary_key=True)
    id_cgca = db.Column(db.Integer, db.ForeignKey('cat_clave_cgca.id_cgca'), nullable=False)
    id_dependencia = db.Column(db.Integer, db.ForeignKey('cat_dependencia.id_dependencia'))
    id_ua = db.Column(db.Integer, db.ForeignKey('cat_unidades_administrativas.id_ua'))
    id_area = db.Column(db.Integer, db.ForeignKey('cat_areas_productoras.id_area'))

    # Relación de vuelta a la Maestra
    maestra = db.relationship('CatClaveCGCA', back_populates='areas_productoras')
    # Relaciones a catálogos para facilitar consultas
    dependencia = db.relationship('CatDependencia')
    unidad = db.relationship('CatUnidadesAdministrativas')
    area = db.relationship('CatAreasProductoras')

class ClaveCGCAAreaRel(db.Model):
    __tablename__ = 'clavecgca_area_rel'
    id_clavecgca_area_rel = db.Column(db.Integer, primary_key=True)
    id_cgca = db.Column(db.Integer, db.ForeignKey('cat_clave_cgca.id_cgca'), nullable=False)
    id_dependencia = db.Column(db.Integer, db.ForeignKey('cat_dependencia.id_dependencia'))
    id_ua = db.Column(db.Integer, db.ForeignKey('cat_unidades_administrativas.id_ua'))
    id_area = db.Column(db.Integer, db.ForeignKey('cat_areas_productoras.id_area'))

    maestra = db.relationship('CatClaveCGCA', back_populates='areas_relacionadas')

class ClaveCGCAFundamentos(db.Model):
    __tablename__ = 'clavecgca_fundamento'
    id_clavecgca_fundamento = db.Column(db.Integer, primary_key=True)
    id_cgca = db.Column(db.Integer, db.ForeignKey('cat_clave_cgca.id_cgca'), nullable=False)
    id_ley = db.Column(db.Integer, db.ForeignKey('cat_leyes.id_ley'))
    
    maestra = db.relationship('CatClaveCGCA', back_populates='fundamento')
    ley = db.relationship('CatLeyes', backref='series_fundamentadas')

class ClaveCGCAProcedimientos(db.Model):
    __tablename__ = 'clavecgca_procedimiento'
    id_clavecgca_proc = db.Column(db.Integer, primary_key=True)
    id_cgca = db.Column(db.Integer, db.ForeignKey('cat_clave_cgca.id_cgca'), nullable=False)
    id_procedimiento = db.Column(db.Integer, db.ForeignKey('cat_procedimientos.id_procedimiento'))
    
    maestra = db.relationship('CatClaveCGCA', back_populates='procedimiento_vinculo')
    procedimiento = db.relationship('CatProcedimientos', backref='series_vinculadas')

# --- VINCULACIÓN CON SOPORTE DOCUMENTAL ---
class ClaveCGCASoporte(db.Model):
    __tablename__ = 'clavecgca_soporte'
    id_clavecgca_soporte = db.Column(db.Integer, primary_key=True)
    id_cgca = db.Column(db.Integer, db.ForeignKey('cat_clave_cgca.id_cgca'), nullable=False)
    id_soporte = db.Column(db.Integer, db.ForeignKey('cat_soporte_documental.id_soporte'))
    
    # Relación opcional para consultas rápidas
    soporte = db.relationship('CatSoporteDocumental', backref='series_vinculadas')

# --- FUNCIONARIOS (RESPONSABLES Y ARCHIVISTAS) ---
class ClaveCGCAResponsable(db.Model):
    __tablename__ = 'clavecgca_responsable'
    id_clavecgca_resp = db.Column(db.Integer, primary_key=True)
    id_cgca = db.Column(db.Integer, db.ForeignKey('cat_clave_cgca.id_cgca'), nullable=False)
    id_funcionario = db.Column(db.Integer, db.ForeignKey('cat_funcionarios.id_funcionarios'), nullable=False)

    # Relación opcional
    funcionario = db.relationship('CatFuncionarios', backref='responsabilidades')

# --- ARCHIVOS ---
class ClaveCGCAArchivo(db.Model):
    __tablename__ = 'clavecgca_archivo'
    id_clavecgca_archivo = db.Column(db.Integer, primary_key=True)
    id_cgca = db.Column(db.Integer, db.ForeignKey('cat_clave_cgca.id_cgca'), nullable=False)
    id_archivo = db.Column(db.Integer, db.ForeignKey('cat_archivo.id_archivo'))

# --- ACCESO Y SEGURIDAD (VINCULACIÓN) ---
class ClaveCGCAAcceso(db.Model):
    __tablename__ = 'clavecgca_acceso'
    id_clavecgca_acceso = db.Column(db.Integer, primary_key=True)
    id_cgca = db.Column(db.Integer, db.ForeignKey('cat_clave_cgca.id_cgca'), nullable=False)
    condiciones = db.Column(db.String(255))
    id_ley = db.Column(db.Integer, db.ForeignKey('cat_leyes.id_ley'))
    
    # Relación opcional con la maestra
    maestra = db.relationship('CatClaveCGCA')

# --- FECHAS EXTREMAS ---
class ClaveCGCAFechas(db.Model):
    __tablename__ = 'clavecgca_fechas'
    id_clavecgca_fechas = db.Column(db.Integer, primary_key=True)
    id_cgca = db.Column(db.Integer, db.ForeignKey('cat_clave_cgca.id_cgca'), nullable=False)
    fecha_apertura = db.Column(db.Date)
    fecha_cierre = db.Column(db.Date)
    anio_conclusion = db.Column(db.Integer)
    causa_conclusion = db.Column(db.Text)

# --- Información asociada ----
class CondicionAcceso(db.Model):
    __tablename__ = 'condiciones_acceso'
    id_condicion = db.Column(db.Integer, primary_key=True)
    id_cgca = db.Column(db.Integer, db.ForeignKey('cat_clave_cgca.id_cgca'), nullable=False)
    
    # Cambiamos back_populates para que coincida con la Maestra
    maestra_entidad = db.relationship('CatClaveCGCA', back_populates='condiciones') 
    
    es_publica = db.Column(db.Boolean, default=False)
    es_reservada = db.Column(db.Boolean, default=False)
    es_confidencial = db.Column(db.Boolean, default=False)
    anios_reserva = db.Column(db.Integer, nullable=True)
    justificacion_reservada = db.Column(db.Text, nullable=True)
    justificacion_confidencial = db.Column(db.Text, nullable=True)

class Expediente(db.Model):
    __tablename__ = 'expediente'
    id_expediente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # CAMBIO CRÍTICO: Añadimos la relación que no existía
    id_cgca = db.Column(db.Integer, db.ForeignKey('cat_clave_cgca.id_cgca'), nullable=False)
    clave_cgca = db.Column(db.String(100), nullable=False) # Se queda como texto auxiliar
    descripcion = db.Column(db.Text, nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=True)
    fecha_final = db.Column(db.Date, nullable=True)
    fojas_expediente = db.Column(db.Integer, default=0)
    fojas_legajo = db.Column(db.Integer, default=0)
    legajo = db.Column(db.Integer, default=1)
    total_legajos = db.Column(db.Integer, default=1)
    id_archivo = db.Column(db.Integer, db.ForeignKey('cat_archivo.id_archivo'))
    estanteria = db.Column(db.String(50), nullable=True)
    caja = db.Column(db.String(50), nullable=True)

class ClaveCGCACDD(db.Model):
    __tablename__ = 'clavecgca_cdd'
    id_clavecgca_cdd = db.Column(db.Integer, primary_key=True)
    id_cgca = db.Column(db.Integer, db.ForeignKey('cat_clave_cgca.id_cgca'), nullable=False)
    
    # CAMBIO: Usar back_populates para conectar con la maestra sin chocar
    maestra = db.relationship('CatClaveCGCA', back_populates='disposiciones')
    
    administrativo = db.Column(db.Boolean, default=False)
    justificacion_admvo = db.Column(db.Text)
    legal = db.Column(db.Boolean, default=False)
    justificacion_legal = db.Column(db.Text)
    fiscal = db.Column(db.Boolean, default=False)
    justificacion_fiscal = db.Column(db.Text)
    testimonial = db.Column(db.Boolean, default=False)
    justificacion_testimonial = db.Column(db.Text)
    historico = db.Column(db.Boolean, default=False)
    justificacion_historico = db.Column(db.Text)
    evidencial = db.Column(db.Boolean, default=False)
    justificacion_evidencial = db.Column(db.Text)
    
    anios_tramite = db.Column(db.Integer, default=0)
    anios_concentracion = db.Column(db.Integer, default=0)
    anio_total = db.Column(db.Integer, default=0)
    tecnica_seleccion = db.Column(db.String(100))
    justificacion_disposicion = db.Column(db.Text)

# Tabla intermedia para múltiples soportes
class GuiaSoporteVinculo(db.Model):
    __tablename__ = 'guia_soporte_vinculo'
    id = db.Column(db.Integer, primary_key=True)
    id_guia = db.Column(db.Integer, db.ForeignKey('clave_cgca_guia.id_guia'), nullable=False)
    id_soporte = db.Column(db.Integer, db.ForeignKey('cat_soporte_documental.id_soporte'), nullable=False)

    # --- ESTA ES LA LÍNEA QUE FALTA ---
    # Permite acceder desde el vínculo al nombre del soporte: v.soporte.soporte
    soporte = db.relationship('CatSoporteDocumental', backref='vinculos_guias')

# Modelo de la Guía
class ClaveCGCAGuia(db.Model):
    __tablename__ = 'clave_cgca_guia'
    id_guia = db.Column(db.Integer, primary_key=True)
    id_cgca = db.Column(db.Integer, db.ForeignKey('cat_clave_cgca.id_cgca'), nullable=False)
    id_archivo = db.Column(db.Integer, db.ForeignKey('cat_archivo.id_archivo'), nullable=False)
    id_funcionario = db.Column(db.Integer, db.ForeignKey('cat_funcionarios.id_funcionarios'), nullable=False)
    id_enlace = db.Column(db.Integer, db.ForeignKey('enlaces_archivo.id_enlace'), nullable=False)

    # Relaciones
    soportes_rel = db.relationship('GuiaSoporteVinculo', backref='guia_parent', cascade="all, delete-orphan")
    maestra = db.relationship('CatClaveCGCA', backref=db.backref('guia_vinculo', uselist=False))
    
    # También agregamos relaciones para que el HTML no falle al buscar nombres
    archivo = db.relationship('CatArchivo', backref='guias')
    funcionario = db.relationship('CatFuncionarios', backref='guias')
    enlace = db.relationship('EnlaceArchivo', backref='guias')