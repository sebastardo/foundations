import urllib.request
from io import StringIO
import pandas as pd
from sqlalchemy import create_engine


def descarga_archivo():
    url = 'https://cdn.buenosaires.gob.ar/datosabiertos/datasets/arbolado-en-espacios-verdes/arbolado-en-espacios-verdes.csv'

    respuesta = urllib.request.urlopen(url)
    f = StringIO(bytearray(respuesta.read()).decode())
    df = pd.read_csv(f)

    return df


def motor():
    
    parametros = {
        'user' : "admin",
        'password' : "admin",
        'host' : "postgres",
        'port' : "5432",
        'database' : "arboleda"
    }

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


def carga_de_datos():

    arboles = descarga_archivo()
    engine = motor()


    ''' Creacion de dataframes '''
    # familia
    familia = pd.DataFrame(arboles[~arboles['nombre_fam'].duplicated()]['nombre_fam'])
    familia['id_familia'] = list(range(1,familia.shape[0]+1))

    # genero
    genero = pd.DataFrame(arboles[~arboles['nombre_gen'].duplicated()][{'nombre_gen', 'nombre_fam'}])
    genero = pd.merge(genero, familia, left_on='nombre_fam', right_on='nombre_fam')[{'nombre_gen','id_familia'}]
    genero['id_genero'] = list(range(1,genero.shape[0]+1))

    # origen
    origen = pd.DataFrame(arboles[~arboles['origen'].duplicated()]['origen'])
    origen['id_origen'] = list(range(1,origen.shape[0]+1))
    
    # follaje
    follaje = pd.DataFrame(arboles[~arboles['tipo_folla'].duplicated()]['tipo_folla'])
    follaje['id_follaje'] = list(range(1,follaje.shape[0]+1))


    # ubicacion
    ubicacion = pd.DataFrame(arboles[~arboles['espacio_ve'].duplicated()][{'espacio_ve','ubicacion'}])
    ubicacion['id_ubicacion'] = list(range(1,ubicacion.shape[0]+1))
    
    
   # especie
    especie = pd.DataFrame(arboles[~arboles['id_especie'].duplicated()][{'id_especie','nombre_com','nombre_cie','nombre_gen','origen'}])
    especie = pd.merge(especie, genero, left_on='nombre_gen', right_on='nombre_gen')[{'id_especie','nombre_com','nombre_cie','id_genero', 'origen'}]
    especie = pd.merge(especie, origen, left_on='origen', right_on='origen')[{'id_especie','nombre_com','nombre_cie','id_genero','id_origen'}]


    # arbol
    arbol = arboles[{'long', 'lat', 'id_arbol', 'altura_tot', 'diametro', 'inclinacio',
                    'id_especie',
                    'tipo_folla', 
                    'espacio_ve',
                    'origen', 'coord_x','coord_y'}]
                                                                                
    arbol = pd.merge(arbol,
                    ubicacion, 
                    left_on='espacio_ve', 
                    right_on='espacio_ve'
                    )[{'long', 
                        'lat', 
                        'id_arbol', 
                        'altura_tot', 
                        'diametro', 
                        'inclinacio',
                        'id_especie',
                    'tipo_folla', 
                        'id_ubicacion',
                        'coord_x',
                        'coord_y'}]




    arbol = pd.merge(arbol, 
                    follaje, 
                    left_on='tipo_folla', 
                    right_on='tipo_folla'
                    )[{'long', 
                        'lat', 
                        'id_arbol', 
                        'altura_tot', 
                        'diametro', 
                        'inclinacio',
                        'id_especie',
                        'id_follaje', 
                        'id_ubicacion',
                        'coord_x',
                        'coord_y'}]
    



    ''' Cambio de nombre de columnas '''
    ubicacion = ubicacion.rename(columns={"espacio_ve":"espacio_verde"})
    especie = especie.rename(columns={"nombre_com":"nombre_comun", "nombre_cie":"nombre_cientifico"})
    arbol = arbol.rename(columns={"altura_tot":"altura_total","inclinacio":"inclinacion"})
    follaje = follaje.rename(columns={"tipo_folla":"tipo_follaje"})
    familia = familia.rename(columns={"nombre_fam":"nombre_familia"})
    genero = genero.rename(columns={"nombre_gen":"nombre_genero"})
    
    



    ''' Carga en base '''
    familia.to_sql('familia', con=engine, if_exists='append', index=False)
    origen.to_sql('origen', con=engine, if_exists='append', index=False)
    follaje.to_sql('follaje', con=engine, if_exists='append', index=False)
    genero.to_sql('genero', con=engine, if_exists='append', index=False)
    ubicacion.to_sql('ubicacion', con=engine, if_exists='append', index=False)
    especie.to_sql('especie', con=engine, if_exists='append', index=False)
    arbol.to_sql('arbol', con=engine, if_exists='append', index=False)
    

if __name__ == '__main__':
    print('Cargando datos...')
    carga_de_datos()
    print('Datos cargados')
    