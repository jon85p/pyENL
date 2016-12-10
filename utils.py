#/usr/bin/env python3

'''
Utilidades para reconocimiento de parámetros de ecuaciones
'''
from numpy import *
ln = log
prop = log  # Solo importa el nombre de la función para comprobación...


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
    '''Verifica que el caracter es alfanumérico'''
    suma = 0
    suma += (caracter >= '\x30' and caracter <= '\x39')
    suma += (caracter >= '\x41' and caracter <= '\x5a')
    suma += (caracter >= '\x61' and caracter <= '\x7a')
    return bool(suma)


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
    # TODO
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
