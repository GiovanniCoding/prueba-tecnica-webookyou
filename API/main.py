import jwt
from datetime import datetime, timedelta, timezone

import uvicorn
import psycopg2
from fastapi import FastAPI

app = FastAPI()
key = "egiovanni"


@app.get("/")
async def root():
    return {"message": "Get SEPOMEX Data"}


@app.get("/generate-user/")
async def root(user = ''):
    try:
        if user == '':
            return {"error": "Necesita proporcionar user para poder generar una key"}
        token = jwt.encode(
            {
                'Username': user,
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=15)
            },
            key,
            algorithm="HS256"
        )
        return {"key": token}
    except:
        return {"error": "Error en la generacion de la key"}


@app.get("/search-by-cp/")
async def root(token = '', cp: str = '01001'):
    try:
        try:
            jwt.decode(token, key, algorithms="HS256")
        except:
            return {"error": "Token invalido, favor de verificar"}

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
        try:
            conn.close()
        except:
            print('La conexion ya fue cerrada')


@app.get("/search-by-text/")
async def root(token = '', colonia = '', municipio = '', estado = ''):
    jwt.decode(token, key, algorithms="HS256")
    try:
        try:
            jwt.decode(token, key, algorithms="HS256")
        except:
            return {"error": "Token invalido, favor de verificar"}

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
        try:
            conn.close()
        except:
            print('La conexion ya fue cerrada')

@app.post("/add-new-colonia/")
async def root(token = '', colonia = '', estado = '', mnpio = ''):
    try:
        try:
            jwt.decode(token, key, algorithms="HS256")
        except:
            return {"error": "Token invalido, favor de verificar"}

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
        try:
            conn.close()
        except:
            print('La conexion ya fue cerrada')

if __name__ == '__main__':
    try:
        uvicorn.run(
            "main:app",
            host='0.0.0.0',
            port=6757,
        )
    finally:
        try:
            conn.close()
        except:
            print('La conexion ya fue cerrada')