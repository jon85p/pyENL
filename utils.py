#/usr/bin/env python3
import random
import os
import appdirs
import sys
import configparser
from translations import translations as pyENL_translations

currentFile_path = os.path.realpath(__file__)
pyENL_dirpath = os.path.dirname(currentFile_path) + os.sep
sys.path.append(pyENL_dirpath)
user_config_dir = appdirs.user_config_dir() + os.sep + "pyENL" + os.sep

'''
Utilidades generales para uso de pyENL
'''
from numpy import *
from pyENL_fcns import *
import re
ln = log
prop = log  # Solo importa el nombre de la función para comprobación...
haprop = log
import copy # recordar que copy entra en conflicto con el copy importado de numpy

from tarjan import tarjan

class configFile:
    '''
    Clase que facilita datos de configuración, su lectura y escritura
    '''

    def __init__(self, pathC):
        '''
        Inicializada con el nombre de archivo que contiene la configuración
        del programa
        '''
        config = configparser.ConfigParser()
        config.read(pathC)
        nuevo = len(config.sections()) == 0
        # Primero verifica que exista el archivo, si no; carga configuración por
        # defecto.
        # items a configurar
        self.items = ["lang", "method"]
        self.lang = 'en'
        self.method = 'hybr'
        self.format = '{:,.3}'
        self.tol = 1e-4
        self.timeout = 10
        self.sFontUI = 'Monospace,12,-1,5,25,0,0,0,0,0'
        self.cuDir = os.path.expanduser('~')
        if nuevo:
            os.makedirs(user_config_dir, exist_ok= True)
            config["GENERAL"] = {
                    "lang": self.lang,
                    "method": self.method,
                    "format": self.format,
                    "tol": self.tol,
                    "theme": "Default",
                    "timeout": self.timeout,
                    "font": self.sFontUI,
                    "cuDir": self.cuDir
                    }
            with open(pathC, "w") as configfile:
                config.write(configfile)
        else:
            # El archivo sí existe, así que vamos a leer
            gen = config["GENERAL"]
            self.lang = gen["lang"]
            self.method = gen["method"]
            self.format = gen["format"]
            self.tol = float(gen["tol"])
            self.timeout = float(gen["timeout"])
            self.sFontUI = gen["font"]
            self.cuDir = gen["cuDir"]


def ajustes(texto):
    '''
    Ajusta el contenido del texto de cada ecuación por si se necesitan hacer
    arreglos, tales como soporte para números en notación científica con
    exponentes negativos
    '''
    pos_e_menos = buscainds(texto, 'e-')
    for posicion in pos_e_menos:
        # Verificar que lo que hay antes y después del e- son números.
        t1 = texto[posicion - 1]
        t2 = texto[posicion + 2]
        try:
            int(t1)  # Comprueba que son números
            int(t2)  # Si no, entonces es excepción y chao
            texto = texto.replace(t1 + 'e-' + t2, t1 + 'e ' + t2)
        except:
            pass
    texto = texto.replace('e ', 'e')
    return texto


def esalfanum(caracter):
    '''Verifica que el caracter es alfanumérico o punto'''
    suma = 0
    suma += (caracter >= '\x30' and caracter <= '\x39')
    suma += (caracter >= '\x41' and caracter <= '\x5a')
    suma += (caracter >= '\x61' and caracter <= '\x7a')
    es_punto = (caracter == '.' or caracter == '_')
    return bool(suma + es_punto)


def buscainds(texto, busq):
    '''Busca los índices de busq dentro de texto'''
    index = []
    end = 0
    res = 0
    while res != -1:
        res = texto.find(busq, end)
        end = res + 1
        index.append(res)
    index.pop(-1)
    return index


def probar(texto_var):
    '''
    Devuelve si texto_var es o no una variable del sistema de ecuaciones
    '''
    try:
        eval(texto_var)
        return False
    except:
        return True


def variables(texto_eqn, return_posibles_vars = False):
    '''
    Regresa:
    - Texto las variables del string texto_eqn
    - Lista de caracteres que posiblemente son variables (opcional)
    '''
    # Reconocer lo que hay entre paréntesis
    # Cambiar todos los nombres de las funciones por números
    #   Buscar las posiciones de "("
    #   Comprobar que el término anterior es número o letra
    #   Retroceder hasta el símbolo anterior de operación o "(" y cortar
    # Cambiar todos los paréntesis por +'s
    # Separar lo que esté separado por símbolos de operación:
    #   + - * / **
    # Cambiar todos los símbolos por +'s
    # Ahora comprobar con la función probar() cada uno de los elementos separados
    # por los +'s
    # Ir agregando los válidos siempre que no se repitan a la lista de salida
    # Return esa lista
    # TODO
    # Eliminar los [unit] para efectos de buscar variables
    texto_eqn = '1*' + texto_eqn
    texto_eqn = ajustes(texto_eqn)
    # print(texto_eqn)
    # Índices donde hay paréntesis open
    parent_abrir = buscainds(texto_eqn, '(')
    # print(parent_abrir)
    cambios = []  # Lista con los cambios a realizar
    for posicion in parent_abrir:
        if posicion > 0:
            # Esto para evitar que se devuelva en la búsqueda
            pos_check = posicion - 1
            if esalfanum(texto_eqn[pos_check]):
                # Se comprueba que es una función
                EsParada = False  # ¿Finalizó el nombre de la función?
                while EsParada == False:
                    # Mientras no sea el comienzo del nombre de la función:
                    pos_check -= 1
                    if pos_check == 0:
                        EsParada == True
                        start_check = 0
                    else:
                        EsParada = not esalfanum(texto_eqn[pos_check])
                        start_check = pos_check + 1
                cambios.append(texto_eqn[start_check:posicion])
    # Ahora se efectúan todos los cambios:
    for cambio in cambios:
        texto_eqn = texto_eqn.replace(cambio, '1+')
    # Acá eliminar lo que hay entre corchetes []
    texto_eqn = re.sub(r'\[[^)]*\]', '', texto_eqn)
    # Reemplazos:
    A_reemplazar = ['(', ')', '-', '*', '/', '^', ',']
    for termino in A_reemplazar:
        texto_eqn = texto_eqn.replace(termino, '+')
    posibles = texto_eqn.split('+')
    # Verificar que cada término es una variable del sistema de ecuaciones
    salida = []
    for variable in posibles:
        if variable != '':
            if probar(variable) == True:
                if variable not in salida:
                    salida.append(variable)

    if return_posibles_vars:
        return salida, posibles
    else:
        return salida


def random_lim(a, b):
    '''
    Número aleatorio entre a y b
    '''
    temp = random.rand()
    salida = a + (b - a) * temp
    return salida


def variables_string(texto):
    '''
    Acomoda el texto para que puedan usarse variables tipo string en el archivo
    de entrada de ecuaciones.
    Las variables de texto se declaran como:
    #ref# = 'R404a'
    '''
    # 1. Identificar las lineas de declaración de estas variables
    # 2. Llevar a cabo los respectivos reemplazos.
    # 3. Eliminar las líneas de declaración
    # 4. Lanzar excepciones si se ven variables que no han sido declaradas
    dicc = {}
    to_del = []
    for i, eqn in enumerate(texto):
        # Asegurarse de que no elimine contenido de comentarios:
        eqn = eqn.split('<<')[0]
        try:
            lista = eqn.split('=')
            if len(lista) == 2 and ('#' == lista[0].replace(' ', '')[0]):
                nombre_var = lista[0]
                nombre_var = nombre_var.replace(' ', '')
                dicc[nombre_var] = lista[1].replace(' ', '')
                to_del.append(i)
        except:
            pass
    for i, num in enumerate(to_del):
        texto.pop(num-i)
    # Segunda iteración para reemplazos
    pattern = re.compile('|'.join(dicc.keys()))
    for i, eqn in enumerate(texto):
        eqn = eqn.split('<<')[0]
        try:
            result = pattern.sub(lambda x: dicc[x.group()], eqn)
            # print(eqn)
            # El reemplazo:
            texto[i] = result
        except:
            pass
    # Ahora la comprobación de que no han quedado $ en las ecuaciones:
    for i, eqn in enumerate(texto):
        eqn = eqn.split('<<')[0]
        if '#' in eqn:
            raise Exception('No se usa bien variable string en ', str(i))
    return texto


def cantidadEqnVar(texto_caja):
    '''
    Regresa la cantidad de ecuaciones y de variables en el texto entero de
    entrada del usuario
    '''
    texto_fcn = variables_string(texto_caja)
    ecuaciones = 0
    lista = []
    for eqn in texto_fcn:
        eqn = eqn.split('<<')[0]
        if ((eqn.replace(' ','').replace('\t', '') != '') and ('{' not in eqn)):
            ecuaciones += 1
            expresion = eqn.replace(" ", "")
            expresion = expresion.replace("\t", "")
            # Capacidad de interpretar pow
            expresion = expresion.replace("^", "**")
            izq_der = expresion.split('=')
            paraRaiz = izq_der[0] + \
                '-(' + izq_der[1] + ')'  # Igualación de cero
            lista.append(paraRaiz)
    lista_vars = []
    dict_vars_properties = {}
    for ecuacion in lista:
        vars_ecuacion, posibles = variables(ecuacion,True)
        vars_eqn_properties = variablesProperties(ecuacion,vars_ecuacion, posibles)
        lista_vars = lista_vars + vars_ecuacion
        dict_vars_properties.update(vars_eqn_properties)
    lista_vars = list(set(lista_vars))
    # Regresa el número de ecuaciones y de variables.

    return ecuaciones, lista_vars, dict_vars_properties

def actualizar_directorio(cuDir):
    '''Guarda en config la ultima ruta de la carpeta donde se abrió o guardó un archivo'''
    # se guarda la ultima carpeta usada para cuando se vuelva a abrir el programa
    config = configparser.ConfigParser()
    config.read(user_config_dir + 'config')
    config['GENERAL']["cuDir"] = cuDir
    with open("config", "w") as configfile:
                config.write(configfile)
    
def funcion_a(Diccionario):
    '''Asociación de ecuaciones con variables (opción aleatoria)'''
    while True:
        lista_claves = tuple(Diccionario.keys())
        Diccionario_aleat = copy.deepcopy(Diccionario)
        lista_claves_check = list(lista_claves)
        for clave in lista_claves:

            try:
                # Se intenta tomar al azar un elemento (variable) de la
                # ecuacion clave
                variable = random.choice(Diccionario_aleat[clave])

            except:  # Si no se puede es porque el contenido de la clave está vacio por lo que se rompe el bucle y se comienza again
                break
            # Para esa clave ahora solo existira el elemento variable
            Diccionario_aleat[clave] = variable
            lista_claves_check.remove(clave)

            for key in lista_claves_check:  # Se borra la variable del resto de ecuaciones
                if variable in Diccionario_aleat[key]:
                    Diccionario_aleat[key].remove(variable)

        else:  # Si se termina el primer bucle for es porque se encontró una solución
            print('Eureka!!')
            break

    return Diccionario_aleat


def funcion_e(Diccionario):
    '''Asociación de ecuaciones con variables (opción organizada)'''
    Diccionario_orga = {}
    lista_claves = list(Diccionario.keys())
    N_ecua = len(lista_claves)
    contador = 0

    # Cuando las claves esta vacia será porque ya se encontró la solución
    while len(Diccionario.keys()) > 0:
        bandera = 0
        lista = min(Diccionario.values(), key=len)
        variable = lista[0]

        for key in lista_claves:  # Se barre todas las claves para borrar la variable del resto de Ecuaciones

            if lista == Diccionario[key] and bandera == 0:
                # Se almacena en el nuevo diccionario
                Diccionario_orga[key] = variable
                key_blue = key  # Se guarda la llave para borrarla luego del diccionario
                bandera = 1  # para cuando el contenido de una llave es igual al de otra

            # Para borrar la variable de las demas ecuaciones
            elif variable in Diccionario[key]:
                Diccionario[key].remove(variable)

        # se retira la clave del Dicc para no buscar ahí
        Diccionario.pop(key_blue)
        # ahora la lista tiene un elemento menos en el cual buscar
        lista_claves = list(Diccionario.keys())
        # print(key_blue,variable)
        # print(Diccionario)
        contador += 1
        if contador > N_ecua + 1:  # Seguro por si ocurre algo
            raise Exception('Hubo un error D: , ni idea cual lo sentimos ')
            break

    return Diccionario_orga

def onevsone(matriz):
    '''Asociación de ecuaciones con variables 1 a 1 (opción matricial)
    La matriz de entra está formada por un array de listas donde cada lista 
    representan una ecuación y contiene n booleanos , donde n es el número total
    de variables de todo el sistema de ecuaciones

    Return: 
    '''
    m =matriz.copy()
    size = m.shape[0] # Representa el numero de eqn

    # A cada 
    for a in range(size):

        # Lista de número de veces que se repite cada variable 
        sumCol = sum(m,axis = 0) #sumar columnas
        # Lista de cantidad de variables que tiene cada ecuación
        sumRow = sum(m,axis=1) #sumar filas

        # Se busca la variable que se repite la menor cantidad de veces
        # y almacena el num de repeticiones y la posición en la lista
        minSumCol = sumCol.min() # Si hay varias tomará la primera que encuentre
        yminSumCol = sumCol.argmin()

        # Se identifica la ecuación con menor num de variables
        minSumRow = sumRow.min()
        xminSumRow = sumRow.argmin()

        # Se identifica si hay variables unicas o eqn con solo una variable
        # Variables que se encuentran una sola vez en todo el sistema
        checkCol=argwhere(sumCol== 1)
        # Eqn que solo continene una variable
        checkRow = argwhere(sumRow==1)

        VcheckCol = zeros(size)
        VcheckRow = zeros(size)
        for b in checkCol:
            VcheckCol  = VcheckCol + m[:,b]

        for c in checkRow:
            VcheckRow =VcheckRow + m[c,:]
        if True in (VcheckCol>1): #or True in (VcheckCol>1):
            # Significa que el sistema de eqns es inconsistente
            # TODO de acá podemso detectar fallos en el sistema de eqns y notificar a usuario
            # para que los arregle como doble declaración de variables
            print(VcheckCol)
            raise Exception(pyENL_translations()["Mal planteamiento del sistema de ecuaciones"])
            return m ,-1

        if minSumRow == 1:
            # si una equ tiene solo una variable
            yminSumRow =m[xminSumRow].argmax() # variable que tiene la equ
            m[:,yminSumRow] = (arange(size) == xminSumRow)*(size+1)

        else:
            #se mira la variable que se repita el menor numero de veces
            xminSumCol =m[:,yminSumCol].argmax() # equ que posee la variable
            m[xminSumCol] = (arange(size) == yminSumCol)*(size+1)
            m[:,yminSumCol] = (arange(size) == xminSumCol)*(size+1)



    m = m//(size+1)

    #Verificacion
    sumCol = sum(m,axis = 0) #sumar columnas
    sumRow = sum(m,axis=1) #sumar filas
    ones = ones_like(sumCol)
    if array_equal(sumCol,ones) and array_equal(sumRow,ones):
        return m , 1
    else:
        return m, 0



def bloques(pyENL_eqns, pyENL_variables, tol=None, method='hybr', minEqns=3):
#def bloques(sistema_eqns, tol=None, method='hybr', minEqns=3):
    '''
    Recibe las ecuaciones y variables para resolver usando bloques mediante
    algoritmo de Tarjan para separación de sistemas de ecuaciones
    independientes entre sí.

    pyENL_eqns contiene ecuaciones, pyENL_variables las variables que hay,
    tol se refiere a la tolerancia del método, method es el método a usar y
    minEqns es la opción para que a partir de esa cantidad de ecuaciones se
    usen bloques (un valor muy bajo podría ser contraproducente ya que se
    tardaría más tiempo agrupando que solucionando el sistema de un solo
    llamado a la función root() )

    Devuelve resultado pyENL
    '''
    # TODO: Optimizar el asunto de valores ya calculados para no repetición
    # de cálculos de estas variables.



    #1.SE CREA LA MATRIZ DEL SISTEMA DE ECUACIONES################
    lista_eqn= pyENL_eqns
    lista_variables=[x.name for x in pyENL_variables]

    Num_eqn = len(lista_eqn)
    matriz_sistema = zeros((Num_eqn,Num_eqn) , dtype = int)

    for i , eqn in enumerate(lista_eqn):

        varINeqn=variables(eqn) #variables funcion de utils

        #Crea la fila de la matriz
        fila = []
        for variable in lista_variables:

            if variable in varINeqn:
                fila.append(1)
            else:
                fila.append(0)

        matriz_sistema[i,:] = array(fila)



    #2.CREAR MATRIZ DE RELACION 1VS1###################


    Rel11, flag = onevsone(matriz_sistema)


    #3.CREAR GRAFO ###################################

    matrizTarjan = (matriz_sistema - Rel11).T

    diccTarjan = {}

    for x ,fila in enumerate(matrizTarjan):
        posFila= (argwhere(fila == 1))
        contenido = list(posFila.reshape(posFila.size))

        diccTarjan[int(argwhere(Rel11[:,x]==1))] = contenido

    bloques = tarjan(diccTarjan)
    bloques.reverse()

    return bloques

def removeBigComments(texto):
    '''
        Remueve el contenido entre el inicio de comentario "<<" y el fin ">>"
        Mantiene los comentarios de una sola linea (los que solo tienen el inicio "<<")
    '''
    list_texto = texto.split('<<')
    list_sin_comentarios = []
    for seccion in list_texto:
        # se agrega de nuevo el << para los comentarios de una linea
        lista_seccion =  (seccion + '<<').split('>>')
        list_sin_comentarios += [lista_seccion[-1]]
    texto_sin_comentarios = ''.join(list_sin_comentarios)

    return texto_sin_comentarios

def variablesProperties(texto_eqn,vars_ecuacion,posibles):
    '''
    Identifica a partir de una ecación si es posible asociar la magnitud
    y/o unidad a la variable.

    Retorna un diccionario donde la llave es la variable y el contenido
    es otro diccionario asociado a la propiedad identificada

    Ejemplo:
    a = 1[cm] + 0.5[m]

    Resultado:

    {'a': {
            'guess': 51.0,
            'units': Unit('centimeter'),}
    }
    '''

    # validar si hay una sola variable y no se repite
    dic_vars = {}
    if len(vars_ecuacion) == 1 and posibles.count(vars_ecuacion[0]) == 1:
        variable_unique = vars_ecuacion[0]

        # validar que la variable esté despejada
        terminos_eqn = texto_eqn.replace('-','+').split('+')
        if variable_unique in terminos_eqn:
            to_eval = texto_eqn.replace(variable_unique,'')
            to_eval =to_eval.replace("[", "*pyENLu.parse_units('").replace("]", "')")
            result_var = eval(to_eval)

            dic_vars = {variable_unique: {}}
            # si no hay unidades el eval retornara un int or float
            if 'pyENLu' in to_eval:
                dic_vars[variable_unique]['guess'] = - result_var.magnitude
                dic_vars[variable_unique]['units'] = result_var.units
            else:
                dic_vars[variable_unique]['guess'] = - result_var

    return dic_vars