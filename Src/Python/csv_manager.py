import os
import csv
import shutil

CARPETA_CSV = "../data/csv"

"""
la idea es que este código se use al inicio o al reiniciar el sistema, para crear las carpetas de data y csv y para los crear archivos .csv desde 0.
este código tiene que recibir dos listas. una de objetivos en los que centrarse (carbohidratos, agua, etc) que contiene strings, 
y una de cuanto quiero tener de cada (para agua 3 litros, por ejemplo), el cual contiene integers.
a partir de estos, crea objetivos.csv, historial.csv(vacío, excepto por los objetivos), y estado.csv(vacío)
"""
def inicializar_sistema(objetivos = list, valores = list):
    
    #Esto me verifica si las carpetas existen. Si no, las crea y no tira error (makedirs es, lo de exist_ok es lo que me evita el error)
    os.makedirs(CARPETA_CSV, exist_ok=True)

    #Esto crea el archivo o lo sobreescribe (la w) y el newline es para que no queden lineas al pedo. "f" se usa por convención, significa "file" (archivo en inglés)
    with open(CARPETA_CSV + "/objetivos.csv", "w", newline="") as f:
        #creo la herramienta writer, como si fuera una variable (le pongo writer, pero le puedo poner como quiera)
        writer = csv.writer(f)
    
        #uso la herramienta writer para escribir en la primera linea
        writer.writerow(objetivos)
        #uso la herramienta writer para escribir en la segunda linea (writerow la pasa sola)
        writer.writerow(valores)

    #creo el archivo de historial
    with open(CARPETA_CSV + "/historial.csv", "w", newline="") as f:
        #defino writer
        writer = csv.writer(f)
    
        #como primera fila, defino las columnas
        writer.writerow(["dia"] + objetivos)

    #creo el archivo de estado, pero solo le pongo la fila 1, para definir la columna "dia"
    with open(CARPETA_CSV + "/estado.csv", "w", newline="") as f:
        #defino writer
        writer = csv.writer(f)
    
        #como primera fila, defino las columnas
        writer.writerow(["dia"])
        
        #como segunda fila, indico que es el día 1
        writer.writerow([1])


"""
esta función recibe los datos del día cuando se pasa de día y agrega todos estos datos a los csv correspondientes. debe recibir una lista (datos_dia)
"""
def registrar_dia(datos_dia = list):
    #abro el archivo estado.csv, pero solo para leerlo (la "r"). esto es para sacar que día es
    with open(CARPETA_CSV + "/estado.csv", "r", newline="") as f:
        #reader es una lista de listas, la cual sería [[dia], [1]] en este caso, así que tengo que sacar el dato de que dia es nomás
        reader = csv.reader(f)
        
        #guardo el reader como una variable
        filas = list(reader)
        
        #guardo el día en una variable
        dia_actual = int(filas[1][0])
    
    #ahora que sé que día es, modifico el archivo de historial para meter el día de hoy. acá va una "a" y no una "w" por que no estoy sobreescribiendo, sino agregando una fila nueva
    with open(CARPETA_CSV + "/historial.csv", "a", newline= "") as f:
        #defino writer
        writer = csv.writer(f)
        
        #escribo una nueva fila
        writer.writerow([dia_actual] + datos_dia)
    
    #avanzo un día, modificandolo, así que va la "w"
    with open(CARPETA_CSV + "/estado.csv", "w", newline="") as f:
        #defino el writer
        writer = csv.writer(f)
        
        #mantengo la fila 1
        writer.writerow(["dia"])
        
        #sobreescribo la fila 2
        writer.writerow([dia_actual + 1])

"""
este código devuelve una lista de diccionarios con el historial completo. cada diccionario es una fila y cada clave es una columna 
"""
def leer_historial():
    #creo la lista para devolver
    lista_devolucion = []
    
    #abro el archivo de historial
    with open(CARPETA_CSV + "/historial.csv", "r") as f:
        #defino reader
        reader = csv.reader(f)
        
        #guardo el reader como una variable
        filas = list(reader)
        
        #esto es un quilombo, pero basicamente creo una lista de diccionarios en la que cada diccionario es un dia (no se como anda pero anda, no lo toquen porfa, me salio a la primera)
        for lista in filas:
            if lista != filas[0]:
                diccionario = {}
                num_dato = 0
                for dato in lista:
                    diccionario[filas[0][num_dato]] = lista[num_dato]
                    num_dato += 1
                lista_devolucion.append(diccionario)
        
        #devuelvo la lista de diccionarios
        return lista_devolucion

"""
esto devuelve un diccionario con los objetivos puestos por el usuario al inicio
"""
def leer_objetivos():
    #abro el archivo de objetivos
    with open(CARPETA_CSV + "/objetivos.csv", "r") as f:
        #defino reader
        reader = csv.reader(f)
        
        #guardo el reader como una variable
        filas = list(reader)
        
        diccionario = {}
        
        for num_dato in range(len(filas[0])):
            diccionario[filas[0][num_dato]] = int(filas[1][num_dato])
        
        return diccionario

"""
esto devuelve una lista de diccionarios de diccionarios que comparan todos los datos recibidos con los objetivos y devuelve  algo así:
[
    {
        "dia": 1,
        "calorias": {"real": 350, "objetivo": 400, "cumplido": False},
        "agua": {"real": 4000, "objetivo": 3000, "cumplido": True}
    }
    
    {
        "dia": 2,
        "calorias": {"real": 450, "objetivo": 400, "cumplido": True},
        "agua": {"real": 2500, "objetivo": 3000, "cumplido": False}
    }
]
"""
def comparar_historial_objetivos():
    
    #creo un diccionario para poner todas las comparaciones
    lista_mayor = []
    
    #abro el archivo de historial para saber el día
    with open(CARPETA_CSV + "/historial.csv", "r") as f_historial:
        
        #defino reader del historial
        reader_historial = csv.reader(f_historial)
        
        #guardo el reader del historial como una variable
        filas_historial = list(reader_historial)
        
        #creo la variable dias para ver cuantos días hay
        dias = len(filas_historial)
        
        #itero por día que pasa
        for num_dia in range(1, dias):
            
            #creo un diccionario para poner todas las comparaciones del día
            diccionario_mayor = {}
            
            #agrego al diccionario el día a ver
            diccionario_mayor["dia"] = int(filas_historial[num_dia][0])

            #abro el archivo de los objetivos
            with open(CARPETA_CSV + "/objetivos.csv", "r") as f_objetivos:
                
                #defino reader de los objetivos
                reader_objetivos = csv.reader(f_objetivos)
            
                #guardo el reader de los objetivos como una variable
                filas_objetivos = list(reader_objetivos)
                
                #comparo uno por uno cada objetivo y lo agrego al diccionario
                for num_objetivo in range(len(filas_objetivos[0])):
                    
                    #creo un diccionario solo para este objetivo
                    diccionario_local = {}
                    
                    #agrego al diccionario local el valor real de este objetivo
                    diccionario_local["real"] = int(filas_historial[num_dia][num_objetivo + 1])
                    
                    #agrego al diccionario local el valor que queríamos tener en este objetivo
                    diccionario_local["objetivo"] = int(filas_objetivos[1][num_objetivo])
                    
                    #veo si se cumplió o no el objetivo (si el real es mayor al objetivo)
                    diccionario_local["cumplido"] = diccionario_local["real"] >= diccionario_local["objetivo"]
                    
                    #meto al diccionario de este día las comparaciones de este objetivo
                    diccionario_mayor[filas_objetivos[0][num_objetivo]] = diccionario_local

            #le meto el diccionario de este dia a la lista
            lista_mayor.append(diccionario_mayor)
    
    return lista_mayor


"""
este codigo elimina toda la carpeta data e inicializa el sistema con valores que se le ingresan
"""
def restaurar(objetivos = list, valores = list):
    if os.path.exists("../data"):
        shutil.rmtree("../data")
    
    inicializar_sistema(objetivos, valores)

"""
este codigo lee el historial y devuelve el promedio cumplido (promedio de agua tomada por dia, promedio de carbohidratos ingeridos por dia) en un diccionario 
por ejemplo: 
{
    "calorias": 405,
    "agua": 3250,
    "sueno": 8
}
"""
def promedio(historial):
    
    #creo una variable para indicar cauntos días procesé
    dia_actual = 0
    
    #creo el diccionario para devolver lleno
    dicc_promedio = {}
    
    #leo solo un dia del historial
    for dia in historial:
        
        #leo especificamente cada dato de ese día
        for clave in dia:
            
            #garantizo que ignore el día que es, ya que es un promedio
            if clave != "dia":
                
                #si ya hay una clave de este dato en el diccionario, se lo sumo, si no lo creo
                if clave not in dicc_promedio:
                    dicc_promedio[clave] = dia[clave]
                else:
                    dicc_promedio[clave] = dicc_promedio[clave] + dia[clave]
        
        #paso al siguiente día, para saber cuantos pasé al final
        dia_actual += 1
    
    #calculo el promedio por cada categoría
    for clave in dicc_promedio:
        dicc_promedio[clave] = dicc_promedio[clave] // dia_actual
    
    return dicc_promedio

"""
este código devuelve el porcentaje de cumplimiento de cada categoría en forma de diccionario.
ejemplo:
{
  "calorias": 50,
  "agua": 100,
  "sueno": 100
}
"""
def porcentaje_cumplimiento():
    #uso la funcion de comparar para obtener la lista de diccionarios ya armada
    comparaciones = comparar_historial_objetivos()
    
    #este cuenta la cantidad de cumplimientos totales de cada caracteistica
    diccionario_cumplimiento = {}
    
    #creo un diccionario para devolver
    diccionario_porcentajes = {}
    
    total_dias = len(comparaciones)
    
    #miro cada diccionario en comparaciones
    for diccionario_dia in comparaciones:
        
        #miro cada diccionario menos el de día (por que no lo necesito)
        for clave  in diccionario_dia:
            
            #verifico que no sea el día
            if clave != "dia":
                if clave not in diccionario_cumplimiento:
                    diccionario_cumplimiento[clave] = 0
                
                if diccionario_dia[clave]["cumplido"]:
                    diccionario_cumplimiento[clave] += 1
    
    # calcular porcentajes
    for clave in diccionario_cumplimiento:
        diccionario_porcentajes[clave] = int(
            (diccionario_cumplimiento[clave] / total_dias) * 100
        )
    
    return diccionario_porcentajes