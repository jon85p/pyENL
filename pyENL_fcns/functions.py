'''
Funciones propias de pyENL
'''


def quadsum(x, y):
    return x**2 + y ** 2


def corriente(str1, a, str2, b):
    '''
    Ejemplo para funciones de usuario usando función sencilla para hallar
    la corriente dado un voltaje V y una resistencia R.
    La llamada es similar a como se llaman las funciones de propiedades
    Ejemplo en test/test4.txt
    '''
    V = ['V', 'v', 'voltaje', 'Voltaje']
    R = ['R', 'r', 'resistencia', 'Resistencia']
    if str1 in V and str2 in R:
        v, r = a, b
    if str1 in R and str2 in V:
        r, v = a, b
    return v / r
