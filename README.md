#pyENL

###Descripción
Solucionador de sistemas de ecuaciones no lineales para ingeniería
###Características
- Resuelve numéricamente ecuaciones no lineales usando MINPACK desde SciPy.
- Opción para cambiar los valores de búsquedas iniciales.
- En desarrollo!

###Uso de archivos:
- <pre><code>solver(pyENL_eqns, pyENL_variables, pyENL_iteraciones, pyENL_tol):</code></pre>
    Acá llegan como parámetros la lista de funciones a hallar raíces como string
    La segunda entrada consiste en los objetos pyENL_variables en lista.
- <pre><code>entrada.py:</code></pre>
  Consiste de un parser de un archivo de texto que contiene las ecuaciones en
  cada línea de texto, además de las restricciones dadas de cada variable.
  Ejemplo:
    - x^2+y^2 = 1
    - y = 2*x - 5
    - {x, 1, -5, 5}

  En este caso se busca solucionar las dos primeras ecuaciones contenidas en un
  archivo de texto con la condición de que x se encuentre entre -5 y 5, así como
  que el valor inicial de suposición de x es 1.
