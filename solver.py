#!/usr/bin/env python3
'''Núcleo del solucionador de ecuaciones de pyENL'''

import scipy.optimize as opt
from numpy import *
from pyENL_fcns import *
from CoolProp.CoolProp import PropsSI as prop
from CoolProp.CoolProp import HAPropsSI as haprop
ln = log
log = log10
import warnings
# from time import time as pyENL_time

# Definición de la función a resolver
# pyENL designa acá el vector de posibles soluciones que se está probando


def pyENL_sistema(pyENL, pyENL_variables, pyENL_eqns):
    cantidad_eqns = len(pyENL_variables)
    # Asignación de variables
    for cont, var in enumerate(pyENL_variables):
        exec(var.name + '= pyENL[' + str(cont) + ']')
    salidapyENL = empty((cantidad_eqns))
    # Funciones para hallar raíces
    for cont, eqn in enumerate(pyENL_eqns):
        try:
            salidapyENL[cont] = eval(eqn)
        except Exception as e:
            if 'invalid syntax' in str(e):
                raise Exception(
                    'Error de sintaxis en la ecuación ' + str(cont + 1))
            if 'is not defined' in str(e):
                raise Exception('No se ha definido a ' + str(e)
                                [6:-16] + " en la ecuación " + str(cont + 1))
            else:
                raise Exception
    return salidapyENL


def solver(pyENL_eqns, pyENL_variables, pyENL_iteraciones, pyENL_tol):
    '''
    Acá llegan como parámetros la lista de funciones a hallar raíces como string
    La segunda entrada consiste en los objetos pyENL_variables en lista.
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
    try:
        pyENL_sol = opt.root(pyENL_sistema, pyENL_guesses,
                             args=(pyENL_variables, pyENL_eqns), tol=pyENL_tol, method='hybr')
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
        # print('ERROR:',str(pyENL_e))
        # exit(0)
        # No está tomando el error porque primero aparece el de opt.root y antes
        # de ese si está el que se supone se quiere.
        # print(str(e))
        if 'de sintaxis' in str(e):
            raise Exception(str(e))
        if 'No se ha definido' in str(e):
            raise Exception(str(e))
    asegura_convergencia = True
    try:
        if pyENL_sol['success'] == False:
            asegura_convergencia = False
    except:
        pass

    for cont in range(0, len(pyENL_variables)):
        pyENL_variables[cont].guess = pyENL_sol['x'][cont]
    pyENL_residuos = pyENL_sistema(pyENL_sol['x'], pyENL_variables, pyENL_eqns)
    return pyENL_variables, pyENL_residuos, asegura_convergencia
