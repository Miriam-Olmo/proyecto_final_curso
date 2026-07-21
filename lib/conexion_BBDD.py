import mysql.connector
from mysql.connector import Error
import pandas as pd


db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'V4ll3c4n@93',
    'database': 'proyecto_final'
}

def get_connection():
    try:
        return mysql.connector.connect(**db_config)
    except Error as E:
        print(f'Error: {E}')
        return None


def insert_prestamos(df_prestamos_limpios):
    sql = """INSERT INTO prestamos(
                id_prestamo, fecha,
                id_libro, generos,
                formato, perfil_socio,
                sala, dias_prestamo, renovaciones,
                dias_retraso, comentario)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    columnas = ['id_prestamo','fecha',
                'id_libro', 'generos',
                'formato', 'perfil_socio', 'sala', 'dias_prestamo',
                'renovaciones', 'dias_retraso', 'comentario']

    # Lista de tuplas, en el orden correcto — sin iterrows
    datos = [tuple(x) for x in df_prestamos_limpios[columnas].itertuples(index=False, name=None)] # Convierte las filas del DataFrame en una lista de tuplas utilizando itertuples(), omitiendo el índice y nombres de clase. Es la forma más rápida de preparar datos en Pandas para SQL.

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.executemany(sql, datos)   # una sola llamada
        conn.commit()                     # un solo commit
        print(f'{cursor.rowcount} filas insertadas')
    except Error as e:
        conn.rollback() # Si ocurre un error, cancela la transacción (rollback()) para no dejar datos corruptos e imprime el error.
        print(f'Error: {e}')
    finally:
        conn.close()

def insert_libros(df_libros_limpios):
    sql = """INSERT INTO libros(
        id_libro, titulo,
        autor, anio_publicacion,
        editorial, generos)
        VALUES (%s, %s, %s, %s, %s, %s)"""

    columnas = ['id_libro', 'titulo','autor','anio_publicacion', 'editorial', 'generos']

    # Lista de tuplas, en el orden correcto — sin iterrows
    datos = [tuple(x) for x in df_libros_limpios[columnas].itertuples(index=False, name=None)]

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.executemany(sql, datos)   # una sola llamada
        conn.commit()                     # un solo commit
        print(f'{cursor.rowcount} filas insertadas')
    except Error as e:
        conn.rollback()
        print(f'Error: {e}')
    finally:
        conn.close()


## Validación y Resumen (ayuda IA)

def validar_carga_prestamos():
    """Valida que los datos de préstamos se cargaron correctamente."""
    print("\n" + "="*50)
    print("VALIDACIÓN DE CARGA - PRÉSTAMOS")
    print("="*50)
    
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        # Total de filas
        cursor.execute("SELECT COUNT(*) FROM prestamos") # Consulta y muestra el número total de registros existentes en la tabla prestamos. fetchone()[0] extrae el entero del resultado.
        total = cursor.fetchone()[0]
        print(f"\n✓ Total de préstamos cargados: {total}")
        
        # Valores nulos
        cursor.execute("""
            SELECT 
                COALESCE(SUM(IF(id_prestamo IS NULL, 1, 0)), 0) AS nulos_id,
                COALESCE(SUM(IF(fecha IS NULL, 1, 0)), 0) AS nulos_fecha,
                COALESCE(SUM(IF(dias_retraso IS NULL, 1, 0)), 0) AS nulos_retraso
            FROM prestamos
        """)
        nulos = cursor.fetchone()
        print(f"\n✓ Validación de nulos:")
        print(f"  - Nulos en id_prestamo: {nulos[0]}")
        print(f"  - Nulos en fecha: {nulos[1]}")
        print(f"  - Nulos en dias_retraso: {nulos[2]}") # Ejecuta una consulta SQL que suma las filas donde las columnas clave son nulas (NULL) e imprime el resultado posición por posición (nulos[0], nulos[1], etc.).
        
        # Duplicados
        cursor.execute("""
            SELECT id_prestamo, COUNT(*) as repeticiones
            FROM prestamos
            GROUP BY id_prestamo
            HAVING COUNT(*) > 1
        """)
        duplicados = cursor.fetchall()
        print(f"\n✓ Duplicados encontrados: {len(duplicados)}")
        
        # Rango de fechas
        cursor.execute("SELECT MIN(fecha), MAX(fecha) FROM prestamos")
        fechas = cursor.fetchone()
        print(f"\n✓ Rango de fechas: {fechas[0]} a {fechas[1]}")
        
        # Resumen de retrasos
        cursor.execute("""
            SELECT 
                COUNT(CASE WHEN dias_retraso = 0 THEN 1 END) AS sin_retraso,
                COUNT(CASE WHEN dias_retraso > 0 THEN 1 END) AS con_retraso
            FROM prestamos
        """)
        retrasosn = cursor.fetchone()
        print(f"\n✓ Resumen de retrasosn:")
        print(f"  - Sin retraso: {retrasosn[0]}")
        print(f"  - Con retraso: {retrasosn[1]}")
        
    except Error as e:
        print(f'Error: {e}')
    finally:
        conn.close()


def validar_carga_libros():
    """Valida que los datos de libros se cargaron correctamente."""
    print("\n" + "="*50)
    print("VALIDACIÓN DE CARGA - LIBROS")
    print("="*50)
    
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        # Total de filas
        cursor.execute("SELECT COUNT(*) FROM libros")
        total = cursor.fetchone()[0]
        print(f"\n✓ Total de libros cargados: {total}")
        
        # Valores nulos
        cursor.execute("""
            SELECT 
                COALESCE(SUM(IF(id_libro IS NULL, 1, 0)), 0) AS nulos_id,
                COALESCE(SUM(IF(titulo IS NULL, 1, 0)), 0) AS nulos_titulo,
                COALESCE(SUM(IF(autor IS NULL, 1, 0)), 0) AS nulos_autor
            FROM libros
        """)
        nulos = cursor.fetchone()
        print(f"\n✓ Validación de nulos:")
        print(f"  - Nulos en id_libro: {nulos[0]}")
        print(f"  - Nulos en titulo: {nulos[1]}")
        print(f"  - Nulos en autor: {nulos[2]}")
        
        # Duplicados
        cursor.execute("""
            SELECT id_libro, COUNT(*) as repeticiones
            FROM libros
            GROUP BY id_libro
            HAVING COUNT(*) > 1
        """)
        duplicados = cursor.fetchall()
        print(f"\n✓ Duplicados encontrados: {len(duplicados)}")
        
        # Rango de años
        cursor.execute("SELECT MIN(anio_publicacion), MAX(anio_publicacion) FROM libros")
        anos = cursor.fetchone()
        print(f"\n✓ Rango de años de publicación: {anos[0]} a {anos[1]}")
        
    except Error as e:
        print(f'Error: {e}')
    finally:
        conn.close()


def crear_resumen_prestamos():
    """Crea una tabla de resumen/agregación de préstamos."""
    print("\n" + "="*50)
    print("CREANDO TABLA RESUMEN DE PRÉSTAMOS")
    print("="*50)
    
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        # Eliminar tabla si existe
        cursor.execute("DROP TABLE IF EXISTS resumen_prestamos")
        
        # Crear tabla de resumen
        crear_tabla = """
        CREATE TABLE resumen_prestamos AS
        SELECT 
            perfil_socio,
            COUNT(*) AS total_prestamos,
            COUNT(DISTINCT id_libro) AS libros_diferentes,
            ROUND(AVG(dias_prestamo), 2) AS promedio_dias_prestamo,
            ROUND(AVG(dias_retraso), 2) AS promedio_dias_retraso,
            COUNT(CASE WHEN dias_retraso > 0 THEN 1 END) AS prestamos_con_retraso,
            ROUND(COUNT(CASE WHEN dias_retraso > 0 THEN 1 END) / COUNT(*) * 100, 2) AS porcentaje_retraso,
            COUNT(DISTINCT sala) AS salas_utilizadas,
            MAX(fecha) AS ultima_fecha_prestamo
        FROM prestamos
        GROUP BY perfil_socio
        ORDER BY total_prestamos DESC
        """
        
        cursor.execute(crear_tabla)
        conn.commit()
        print("\n✓ Tabla 'resumen_prestamos' creada exitosamente")
        
        # Mostrar el resumen
        cursor.execute("SELECT * FROM resumen_prestamos")
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        
        print("\n" + "="*50)
        print("CONTENIDO DEL RESUMEN:")
        print("="*50)
        
        # Crear DataFrame para mostrar mejor
        df_resumen = pd.DataFrame(resultados, columns=columnas)
        print(df_resumen.to_string(index=False))
        
        return df_resumen
        
    except Error as e:
        print(f'Error: {e}')
    finally:
        conn.close()


def crear_resumen_generos():
    """Crea una tabla de resumen de préstamos por género."""
    print("\n" + "="*50)
    print("CREANDO TABLA RESUMEN DE GÉNEROS")
    print("="*50)
    
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        # Eliminar tabla si existe
        cursor.execute("DROP TABLE IF EXISTS resumen_generos")
        
        # Crear tabla de resumen
        crear_tabla = """
        CREATE TABLE resumen_generos AS
        SELECT 
            generos,
            COUNT(*) AS total_prestamos,
            COUNT(DISTINCT id_libro) AS libros_diferentes,
            ROUND(AVG(dias_retraso), 2) AS promedio_dias_retraso,
            COUNT(CASE WHEN dias_retraso > 0 THEN 1 END) AS con_retraso
        FROM prestamos
        GROUP BY generos
        ORDER BY total_prestamos DESC
        """ # Ejecuta un CREATE TABLE ... AS SELECT (CTAS) que agrupa los préstamos por perfil de socio (perfil_socio)
        
        cursor.execute(crear_tabla)
        conn.commit()
        print("\n✓ Tabla 'resumen_generos' creada exitosamente") 
        
        # Mostrar el resumen
        cursor.execute("SELECT * FROM resumen_generos LIMIT 15")
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description] # Ejecuta la creación de la tabla, confirma la transacción en MySQL, consulta el contenido completo de la nueva tabla y recupera los nombres de las columnas a través de cursor.description.
        
        print("\n" + "="*50)
        print("TOP 15 GÉNEROS:")
        print("="*50)
        
        df_resumen = pd.DataFrame(resultados, columns=columnas)
        print(df_resumen.to_string(index=False))
        
        return df_resumen
        
    except Error as e:
        print(f'Error: {e}')
    finally:
        conn.close() # Convierte los resultados devueltos por MySQL en un DataFrame de Pandas para imprimirlo de manera limpia en la consola sin índices, retorna el DataFrame y cierra la conexión.