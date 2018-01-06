#/usr/bin/env python3
import random
import copy
import os
'''
Utilidades generales para uso de pyENL
'''
from numpy import *
from pyENL_fcns import *
import re
ln = log
prop = log  # Solo importa el nombre de la función para comprobación...
haprop = log


class configFile:
    '''
    Clase que facilita datos de configuración, su lectura y escritura
    '''

    def __init__(self, filename):
        '''
        Inicializada con el nombre de archivo que contiene la configuración
        del programa
        '''
        # Primero verifica que exista el archivo, si no; carga configuración por
        # defecto.
        # TODO : Mejorar aspectos cuando está dañado o no existe config.txt
        # items a configurar
        self.items = ["lang", "method"]
        self.lang = 'en'
        self.method = 'hybr'
        self.format = '{:,.3}'
        self.tol = 1e-4
        self.timeout = 10
        self.sFontUI = 'Monospace,12,-1,5,25,0,0,0,0,0'
        self.cuDir = os.path.expanduser('~')
        try:
            f = open(filename, 'rb')
            texto_config = f.read().decode("utf-8").splitlines()
            f.close()
            for i, elm in enumerate(texto_config):
                valor = elm.split("=")[1]#.replace(" ", "")
                if 'lang' in elm:
                    self.lang = valor
                if 'method' in elm:
                    self.method = valor
                if 'format' in elm:
                    self.format = valor
                if 'tol' in elm:
                    self.tol = float(valor)
                if 'timeout' in elm:
                    self.timeout = float(valor)
                if 'font' in elm:
                    self.sFontUI = valor
                if 'cuDir' in elm:
                    if os.path.exists(valor): #se confirma que la ruta si existe, si no se deja la de usuario
                        self.cuDir = valor
        except:
            # Guardar con la configuración!
            pass

    


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


def variables(texto_eqn):
    '''
    Regresa en texto las variables del string texto_eqn
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
        if '<<' not in eqn:
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
        if '<<' not in eqn:
            try:
                result = pattern.sub(lambda x: dicc[x.group()], eqn)
                # print(eqn)
                # El reemplazo:
                texto[i] = result
            except:
                pass
    # Ahora la comprobación de que no han quedado $ en las ecuaciones:
    for i, eqn in enumerate(texto):
        if '<<' not in eqn:
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
        if ((eqn.replace(' ','').replace('\t', '') != '') and ('{' not in eqn)) and ('<<' not in eqn):
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
    for ecuacion in lista:
        lista_vars = lista_vars + variables(ecuacion)
    lista_vars = list(set(lista_vars))
    # Regresa el número de ecuaciones y de variables.
    return ecuaciones, lista_vars

def actualizar_directorio(cuDir):
    '''Guarda en config.txt la ultima ruta de la carpeta donde se abrió o guardó un archivo'''
    # se guarda la ultima carpeta usada para cuando se vuelva a abrir el programa
    f = open('config.txt','r+')
    data =f.read().splitlines() #se crea una lista con cada linea del txt
    if 'cuDir' in f.read(): # si existe cuDir en el txt solo se reemplaza en la posicion "i" donde se encuentre
        for i,fila in enumerate(data):
            if 'cuDir' in fila:
                data[i] = 'cuDir=' + str(cuDir) + '\n'
    else: # de lo contrario lo crea en la ultima linea (la ultima linea está vacía)
        data[-1] = 'cuDir=' + str(cuDir) + '\n'

    f.seek(0) # Posiciona el cursor en el inicio
    f.truncate() #Borra todo el txt para sobreescribirlo sin problemas
    f.write('\n'.join(data))
    f.close()

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

    def bloques(pyENL_eqns, pyENL_variables, tol=None, method='hybr', minEqns=3):
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
        pass
