import uvicorn
import psycopg2
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Get SEPOMEX Data"}


@app.get("/search-by-cp/")
async def root(cp: str = '01001'):
    try:
        conn = psycopg2.connect(
            database="railway",
            user='postgres',
            password='OoYIQGsQKPQwpk1g8lT3',
            host='containers-us-west-186.railway.app',
            port= '6502'
        )

        cursor = conn.cursor()
        query='''
            SELECT colonia, colonia.cp, mnpio, estado
            FROM colonia
            INNER JOIN municipio ON colonia.cp = municipio.cp
            INNER JOIN estado ON colonia.c_estado = estado.c_estado
            WHERE colonia.cp = '{0}';
        '''.format(str(cp))
        cursor.execute(query)
        response = cursor.fetchall()
        conn.commit()
        conn.close()
        
        return {
            "data": response
        }
    except:
        return {
            'error': 'error durante la busqueda'
        }
    finally:
        conn.close()


@app.get("/search-by-text/")
async def root(colonia = '', municipio = '', estado = ''):
    try:
        conn = psycopg2.connect(
            database="railway",
            user='postgres',
            password='OoYIQGsQKPQwpk1g8lT3',
            host='containers-us-west-186.railway.app',
            port= '6502'
        )

        if colonia != '':
            query='''
                SELECT colonia, colonia.cp, mnpio, estado
                FROM colonia
                INNER JOIN municipio ON colonia.cp = municipio.cp
                INNER JOIN estado ON colonia.c_estado = estado.c_estado
                WHERE colonia.colonia LIKE '%{}%';
            '''.format(colonia)
        elif municipio != '':
            query='''
                SELECT mnpio, mnpio.cp, estado
                FROM municipio
                INNER JOIN estado ON municipio.c_estado = estado.c_estado
                WHERE municipio.municipio LIKE '%{}%'
                LIMIT 100;
            '''.format(municipio)
        elif estado != '':
            query='''
                SELECT estado
                FROM estado
                WHERE estado.estado LIKE '%{}%';
            '''.format('Gu')
        else:
            return {
                'error': 'Puede buscar por colonia, municipio o estado'
            }

        cursor = conn.cursor()
        cursor.execute(query)
        response = cursor.fetchall()
        conn.commit()
        conn.close()
        
        return {
            "data": response
        }
    except:
        return {
            'error': 'error durante la busqueda parcial'
        }
    finally:
        conn.close()

@app.post("/add-new-colonia/")
async def root(colonia, estado, mnpio):
    try:
        conn = psycopg2.connect(
            database="railway",
            user='postgres',
            password='OoYIQGsQKPQwpk1g8lT3',
            host='containers-us-west-186.railway.app',
            port= '6502'
        )
        # Verificar estado y municipio validos
        # Verificar estado
        cursor = conn.cursor()

        query='''
            SELECT c_estado
            FROM estado
            WHERE estado = '{0}';
        '''.format(str(colonia))
        cursor.execute(query)
        response = cursor.fetchall()
        conn.commit()
        if len(response) == 0:
            return {
                "error": 'Estado no encontrado, favor de utilizar un estado valido'
            }
        else:
            c_estado = response[0][0]

        # Verificar municipio
        query='''
            SELECT cp
            FROM municipio
            WHERE mnpio = '{0}';
        '''.format(str(mnpio))
        cursor.execute(query)
        response = cursor.fetchall()
        conn.commit()
        if len(response) == 0:
            return {
                "error": 'Municipio no encontrado, favor de utilizar un municipio valido valido'
            }
        else:
            cp = response[0][0]
        
        # Insertar elemento a la base de datos
        query = '''
            INSERT INTO colonia (colonia, cp, c_estado)
            VALUES(%s, %s, %s);
        '''
        values = (colonia, cp, c_estado)
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        
        
        return {
            "data": response
        }
    except:
        return {
            'error': 'error durante la insercion'
        }
    finally:
        conn.close()

if __name__ == '__main__':
    try:
        uvicorn.run(
            "main:app",
            host='0.0.0.0',
            port=6757,
        )
    finally:
        conn.close()