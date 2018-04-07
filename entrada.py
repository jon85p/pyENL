#!/usr/bin/env python3
'''
Intérprete de texto
'''
import sys
from solver import solver
from utils import variables, random_lim, variables_string
from numpy import inf
from CoolProp.CoolProp import PropsSI as prop
from CoolProp.CoolProp import HAPropsSI as haprop
from time import time
import optparse
import os
from pint import _DEFAULT_REGISTRY as u
u.load_definitions("units.txt")
sindim = ((1*u.m)/(1*u.m)).units
try:
    from expimp import sols2odt, sols2tex
except:
    pass


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
        self.guess = 1.0
        self.upperlim = 1e5
        self.lowerlim = -1e5
        self.comment = 'Variable'
        self.units = sindim  # Unidad de la variable.
        self.solved = False
        self.dim = self.units.dimensionality #Dimensión de la variable

    def __repr__(self):
      return "pyENL variable <" + self.name + ">"
    
    def convert(self):
        '''
        Regresa la cadena de texto con la que debería reemplazarse el nombre de
        la variable para la posterior labor de conversión.
        '''
        # TODO
        pass


def find_between(s, first, last):
    '''
    Busca una cadena de texto entre dos strings; first y last que hacen parte
    del string s.
    '''
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def entradaTexto(ecuaciones, pyENL_timeout, varsObj=None, tol=None, method='hybr'):
    '''
    ecuaciones es una lista de cadenas de texto con ecuaciones de entrada.
    varsObj define si llegan objetos variable como entrada.
    La salida de esta función está dada por
    '''
    lista = []
    dicc_condiciones = {}
    # Si el método no está listado entonces no se procede
    # method = method.strip(' ')
    methods = ['hybr', 'lm', 'broyden1', 'broyden2', 'anderson', 'linearmixing',
               'diagbroyden', 'excitingmixing', 'krylov', 'df-sane']
    if method not in methods:
        raise Exception('El método de resolución no está listado, ver ayuda.')
    for ie, eqn in enumerate(ecuaciones):
        if ((eqn.replace(' ','').replace('\t', '') != '') and ('{' not in eqn)) and ('<<' not in eqn):
            expresion = eqn.replace(" ", "")
            expresion = expresion.replace('\t','')
            # Capacidad de interpretar pow
            expresion = expresion.replace("^", "**")
            izq_der = expresion.split('=')
            operandos = ["+", "-", "*", "/", "("]
            # Revisar que no haya operadores incompletos
            if (izq_der[0][-1] in operandos) or (izq_der[1][-1] in operandos):
              raise Exception('Ecuación mal escrita: ' + str(ie+1))
            # Revisar que no hayan paréntesis sin cerrar
            par_err1 = izq_der[0].count("(") != izq_der[0].count(")")
            par_err2 = izq_der[1].count("(") != izq_der[1].count(")")
            if par_err1 or par_err2:
              raise Exception("No cierran los paréntesis en " + str(ie+1))
            paraRaiz = izq_der[0] + \
                '-(' + izq_der[1] + ')'  # Igualación de cero
            lista.append(paraRaiz)
        if '{' in eqn:
            # Entonces acá vienen condiciones, que son de la forma:
            #   {x,first_guess,-lim,+lim}
            if '}' not in eqn:
                raise Exception("Falt cerrar corchete")
            condicion = find_between(eqn, '{', '}')
            condicion = condicion.replace(' ', '')
            condiciones = condicion.split(',')
            dicc_condiciones.update({condiciones[0]: condiciones[1:4]})

    # Lista contiene las ecuaciones
    lista_vars = []
    for ecuacion in lista:
        lista_vars = lista_vars + variables(ecuacion)
    lista_vars = list(set(lista_vars))
    variables_salida = []
    for miembro in lista_vars:
        # Crear los objetos pyENL_variable a partir de los strings de nombres
        # de vars
        objeto = pyENL_variable(miembro)
        # Ahora verificar que se encuentre listada en las condidiones
        # Si se puede definir directamente entonces dejar ese valor inicial
        # Es decir, tomar el valor del guess como el sugerido en una ecuación
        # Tipo:
        # x = ln(y)
        # y = 5
        # Entonces el valor inicial de y será 5, aún si el usuario no lo deja
        # especificado por los corchetes {}
        for cadaEqn in lista:
            varAux = cadaEqn
            varAux = varAux.replace(objeto.name + '-', '')
            try:
                objeto.guess = eval(varAux)
            except:
                pass
            # Si no, entonces buscar si ya hay una definición:
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
        # Se van añadiendo los objetos de salida de las variables:
        variables_salida.append(objeto)
    pyENL_inicio = time()  # Tiempo de inicio de llamada al solver
    # Llamada al solver
    # Si los objetos variables ya vienen entonces:
    if varsObj:
        variables_salida = varsObj
    pyENL_solved = False
    try:
        pyENL_solucion = solver(lista, variables_salida, tol=tol, method=method)
        pyENL_solved = True
        pyENL_final = time()
        pyENL_transcurrido = pyENL_final - pyENL_inicio
    except Exception as e:
        # exit(0)
        # Intento aleatorio
        # Si el error es de sintaxis hay que detectarlo sin que intente
        # nuevamente buscar soluciones infructuosamente:
        er = str(e)
        if 'de tipeo' in er:
            raise Exception(er)
        if 'Cannot convert' in er or 'is not defined in the unit registry' in er:
            raise Exception(er)
        if 'Improper input parameters were entered.' in er:
            raise Exception('Parámetros inválidos suministrados')
        if 'de sintaxis' in er:
            raise Exception(er)
        if 'No se ha definido' in er:
            # Una función no está definida
            raise Exception(er)
        if 'como variable en' in er:
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
        pyENL_final = time()
        pyENL_transcurrido = pyENL_final - pyENL_inicio
        while pyENL_transcurrido < pyENL_timeout:
            # Encontrar nuevos valores de guesses:
            for cont, objetoVar in enumerate(variables_salida):
                obtemp = objetoVar  # Objeto variable temporal
                obtemp.guess = random_lim(objeto.lowerlim, objeto.upperlim)
                variables_salida[cont] = obtemp
            # Termina de actualizar, ahora:
            try:
                pyENL_solucion = solver(lista, variables_salida,
                                        tol=1.49012e-08)
                pyENL_solved = True
                break
            except Exception as e:
                er = str(e)
                if 'de tipeo' in er:
                    raise Exception(er)
                if 'Cannot convert' in er or 'is not defined in the unit registry' in er:
                    raise Exception(er)
                if 'Improper input parameters were entered.' in er:
                    raise Exception('Parámetros inválidos suministrados')
                if 'de sintaxis' in er:
                    raise Exception(er)
                if 'No se ha definido' in er:
                    # Una función no está definida
                    raise Exception(er)
                if 'como variable en' in er:
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
                if 'Error de unidades' in er:
                    raise Exception(er)
            # Actualiza el tiempo que ha transcurido:
            pyENL_final = time()
            pyENL_transcurrido = pyENL_final - pyENL_inicio
    if pyENL_solved == False:
        raise Exception(
            'El tiempo de espera ha sido superado, verifique las ecuaciones')
    if pyENL_solucion == 'Error ecuaciones/variables':
        raise ValueError("Hay " + str(len(lista)) + ' ecuación(es) y ' +
                         str(len(variables_salida)) + ' variable(s)')
    return [pyENL_solucion, pyENL_transcurrido]


def main():
    '''
    Rutina principal de la versión CLI (Command Line Interface)
    '''
    parser = optparse.OptionParser('Uso: ' + sys.argv[0] + ' -f archivo_texto\
    -t timeout(seg) -m método -e archivo_exp')
    parser.add_option('-f', dest='foption', type='string',
                      help='Archivo de texto con el sistema de ecuaciones')
    parser.add_option('-t', dest='toption', type='float',
                      help='Tiempo de espera máximo para la solución')
    parser.add_option('-e', dest='eoption', type='string',
                      help='Archivo de exportación, puede ser .odt, .tex o .pdf (LaTeX)')
    parser.add_option('-m', dest='moption', type='string',
                      help='Métodos: hybr, lm, broyden1, broyden2, anderson, linearmixing, diagbroyden, excitingmixing, krylov, df-sane')

    (options, args) = parser.parse_args()
    if options.foption == None:
        print(parser.usage)
        exit(0)
    else:
        fichero = options.foption
    # Verificación de existencia y lectura del archivo de texto:
    if not os.path.isfile(fichero):
        print('[!] El archivo de texto no se encuentra')
        exit(0)
    if not os.access(fichero, os.R_OK):
        print('[!] No se cuentan con los permisos apropiados para acceder al archivo')
        exit(0)
    if options.toption == None:
        pyENL_timeout = 10
    else:
        pyENL_timeout = options.toption
    if options.moption:
        metodo = options.moption
    else:
        metodo = 'hybr'

    with open(fichero, 'rb') as f:
        ecuaciones = (f.read()).decode('utf-8')
        ecuaciones = ecuaciones.splitlines()
    # Ahora a organizar lo de las variables tipo string
    ecuaciones = variables_string(ecuaciones)
    try:
        solucion = entradaTexto(ecuaciones, pyENL_timeout, method=metodo)
    except Exception as e:
        print(str(e))
        exit(0)

    # Si se especificó archivo de exportación entonces generarlo:
    if options.eoption:
        if options.eoption[-4::] not in ['.pdf', '.odt', '.tex']:
            print('No se especificó un válido archivo de salida, debe ser .odt\
            o .tex (soporte para LaTeX pendiente)')
            exit(0)
        if '.odt' in options.eoption:
            # Intentar guardar el documento para exportación y en caso de error
            # lanzar mensaje de advertencia.
            try:
                sols2odt(solucion[0][0], options.eoption, ecuaciones)
            except:
                print('No se pudo guardar el archivo de exportación, verifique \
                que tenga permisos de escritura o que el nombre sea válido')
        else:
            # Entonces es .pdf o .tex
            try:
                autor = input('Nombre de autor para reporte LaTeX: ')
                sols2tex(solucion[0][0], options.eoption, ecuaciones, autor)
            except:
                print('No se pudo generar el archivo, verifique que tenga\
                dependencias necesarias instaladas.')

    for variable in solucion[0][0]:
        print(variable.name, '=', variable.guess)
    print('Residuos:', solucion[0][1])

if __name__ == '__main__':
    main()
