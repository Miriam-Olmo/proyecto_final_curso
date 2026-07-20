import pandas as pd

df_excel_prestamos = pd.read_excel('./datos_sucios/prestamos.xlsx')
print(df_excel_prestamos)

df_excel_libros = pd.read_excel('./datos_sucios/libros.xlsx')
print(df_excel_libros)

print(f'Hay {df_excel_prestamos.isnull().sum()} nulos en el archivo de prestamos')
print(f'Hay {df_excel_libros.isnull().sum()} nulos en el archivo de libros')

print(df_excel_prestamos.shape)
print(df_excel_prestamos.info())


def limpieza_generos(df_excel_prestamos):
    df_excel_prestamos['generos'] = (
        df_excel_prestamos['generos']
        .astype(str)
        .str.replace(';', '/', regex=False)
        .str.replace(r'\s+', ' ', regex=True)
        .str.strip()
        .str.lower()
    )
    return df_excel_prestamos


def limpieza_dias_retraso(df_excel_prestamos):
    df_excel_prestamos['dias_retraso'] = (
        df_excel_prestamos['dias_retraso']
        .astype(str)
        .str.replace('dias', '', regex=False)
        .str.replace(',', '.', regex=False)
        .str.strip()
        .apply(pd.to_numeric, errors='coerce')
        .fillna(0)
    )
    return df_excel_prestamos


def comentario(df_excel_prestamos):
    df_excel_prestamos['comentario'] = (
        df_excel_prestamos['comentario']
        .fillna('')
        .astype(str)
        .str.strip()
        .str.capitalize()
    )
    return df_excel_prestamos


def limpieza_dias_prestamo(df_excel_prestamos):
    df_excel_prestamos['dias_prestamo'] = pd.to_numeric(df_excel_prestamos['dias_prestamo'], errors='coerce')
    media = round(df_excel_prestamos['dias_prestamo'].mean(),2)
    df_excel_prestamos['dias_prestamo'] = df_excel_prestamos['dias_prestamo'].fillna(media)
    return df_excel_prestamos


def limpieza_perfil_socio(df_excel_prestamos):
    df_excel_prestamos['perfil_socio'] = (
        df_excel_prestamos['perfil_socio']
        .astype(str)
        .str.strip()
        .fillna('desconocido')
        .str.title()
    )
    return df_excel_prestamos


def normalizacion_id_prestamo(df_excel_prestamos):
    df_excel_prestamos = df_excel_prestamos.copy()
    return df_excel_prestamos.drop_duplicates(subset=['id_prestamo'], keep='first')


## libros

def limpieza_generos_l(df_excel_libros):
    df_excel_libros['generos'] = (
        df_excel_libros['generos']
        .astype(str)
        .str.replace(';', '/', regex=False)
        .str.replace(r'\s+', ' ', regex=True) # \s → cualquier espacio, tabulación o salto de línea. + → uno o más.
        .str.strip()
        .str.lower()
    )
    return df_excel_libros


def id_libro(df_excel_libros):
    df_excel_libros['id_libro'] = df_excel_libros['id_libro']
    return df_excel_libros
