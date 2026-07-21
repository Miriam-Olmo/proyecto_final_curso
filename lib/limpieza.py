import pandas as pd
import numpy as np

df_excel_prestamos = pd.read_excel('./datos_sucios/prestamos.xlsx')
print(df_excel_prestamos)

df_excel_libros = pd.read_excel('./datos_sucios/libros.xlsx')
print(df_excel_libros)

print(f'Hay {df_excel_prestamos.isnull().sum()} nulos en el archivo de prestamos') # Calcula y muestra el total de valores nulos o faltantes por cada columna dentro de df_excel_prestamos.
print(f'Hay {df_excel_libros.isnull().sum()} nulos en el archivo de libros') # Muestra el total de nulos por columna dentro de df_excel_libros.

print(df_excel_prestamos.shape) # Imprime la dimensión del DataFrame de préstamos en formato (filas, columnas).
print(df_excel_prestamos.info()) # Muestra un resumen técnico de df_excel_prestamos (tipos de datos de cada columna, conteo de valores no nulos y uso de memoria).


def limpieza_generos(df_excel_prestamos):
    df_excel_prestamos['generos'] = (
        df_excel_prestamos['generos']
        .astype(str)
        .str.replace(';', '/', regex=False)
        .str.replace(r'\s+', ' ', regex=True) # Reduce espacios múltiples, tabulaciones o saltos de línea a un único espacio en blanco.
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
        .fillna(0) # Reemplaza todos los NaN por 0 (asumiendo que si no hay un dato válido de retraso, este fue de 0 días).
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
    return df_excel_prestamos.drop_duplicates(subset=['id_prestamo'], keep='first') # Crea una copia explícita del DataFrame para evitar advertencias de modificación en vistas (SettingWithCopyWarning) y elimina filas que contengan IDs de préstamo duplicados, conservando solo la primera aparición (keep='first').


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
    df_excel_libros['id_libro'] = df_excel_libros['id_libro'].astype(str).str.strip()
    return df_excel_libros

def limpieza_autor(df_excel_libros):

    def reparar(x):
        try:
            return x.encode('latin1').decode('utf-8') # arregla problemas de codificacion en excel
        except:
            return x # Define la función auxiliar reparar(x) para solucionar el problema de Mojibake o caracteres mal codificados (por ejemplo, cuando en Excel una tilde o "ñ" se convierte en símbolos extraños como Ã±). Codifica a bytes en latin1 y decodifica correctamente en utf-8.

    df_excel_libros['autor'] = (
        df_excel_libros['autor']
        .astype(str)
        .apply(reparar) 
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
        .str.title()
    )

    return df_excel_libros


## Estadísticas descriptivas con NumPy (ayuda IA)

def estadisticas_descriptivas(df):
    """Calcula estadísticas descriptivas para columnas numéricas."""
    print("\n" + "="*50)
    print("ESTADÍSTICAS DESCRIPTIVAS")
    print("="*50)
    
    columnas_numericas = df.select_dtypes(include=[np.number]).columns # Imprime una carátula e identifica automáticamente qué columnas del DataFrame son de tipo numérico (int, float) mediante select_dtypes.
    
    for col in columnas_numericas:
        print(f"\n{col.upper()}:")
        print(f"  Media: {np.mean(df[col]):.2f}")
        print(f"  Mediana: {np.median(df[col]):.2f}")
        print(f"  Desviación estándar: {np.std(df[col]):.2f}")
        print(f"  Mínimo: {np.min(df[col]):.2f}")
        print(f"  Máximo: {np.max(df[col]):.2f}")
        print(f"  Q1 (25%): {np.percentile(df[col], 25):.2f}")
        print(f"  Q3 (75%): {np.percentile(df[col], 75):.2f}") # Itera sobre cada columna numérica e imprime sus métricas estadísticas clave calculadas con funciones puras de NumPy (np.mean, np.median, np.std, np.min, np.max, np.percentile).
    
    return df


def detectar_outliers(df):
    """Detecta y trata valores anómalos (outliers) usando el método IQR."""
    print("\n" + "="*50)
    print("DETECCIÓN DE OUTLIERS (IQR)")
    print("="*50)
    
    columnas_numericas = df.select_dtypes(include=[np.number]).columns
    
    for col in columnas_numericas:
        Q1 = np.percentile(df[col], 25)
        Q3 = np.percentile(df[col], 75)
        IQR = Q3 - Q1
        
        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR
        
        outliers = df[(df[col] < limite_inferior) | (df[col] > limite_superior)] # Filtra las filas que se encuentran fuera de los límites superior e inferior.
        
        if len(outliers) > 0:
            print(f"\n{col.upper()}: {len(outliers)} outliers detectados")
            print(f"  Rango válido: [{limite_inferior:.2f}, {limite_superior:.2f}]")
            # Reemplazar outliers por la mediana
            mediana = np.median(df[col])
            df.loc[(df[col] < limite_inferior) | (df[col] > limite_superior), col] = mediana
            print(f"  Reemplazados por la mediana: {mediana:.2f}")
        else:
            print(f"\n{col.upper()}: Sin outliers detectados") # Si se encuentran atípicos, imprime el número de detección, calcula la mediana de la columna con np.median y sobreescribe los valores atípicos con esa mediana usando .loc[...].
    
    return df


def generar_columnas_derivadas(df):
    """Genera columnas derivadas a partir de los datos existentes."""
    print("\n" + "="*50)
    print("GENERANDO COLUMNAS DERIVADAS")
    print("="*50)
    
    # Para préstamos
    if 'dias_prestamo' in df.columns:
        # Categoría de duración del préstamo
        df['categoria_duracion'] = pd.cut(
            df['dias_prestamo'],
            bins=[0, 14, 30, np.inf],
            labels=['Corto (≤14 días)', 'Medio (15-30 días)', 'Largo (>30 días)']
        )
        print("\n✓ Columna 'categoria_duracion' creada") # Evalúa si la columna dias_prestamo existe en el DataFrame. Si es así, utiliza pd.cut() para segmentar/discretizar la variable numérica en rangos o "bins":
    
    if 'dias_retraso' in df.columns:
        # Categoría de retraso
        df['tiene_retraso'] = df['dias_retraso'] > 0 # Crea un indicador booleano (True/False) llamado tiene_retraso.
        df['categoria_retraso'] = pd.cut(
            df['dias_retraso'],
            bins=[-0.1, 0, 7, 30, np.inf],
            labels=['Sin retraso', 'Retraso leve (1-7 días)', 'Retraso medio (8-30 días)', 'Retraso grave (>30 días)']
        ) # Agrupa los días de morosidad en 4 categorías cualitativas usando pd.cut() (Sin retraso, Leve, Medio y Grave).
        print("✓ Columnas 'tiene_retraso' y 'categoria_retraso' creadas")
    
    if 'perfil_socio' in df.columns and 'tiene_retraso' in df.columns:
        # Combinación de perfil y retraso
        df['perfil_riesgo'] = df['perfil_socio'] + ' - ' + df['tiene_retraso'].map({True: 'Con retraso', False: 'Sin retraso'}) # Mapea los valores booleanos (True/False) a cadenas ('Con retraso'/'Sin retraso') y los concatena con el perfil del usuario para generar una nueva etiqueta de clasificación.
        print("✓ Columna 'perfil_riesgo' creada")
    
    return df