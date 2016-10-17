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

  - Los comentarios se escriben entre << y >>
  - Ejemplo en test/input2.xt

###Propiedades termodinámicas
Se pueden acceder a propiedades con el paquete CoolProp instalable desde pip con
<pre><code>pip install coolprop</code></pre>
- Uso de la función prop en lugar de PropsSI, ejemplos: [en la documentación de CoolProp](http://www.coolprop.org/coolprop/examples.html#sample-props-code)

- Ejemplo: Entalpía del agua a presión atmosférica y 300 K:
 <pre><code>prop('H', 'P', 101325, 'T', 300, 'Water')</code></pre>
