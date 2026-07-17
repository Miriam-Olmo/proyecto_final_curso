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
                fecha,
                id_libro, generos,
                formato, perfil_socio,
                sala, dias_prestamo, renovaciones,
                dias_retraso, comentario)
             VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    columnas = ['fecha', 'id_libro', 'generos',
                'formato', 'perfil_socio', 'sala', 'dias_prestamo',
                'renovaciones', 'dias_retraso', 'comentario']

    # Lista de tuplas, en el orden correcto — sin iterrows
    datos = [tuple(x) for x in df_prestamos_limpios[columnas].itertuples(index=False, name=None)]

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