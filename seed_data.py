from mi_sistema import create_app, db
from mi_sistema.models import (
    CatDependencia, CatUnidadesAdministrativas, CatAreasProductoras, 
    CatCGCA, CatClaveCGCA, CatProcedimientos, CatActividades, ClaveCGCAProcedimientos
)

app = create_app()
with app.app_context():
    print("Cargando datos de prueba (SMADSOT)...")

    # 1. Dependencia
    smadsot = CatDependencia(nombre_dependencia="Secretaría de Medio Ambiente, Desarrollo Sustentable y Ordenamiento Territorial", siglas_dependencia="SMADSOT")
    db.session.add(smadsot)
    db.session.commit()

    # 2. Unidad Administrativa
    ua = CatUnidadesAdministrativas(nombre_ua="Dirección de Recursos Materiales", siglas_ua="DRM", id_dependencia=smadsot.id_dependencia)
    db.session.add(ua)
    db.session.commit()

    # 3. Catálogo CGCA (La base del AGN)
    serie_base = CatCGCA(
        seccion_clave="13C", seccion_nombre="CONTROL Y AUDITORÍA DE ACTIVIDADES",
        serie_clave="7", serie_nombre="Bajas Documentales",
        clave_cgca="13C.7.2",
        descripcion="Expedientes relativos a los procesos de baja documental."
    )
    db.session.add(serie_base)
    db.session.commit()

    # 4. Homologación (EL VÍNCULO MAESTRO)
    homologacion = CatClaveCGCA(
        id_cgca=serie_base.id_cgca, 
        clave_cgca=serie_base.clave_cgca, 
        nombre_cgca="Bajas Documentales (Serie)"
    )
    db.session.add(homologacion)

    # 5. Procedimiento y Actividades
    proc = CatProcedimientos(nombre_procedimiento="Procedimiento de Baja Documental de Archivo")
    db.session.add(proc)
    db.session.commit()

    act1 = CatActividades(descripcion_actividad="Identificación de expedientes con vigencia vencida", id_procedimiento=proc.id_procedimiento)
    act2 = CatActividades(descripcion_actividad="Elaboración de inventario de baja", id_procedimiento=proc.id_procedimiento)
    db.session.add_all([act1, act2])

    # 6. Vincular Serie con Procedimiento
    vinc = ClaveCGCAProcedimientos(id_cgca=homologacion.id_cgca, id_procedimiento=proc.id_procedimiento)
    db.session.add(vinc)

    db.session.commit()
    print("¡Datos cargados! Ya puedes probar la Ficha de Valoración para la clave 13C.7.2")
