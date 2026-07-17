from lib.limpieza import (
    limpieza_generos,
    limpieza_dias_retraso,
    comentario,
    limpieza_dias_prestamo,
    limpieza_perfil_socio,
    normalizacion_id_prestamo,
    limpieza_generos_l,
    id_libro,
    df_excel_libros,
    df_excel_prestamos
)

import pandas as pd

df_excel_libros_limpio=limpieza_generos_l(df_excel_libros)
df_excel_libros_limpio=id_libro(df_excel_libros)
print('='*20)
df_excel_prestamos_limpio=limpieza_generos(df_excel_prestamos)
df_excel_prestamos_limpio=limpieza_dias_prestamo(df_excel_prestamos)
df_excel_prestamos_limpio=limpieza_dias_retraso(df_excel_prestamos)
df_excel_prestamos_limpio=comentario(df_excel_prestamos)
df_excel_prestamos_limpio=limpieza_perfil_socio(df_excel_prestamos)
df_excel_prestamos_limpio=normalizacion_id_prestamo(df_excel_prestamos)

# print(df_excel_prestamos)
# print(df_excel_libros)

print(df_excel_prestamos_limpio)
print(df_excel_libros_limpio)