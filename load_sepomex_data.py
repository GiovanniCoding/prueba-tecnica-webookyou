import pandas as pd

from sqlalchemy import create_engine

def processing_sepomex_data(file):
    # Cargar los datos a un DataFrame
    df = pd.read_csv(
        file,
        encoding='latin1',
        sep='|',
        header=0,
        skiprows=[0]
    )

    def _upload_sepomex(df, table):
        engine = create_engine('postgresql://postgres:OoYIQGsQKPQwpk1g8lT3@containers-us-west-186.railway.app:6502/railway')
        df.to_sql(table, engine, if_exists='replace')

    # Limpiar los datos de los estados y subirlos a la base de datos
    df_estado = df[['c_estado', 'd_estado']].drop_duplicates().reset_index(drop=True)
    df_estado = df_estado.rename(
        columns={
            "d_estado": "estado"
        }
    )
    _upload_sepomex(df_estado, 'estado')

    # Limpiar los datos de los municipios y subirlos a la base de datos
    df_municipio = df[['c_mnpio', 'D_mnpio']].drop_duplicates().reset_index(drop=True)
    df_municipio = df_municipio.rename(
        columns={
            "D_mnpio": "mnpio"
        }
    )
    _upload_sepomex(df_municipio, 'municipio')

    # Limpiar los datos de las colonias y subirlos a la base de datos
    df_colonia = df[['d_asenta', 'd_CP', 'c_estado', 'c_mnpio']].drop_duplicates().reset_index(drop=True)
    df_colonia = df_colonia.rename(
        columns={
            "d_asenta": "colonia",
            "d_CP": "cp"
        }
    )
    _upload_sepomex(df_colonia, 'colonia')

if __name__ == '__main__':
    # PATH al archivo de SEPOMEX en formato txt
    file = 'sepomex/CPdescarga.txt'
    processing_sepomex_data(file)
