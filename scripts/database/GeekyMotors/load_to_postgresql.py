import os
import pandas as pd
import psycopg2

# Ruta del archivo CSV
FILES_PATH = os.path.join('data', 'processed', 'GeekyMotors')
csv_path = os.path.join(FILES_PATH, 'geeky_transformed.csv')

# Importación del archivo CSV
df = pd.read_csv(csv_path, encoding="utf-8")

# Reemplaza los valores por tus credenciales
usuario = 'postgres'
contraseña = 'base'
host = 'localhost'
puerto = '5432'
nombre_bd = 'geekymotors'

# Conexión a la base de datos
conn = psycopg2.connect(
    dbname=nombre_bd,
    user=usuario,
    password=contraseña,
    host=host,
    port=puerto
)
cur = conn.cursor()

# Función para insertar filas en la tabla
def insert_data(df, table_name, cur):
    # Crear la consulta SQL de inserción dinámica
    columns = ', '.join(df.columns)
    values = ', '.join(['%s'] * len(df.columns))
    
    # Consulta para insertar solo si el registro no existe
    insert_query = f"""
    INSERT INTO {table_name} ({columns}) 
    SELECT {values} 
    WHERE NOT EXISTS (
        SELECT 1 FROM {table_name} WHERE {" AND ".join([f"{col} = %s" for col in df.columns])}) 
    ) RETURNING id;"""

    # Insertar los datos fila por fila y obtener el ID de la fila insertada
    ids = []
    for row in df.itertuples(index=False, name=None):
        cur.execute(insert_query, row + row)  # Duplicamos 'row' para el WHERE
        id_insertado = cur.fetchone()
        if id_insertado:  # Si se insertó una fila, agregar el ID
            ids.append(id_insertado[0])  # Obtener el ID insertado
    return ids

# Renombrar la columna 'asientos' a 'asiento_material'
df.rename(columns={'asientos': 'asiento_material'}, inplace=True)

# Cargar los datos en las tablas correspondientes
df_marca = df[['marca']].drop_duplicates().copy()
df_detalles = df[['modelo', 'kilometraje', 'color', 'asiento_material', 'verificacion', 'precio']].copy()
df_anio = df[['anio']].drop_duplicates().copy()
df_combustible = df[['combustible']].drop_duplicates().copy()
df_transmision = df[['transmision']].drop_duplicates().copy()
df_traccion = df[['traccion']].drop_duplicates().copy()
df_carroceria = df[['carroceria']].drop_duplicates().copy()

# Insertar datos en las tablas de referencia y obtener los IDs
marca_ids = insert_data(df_marca, 'marca', cur)
anio_ids = insert_data(df_anio, 'anio', cur)
combustible_ids = insert_data(df_combustible, 'combustible', cur)
transmision_ids = insert_data(df_transmision, 'transmision', cur)
traccion_ids = insert_data(df_traccion, 'traccion', cur)
carroceria_ids = insert_data(df_carroceria, 'carroceria', cur)

# Ahora, insertar en la tabla detalles
# Agregar las IDs correspondientes al DataFrame
df_detalles['id_marca'] = marca_ids[0] if marca_ids else None  # Asumiendo que solo hay una marca
df_detalles['id_anio'] = anio_ids[0] if anio_ids else None    # Asumiendo que solo hay un año

# Aquí debes mapear las IDs de combustible, tracción, transmisión y carrocería según tus datos
# Por simplicidad, estoy asumiendo que hay solo un valor por cada uno de estos
df_detalles['id_combustible'] = combustible_ids[0] if combustible_ids else None
df_detalles['id_transmision'] = transmision_ids[0] if transmision_ids else None
df_detalles['id_traccion'] = traccion_ids[0] if traccion_ids else None
df_detalles['id_carroceria'] = carroceria_ids[0] if carroceria_ids else None

# Inserta en detalles
insert_data(df_detalles, 'detalles', cur)

# Confirmar los cambios y cerrar la conexión
conn.commit()
cur.close()
conn.close()
