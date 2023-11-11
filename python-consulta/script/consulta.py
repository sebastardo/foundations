import pandas as pd
from sqlalchemy import create_engine
import time

def motor():
    
    parametros = {
        'user' : "admin",
        'password' : "admin",
        'host' : "postgres",
        'port' : "5432",
        'database' : "arboleda"
    }

    time.sleep(60)

    engine = create_engine(
                'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
                    parametros['user'],
                    parametros['password'],
                    parametros['host'],
                    parametros['port'],
                    parametros['database']
                    )
                )
    
    return engine.connect()



def consulta(sql_cmd, engine):
    return pd.read_sql(sql=sql_cmd, con=engine)


def prociento(texto):
    return texto+'%'


def main():
    
    pd.options.display.max_colwidth = 50
    
    linea = '═'*80

    
    engine = motor()

    #######################
    # pregunta 1 y titulo #
    #######################
    
    sql_consulta ='''
    SELECT
        e.nombre_comun, 
        COUNT(a.id_arbol) as cantidad 
    FROM arbol a
    JOIN especie e on a.id_especie = e.id_especie
    group by e.nombre_comun
    '''

    df = consulta(sql_consulta, engine)    
    

    print('''
    ╔═══════════════════════════════════════════════╗
    ║      ARBOLEDA DE LA CIUDAD DE BUENOS AIRES    ║
    ║ La Ciudad de Buenos Aires posee {0} árboles ║
    ║       distribuidos en diferentes parques      ║
    ╚═══════════════════════════════════════════════╝
    '''.format(df['cantidad'].sum())
    )

    df['porcentaje'] = ((df['cantidad'] / df['cantidad'].sum()) * 100).apply(lambda x:round(x,2)).astype(str).apply(prociento)
    print('Especies de arboles mas frecuentes')
    print(linea)
    
    print(df.sort_values(by='cantidad', ascending=False).head(10))

    ##############
    # pregunta 2 #
    ##############
    print(linea + '\n\n')
    print('Espacios verdes con mayor cantidad de especies exoticas y la mas predominante')
    print(linea)


    sql_consulta = '''
    select 
        e.nombre_comun, 
        u.espacio_verde, 
        count(e.nombre_comun) as cantidad 
    from arbol a
    join especie e on a.id_especie = e.id_especie
    join origen o on e.id_origen = o.id_origen
    join ubicacion u on a.id_ubicacion = u.id_ubicacion
    where o.origen = 'Exótico'
    group by u.espacio_verde, e.nombre_comun;
    '''
    df = consulta(sql_consulta, engine)

    total_por_esp_verde = df.groupby('espacio_verde')['cantidad'].sum()
    predominante = df[df.groupby('espacio_verde')['cantidad'].transform(max) == df['cantidad']]

    predominante = predominante[['espacio_verde', 'nombre_comun']]

    resultado = pd.merge(total_por_esp_verde,predominante, left_on='espacio_verde', right_on='espacio_verde')
    resultado = resultado.rename(columns={'espacio_verde': 'espacio verde', 'cantidad':'total de exóticos', 'nombre_comun':'arbol predominante'})

    print(resultado)


    ##############
    # pregunta 3 #
    ##############
    print(linea + '\n\n')
    print('Ubicación de arboles de especie nativa de mayor altura')
    print(linea)

    sql_consulta = '''
    SELECT 
        a.id_arbol,
        a.id_ubicacion,
        e.nombre_comun,
        e.nombre_cientifico,
        a.long,
        a.lat,
        a.coord_x,
        a.coord_y,
        a.altura_total
    FROM arbol a
    JOIN especie e ON a.id_especie = e.id_especie
    JOIN origen o ON e.id_origen = o.id_origen 
    WHERE o.origen = 'Nativo/Autóctono'
    '''
    arbol = consulta(sql_consulta, engine)

    sql_consulta = 'SELECT * FROM ubicacion'
    ubicacion = consulta(sql_consulta, engine)


    ubicacion_arbol = pd.merge(
        ubicacion,
        arbol,
        left_on='id_ubicacion',
        right_on='id_ubicacion'
        )[
            [
            'altura_total',
            'nombre_comun',
            'nombre_cientifico',
            'long',
            'lat',
            'coord_x',
            'coord_y',
            'espacio_verde',
            'ubicacion'
            ]
        ]

    print(ubicacion_arbol.sort_values(by='altura_total', ascending=False).head(10))

    ##############
    # pregunta 4 #
    ##############
    print(linea + '\n\n')
    print('Follaje predominante de todo el arbolado')
    print(linea)

    sql_consulta = 'SELECT id_arbol, id_follaje FROM arbol'
    arbol = consulta(sql_consulta, engine)

    sql_consulta = 'SELECT * FROM follaje'
    follaje = consulta(sql_consulta, engine)


    follaje_arbol = pd.merge(follaje,arbol, left_on='id_follaje', right_on='id_follaje')
    df = follaje_arbol.groupby(['tipo_follaje'])['id_arbol'].count().reset_index(name='Cantidad de arboles')
    df = df.sort_values(by=['Cantidad de arboles'], ascending=False).reset_index()
    print(df['tipo_follaje'].head(3))

    ##############
    # pregunta 5 #
    ##############
    print(linea + '\n\n')
    print('Espacios verdes mas poblados')
    print(linea)

    sql_consulta = 'SELECT * FROM ubicacion'
    ubicacion = consulta(sql_consulta, engine)

    sql_consulta = 'SELECT id_arbol, id_ubicacion FROM arbol'
    arbol = consulta(sql_consulta, engine)


    ubicacion_arbol = pd.merge(ubicacion,arbol, left_on='id_ubicacion', right_on='id_ubicacion')
    df = ubicacion_arbol.groupby(['espacio_verde','ubicacion'])['id_arbol'].count().reset_index(name='Cantidad de arboles')

    print(df.sort_values(by=['Cantidad de arboles'], ascending=False).reset_index().head(5))




if __name__ == '__main__':
    main()
