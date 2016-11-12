#!/usr/bin/env python3
'''
Intérprete de texto
'''
import sys
from solver import solver
from utils import variables, random_lim
from numpy import inf
from CoolProp.CoolProp import PropsSI as prop
from time import time

class pyENL_variable:
    '''
    Clase creadora de objetos de tipo variable para las resoluciones de las
    ecuaciones no lineales.
    '''
    def __init__(self, nombre):
        '''
        Función creadora, dado un nombre de variable crea la instancia de la
        variable. El nombre es una cadena de texto
        '''
        self.name = nombre
        self.guess = 1
        self.upperlim = 1e5
        self.lowerlim = -1e5

    def convert(self):
        '''
        Regresa la cadena de texto con la que debería reemplazarse el nombre de
        la variable para la posterior labor de conversión.
        '''
        #TODO
        pass

def find_between(s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

fichero = sys.argv[1]
pyENL_timeout = int(sys.argv[2]) #Cantidad de segundos máxima para obtener respuesta.
with open(fichero, 'rb') as f:
    ecuaciones = (f.read()).decode('utf-8')
    ecuaciones = ecuaciones.splitlines()

lista = []
dicc_condiciones = {}
for eqn in ecuaciones:
    if ((eqn != '') and ('{' not in eqn)) and ('<<' not in eqn):
        expresion = eqn.replace(" ", "")
        expresion = expresion.replace("^", "**") #Capacidad de interpretar pow
        izq_der = expresion.split('=')
        paraRaiz = izq_der[0] + '-(' + izq_der[1] + ')' #Igualación de cero
        lista.append(paraRaiz)
    if '{' in eqn:
        #Entonces acá vienen condiciones, que son de la forma:
        #   {x,first_guess,-lim,+lim}
        if '}' not in eqn:
            print('Error, falta el: }')
        condicion = find_between(eqn, '{', '}')
        condicion = condicion.replace(' ', '')
        condiciones = condicion.split(',')
        dicc_condiciones.update({condiciones[0]:condiciones[1:4]})


#Lista contiene las ecuaciones
lista_vars = []
for ecuacion in lista:
    lista_vars = lista_vars + variables(ecuacion)
lista_vars = list(set(lista_vars))
variables_salida = []
for miembro in lista_vars:
    #Crear los objetos pyENL_variable a partir de los strings de nombres de vars
    objeto = pyENL_variable(miembro)
    #Ahora verificar que se encuentre listada en las condidiones
    #Si se puede definir directamente entonces dejar ese valor inicial
    #Es decir, tomar el valor del guess como el sugerido en una ecuación
    #Tipo:
    #x = ln(y)
    #y = 5
    #Entonces el valor inicial de y será 5, aún si el usuario no lo deja
    #especificado por los corchetes {}
    for cadaEqn in lista:
        varAux = cadaEqn
        A_reemplazar = [objeto.name, '-', '(', ')']
        for termino_areemplazar in A_reemplazar:
            varAux = varAux.replace(termino_areemplazar, '')
        try:
            objeto.guess = eval(varAux)
        except:
            pass
        #Si no, entonces buscar si ya hay una definición:
    try:
        objeto.guess = float(dicc_condiciones[miembro][0])
    except:
        pass
    try:
        objeto.lowerlim = float(dicc_condiciones[miembro][1])
    except:
        pass
    try:
        objeto.upperlim = float(dicc_condiciones[miembro][2])
    except:
        pass
    #Se van añadiendo los objetos de salida de las variables:
    variables_salida.append(objeto)
pyENL_inicio = time() #Tiempo de inicio de llamada al solver
#Llamada al solver
try:
    solver(lista, variables_salida, pyENL_iteraciones = 600, pyENL_tol=1.49012e-08)
    print('A la primera!')
except Exception as e:
    #Intento aleatorio
    pyENL_final = time()
    pyENL_transcurrido = pyENL_final - pyENL_inicio
    pyENL_solved = False
    while pyENL_transcurrido < pyENL_timeout:
        #Encontrar nuevos valores de guesses:
        for cont, objetoVar in enumerate(variables_salida):
            obtemp = objetoVar#Objeto variable temporal
            obtemp.guess = random_lim(objeto.lowerlim, objeto.upperlim)
            variables_salida[cont] = obtemp
        #Termina de actualizar, ahora:
        try:
            solver(lista, variables_salida, pyENL_iteraciones = 600, \
            pyENL_tol=1.49012e-08)
            pyENL_solved = True
            break
        except:
            pass
        pyENL_final = time()
        pyENL_transcurrido = pyENL_final - pyENL_inicio
    if not pyENL_solved:
        print('TIMEOUT')
    print('Transcurrieron', pyENL_transcurrido, 'segundos')
