#!/usr/bin/env python3
'''Núcleo del solucionador de ecuaciones de pyENL'''

import scipy.optimize as opt
from numpy import *
from pyENL_fcns import *
ln = log
log = log10
import warnings
from pint import _DEFAULT_REGISTRY as u
from utils import variables , bloques
u.load_definitions("units.txt")
# from time import time as pyENL_time

# Definición de la función a resolver
# pyENL designa acá el vector de posibles soluciones que se está probando


def pyENL_sistema(pyENL, pyENL_variables, pyENL_eqns):
    '''
    Evalúa el sistema de ecuaciones que ingresa el usuario donde:
    pyENL: Valores numéricos para evaluar
    pyENL_variables: Objetos variables
    pyENL_eqns: Ecuaciones (lista de strings)
    '''
    cantidad_eqns = len(pyENL_variables)
    # Asignación de variables
    pyENL_eqns = list(pyENL_eqns)

    for cont, var in enumerate(pyENL_variables):
        print("----------------------")
        print(pyENL)
        print(var.name, '=', var.guess, var.solved)
        if var.solved and (len(pyENL_variables) != len(pyENL_eqns)):
            # exec(var.name + "=" + str(var.guess))
            # pyENL_eqns.append(var.name + "[" +str(var.units) + "]-(" +\
            #     str(var.guess) + "[" +str(var.units) + "])")
            pyENL_eqns.append(var.name + "-(" + str(var.guess) + ")")
            # "var.name[var.unit] - var.guess[var.unit]"?
        exec(var.name + '= pyENL[' + str(cont) + ']')
    print(pyENL_eqns)
    salidapyENL = empty((cantidad_eqns))
    # pyENL_eqns = list(pyENL_eqns)
    # for i in range(len(pyENL_variables) - len(pyENL_eqns)):
        # Funciones virtuales que sirven para aplicar la
        # engañadora del muérgano, reconocida mundialmente
        # en las Américas y en Francia
        # pyENL_eqns.append("0[u.m")
    # Funciones para hallar raíces
    for cont, eqn in enumerate(pyENL_eqns):
        try:
          # TODO
          # Editar eqn para soporte de unidades
          # Añadir las unidades en los strings!
          # Esto cada vez que aparezca una variable...
          # Ejemplo:
          # a = x**2 + y
          # (a*a.unit) = (x*x.unit) + (y*y.unit)
          # Reemplazar los strings de variables SI al lado no
          # hay valores alfanuméricos
            eqn2 = agregaUnidades(eqn, pyENL_variables)
            eqn2 = eqn2.replace("[", "*u.parse_units('")
            eqn2 = eqn2.replace("]", "')")
            print("Ecuación a evaluar",eqn2)
            tempoo = eval(eqn2)
            salidapyENL[cont] = tempoo.magnitude
        except Exception as e:
            er = str(e)
            print("-------" + er)
            clase = str(e.__class__)
            if clase == "<class 'TypeError'>":
                raise Exception("Error de tipeo en ecuación " + str(cont + 1))
            if 'Cannot convert' in er or 'is not defined in the unit registry' in er:
                raise Exception('Error de unidades en la ecuación ' + str(cont + 1) + ': ' +er)
            if 'invalid syntax' in er:
                raise Exception(
                    'Error de sintaxis en la ecuación ' + str(cont + 1))
            elif 'is not defined' in er:
                # Acá no se ha definido una función.
                raise Exception('No se ha definido a ' + er
                                [6:-16] + " en la ecuación " + str(cont + 1))
            elif 'unsupported operand type(s)' in er:
                # En este caso se intenta usar un nombre de función como
                # variable
                raise Exception('Nombre de función como variable en ecuación '
                                + str(cont + 1))
            elif ('required positional arguments' in er) or ('invalid number of arguments' in er):
                # Acá no se han suministrado suficientes argumentos a la
                # función
                raise Exception('Faltan argumentos en función de la ecuación '
                                + str(cont + 1))
            elif 'Not implemented for this type' in er:
                # Se ingresan variables no numéricas a la función
                raise Exception('Tipo de variable inadecuado en función de ecuación '
                                + str(cont + 1))
            elif 'return arrays must be of ArrayType' in er:
                # Acá no se ingresaron bien valores a una función NumPy:
                raise Exception('Mala entrada a función en la ecuación ' +
                                str(cont + 1))
            elif 'No se tienen los valores' in er:
                # La funció pyENL lanza la excepción por no tener suficientes
                # variables para operar
                raise Exception(er + ' en la ecuación ' + str(cont + 1))
            elif 'debe tener unidades' in er:
                raise Exception(er + ' en la ecuación ' + str(cont + 1))
            else:
                raise Exception
    return salidapyENL


def solver(pyENL_eqns, pyENL_variables, tol=None, method='hybr'):
    '''
    Acá llegan como parámetros la lista de funciones a hallar raíces como string
    La segunda entrada consiste en los objetos pyENL_variables en lista.
    iters por iteraciones
    '''

    warnings.simplefilter('error')
    # for vp in pyENL_variables: print(vp.name)

    # Verificación de que se tiene el mismo número de ecuaciones y de
    # variables:
    if len(pyENL_eqns) != len(pyENL_variables):
        return 'Error ecuaciones/variables'

    # Valores iniciales iguales a cero
    pyENL_variables.sort(key=lambda x: x.name.lower())
    # TODO
    # Lograr dividir las ecuaciones en bloques!!!
    # Reto---------------------------------------------------------------------------
    # Introducir rangos en los que se espera se encuentre una variable y probar con
    # valores aleatorios para pyENL_guesses dentro de esos intervalos hasta dar con la
    # respuesta, siempre que el timeout no se supere.-------------------------
    # La idea es que las claves del diccionario sean las variables en string y que
    # los valores sean listas con los valores máximos y mínimos de la misma para la
    # búsqueda de valores iniciales

    pyENL_cantidad = len(pyENL_variables)
    pyENL_guesses = zeros(pyENL_cantidad)
    # Actualización de los valores de suposiciones iniciales basados en los
    # atributos de los objetos de entrada de las variables.
    for contd, vard in enumerate(pyENL_variables):
        pyENL_guesses[contd] = vard.guess
    pyENL_ones = ones(pyENL_cantidad)
    # Formateo de las ecuaciones para tomar unidades de valores numéricos
    # desde las ecuaciones de usuario tipo: 5[m]
    #lista_eqns = []
    #for cadaEqn in pyENL_eqns:
        #temp = cadaEqn.replace("[", "*u.parse_units('")
        #temp = temp.replace("]", "')")
        #lista_eqns.append(temp)
    
  
    lista_bloques = bloques(pyENL_eqns, pyENL_variables , tol)
    #
    pyENL_eqnsA = array(pyENL_eqns) # Pasar la lista pyENL_eqns a array numpy
    pyENL_guessesA = array(pyENL_guesses)
    lista_guesses = []
    lista_variables = []
    lista_eqns = []
    try:
        # pyENL_sol = opt.root(pyENL_sistema, pyENL_guesses,
        #                      args=(pyENL_variables, pyENL_eqns), tol=tol, method=method)

        for j, bloque in enumerate(lista_bloques):
            lista_eqns.append(pyENL_eqnsA[bloque])
            eqnsBloque = lista_eqns[-1]
            recVars = '+'.join(eqnsBloque).replace("=","+") + "=0"
            # Une todas las ecuaciones del bloque para encontrar las variables
            # del mismo
            varsBloque = variables(recVars)
            varsBloque = [x for x in pyENL_variables if x.name in varsBloque]
            guessBloque = [x.guess for x in varsBloque]
            # print("Bloque número:",j)
            # print(varsBloque, guessBloque,eqnsBloque)
            solBloque = opt.root(pyENL_sistema, guessBloque,
                             args=(varsBloque, eqnsBloque), tol=tol, method=method)
            asegura_convergencia = True
            # print(solBloque['success'])
            if solBloque['success'] == False:
                asegura_convergencia = False
                raise Exception("Gordillo y los chulos")
            # Actualizar el atributo solved
            for i, varBloque in enumerate(varsBloque):
                if not varBloque.solved:
                    varBloque.guess = solBloque['x'][i]
                    varBloque.solved = True
                

       # pyENL_sol = opt.root(pyENL_sistema, pyENL_guesses,
         #                    args=(variables_bloque, eqns_bloque), tol=tol, method=method)
        # Métodos:
        # ‘hybr’
        # ‘lm’
        # ‘broyden1’
        # ‘broyden2’
        # ‘anderson’
        # ‘linearmixing’
        # ‘diagbroyden’
        # ‘excitingmixing’
        # ‘krylov’
        # ‘df-sane’
    #         Notes
    # -----
    # This section describes the available solvers that can be selected by the
    # 'method' parameter. The default method is *hybr*.
    # Method *hybr* uses a modification of the Powell hybrid method as
    # implemented in MINPACK [1]_.
    # Method *lm* solves the system of nonlinear equations in a least squares
    # sense using a modification of the Levenberg-Marquardt algorithm as
    # implemented in MINPACK [1]_.
    # Method *df-sane* is a derivative-free spectral method. [3]_
    # Methods *broyden1*, *broyden2*, *anderson*, *linearmixing*,
    # *diagbroyden*, *excitingmixing*, *krylov* are inexact Newton methods,
    # with backtracking or full line searches [2]_. Each method corresponds
    # to a particular Jacobian approximations. See `nonlin` for details.
    # - Method *broyden1* uses Broyden's first Jacobian approximation, it is
    #   known as Broyden's good method.
    # - Method *broyden2* uses Broyden's second Jacobian approximation, it
    #   is known as Broyden's bad method.
    # - Method *anderson* uses (extended) Anderson mixing.
    # - Method *Krylov* uses Krylov approximation for inverse Jacobian. It
    #   is suitable for large-scale problem.
    # - Method *diagbroyden* uses diagonal Broyden Jacobian approximation.
    # - Method *linearmixing* uses a scalar Jacobian approximation.
    # - Method *excitingmixing* uses a tuned diagonal Jacobian
    #   approximation.

    except Exception as e:
        print('ERROR:',str(e))
        # exit(0)
        # No está tomando el error porque primero aparece el de opt.root y antes
        # de ese si está el que se supone se quiere.
        # print(str(e))
        er = str(e)
        # print(er)
        if 'de tipeo' in er:
            raise Exception(er)
        if 'de sintaxis' in er:
            raise Exception(er)
        if 'No se ha definido' in er:
            raise Exception(er)
        if 'como variable en':
            raise Exception(er)
        if 'Faltan argumentos' in er:
            raise Exception(er)
        if 'inadecuado en función' in er:
            raise Exception(er)
        if 'Mala entrada' in er:
            raise Exception(er)
        if 'No se tienen los valores' in er:
            raise Exception(er)
        if 'debe tener unidades' in er:
            raise Exception(er)
    # asegura_convergencia = True
    # try:
    #     if pyENL_sol['success'] == False:
    #         asegura_convergencia = False
    # except:
    #     pass

    # for cont in range(0, len(pyENL_variables)):
    #     pyENL_variables[cont].guess = pyENL_sol['x'][cont]
    # pyENL_residuos = pyENL_sistema(pyENL_sol['x'], pyENL_variables, pyENL_eqns)
    sol_sistema = [x.guess for x in pyENL_variables]
    pyENL_residuos = pyENL_sistema(sol_sistema, pyENL_variables, pyENL_eqns)
    return pyENL_variables, pyENL_residuos, asegura_convergencia
  
def agregaUnidades(eqn_, pyENL_variables):
  from utils import variables, esalfanum
  vars_ = variables(eqn_)
  # TODO
  # Primero ajustar valores numéricos que vienen con unidades:
  # Ejemplo, si "a" y "b" están en metros y...
  # a = b + 5[m]
  # poder reconocer esos 5 como metros reemplazando con:
  # a = b + 5*u.parse_units("m")
  
  # print(vars_)
  eqn__ = eqn_
  for var_ in vars_:
    # Por cada variable se reemplaza con su unidad
    # eqn__ = eqn__.replace(var_, "(" + var_ + ")")
    l_var = len(var_)
    # Buscar la unidad de la variable asociada
    # Primero el índice de la variable
    indi = ([i for i, obj in enumerate(pyENL_variables) if obj.name == var_] )[0]
    unidad = str(pyENL_variables[indi].units) # Unidad en string
    enc = 0
    # print(eqn__)
    while enc != -1:
      # Mientras hay por encontrar...
      enc = enc + bool(enc)
      enc = eqn__.find(var_, enc)
      if enc == -1:
        break
      l_eqn = len(eqn__)
      # Verifica que se deba reemplazar
      # Condiciones: Que no hayan alfanuméricos antes o sea el primer puesto
      # Y que no hayan alfanuméricos después o sea el último puesto
      cond1 = (not esalfanum(eqn__[enc-1])) or enc == 0
      # cond2 = not esalfanum(eqn_[enc+1]) or enc == l_eqn - l_var
      if enc == l_eqn - l_var:
        cond2 = True
      else:
        cond2 = (not esalfanum(eqn__[enc+l_var]))
      comillas = ["'", '"']
      cond3 = (eqn__[enc-1] not in comillas) and (eqn__[enc + l_var] not in comillas)
      if (cond1 and cond2) and cond3:
        # Reemplazar
        eqn__ = eqn__[0:enc] + "(" + eqn__[enc:enc+l_var] + \
          "*u.parse_units('" + unidad + "'))" + eqn__[enc+l_var:]
        enc = enc + 1
  # print(eqn__)
  return eqn__
