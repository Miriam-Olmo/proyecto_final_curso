# Importa la clase Path de la librería pathlib, que sirve para trabajar con rutas de archivos y carpetas de forma más segura
from pathlib import Path


from lib.limpieza import (
    limpieza_generos,
    limpieza_dias_retraso,
    comentario,
    limpieza_dias_prestamo,
    limpieza_perfil_socio,
    normalizacion_id_prestamo,
    limpieza_generos_l,
    id_libro,
    limpieza_autor,
    df_excel_libros,
    df_excel_prestamos,
    estadisticas_descriptivas,
    detectar_outliers,
    generar_columnas_derivadas,
)
from lib.conexion_BBDD import insert_prestamos, insert_libros, validar_carga_prestamos, validar_carga_libros, crear_resumen_prestamos, crear_resumen_generos

base_dir = Path(__file__).resolve().parent # __file__: Es una variable especial de Python que contiene la ruta del archivo que se está ejecutando. Convierte esa ruta en un objeto Path(_file_). resolve():Obtiene la ruta absoluta.
output_dir = base_dir / "datos_limpios" # Aquí se crea una nueva ruta.
output_dir.mkdir(exist_ok=True) # crea la carpeta si no existe

# Limpiar libros
libros_limpios = df_excel_libros.copy() # Se hace una copia del DataFrame para no modificar el original.
libros_limpios = limpieza_generos_l(libros_limpios) 
libros_limpios = id_libro(libros_limpios)
libros_limpios = limpieza_autor(libros_limpios)

libros_limpios.to_excel(
    output_dir / "libros_limpios.xlsx",
    index=False, # Hace que no se escriba el índice de pandas en el Excel. 
    engine="openpyxl" # indica que se usa esa biblioteca para crear excel
)



print("=" * 20)

# Limpiar préstamos

prestamos_limpios = df_excel_prestamos.copy()
prestamos_limpios = limpieza_generos(prestamos_limpios)
prestamos_limpios = limpieza_dias_prestamo(prestamos_limpios)
prestamos_limpios = limpieza_dias_retraso(prestamos_limpios)
prestamos_limpios = comentario(prestamos_limpios)
prestamos_limpios = limpieza_perfil_socio(prestamos_limpios)
prestamos_limpios = normalizacion_id_prestamo(prestamos_limpios)

# Estadísticas, outliers y columnas derivadas
prestamos_limpios = estadisticas_descriptivas(prestamos_limpios)
prestamos_limpios = detectar_outliers(prestamos_limpios)
prestamos_limpios = generar_columnas_derivadas(prestamos_limpios)

prestamos_limpios.to_excel(output_dir / "prestamos_limpios.xlsx", index=False, engine='openpyxl')

print("Archivos generados en:", output_dir) # output_dir: Muestra en pantalla la carpeta donde se han guardado los archivos.
print("libros_limpios.xlsx")
print("prestamos_limpios.xlsx")

insert_prestamos(prestamos_limpios)
insert_libros(libros_limpios)
                                        # creado IA
# Validar carga y crear resúmenes
validar_carga_prestamos()
validar_carga_libros()

# Crear tablas de resumen/agregación
resumen_prestamos = crear_resumen_prestamos()
resumen_generos = crear_resumen_generos()