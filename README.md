# pyENL

(Python "Ecuaciones No Lineales")


<sup>A baby tiny open-source alternative to Engineering Equation Solver (EES)<sub>

[![Build Status](https://travis-ci.org/jon85p/pyENL.svg?branch=master)](https://travis-ci.org/jon85p/pyENL)
[![codecov](https://codecov.io/gh/jon85p/pyENL/branch/master/graph/badge.svg)](https://codecov.io/gh/jon85p/pyENL)
[![Code Health](https://landscape.io/github/jon85p/pyENL/master/landscape.svg?style=flat)](https://landscape.io/github/jon85p/pyENL/master)
[![license](https://img.shields.io/github/license/jon85p/pyENL.svg)]()


<img src="GUI/imgs/icon240.png">*

### Description

Engineering nonlinear equations systems solver
### Features
- [x] Solve numerically systems equations from MINPACK method of SciPy.
- [x] More solvers available from: [scipy.optimize.root](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root.html#scipy.optimize.root)
- [x] Physical units support
- [x] CoolProp thermodynamical functions support
- [ ] Engineering functions inside
- [ ] Users functions (Python).
- On development stage!

### Use:
- Terminal mode:
<pre><code>entrada.py -f file_text -t[seconds]:</code></pre>
  Equations file with conditions of each variable.
  Example:
    - x^2+y^2 = 1
    - y = 2*x - 5
    - {x, 1, -5, 5}

  In this case, the target is solve the equations in a file text
  with the following restrictions: x it's betweet -5 and 5, and
  the initial guess for x is 1.

  - Comments between symbols: "<<" and ">>"
  - Example: test/input2.xt
- GUI (User Interface):

File pyENL.py run the Qt interface for pyENL.

  - Screenshots:

<img src="https://jon85p.github.io/pyENL/images/s1.png">
<img src="https://jon85p.github.io/pyENL/images/s2.png">
<img src="https://jon85p.github.io/pyENL/images/s3.png">
<img src="https://jon85p.github.io/pyENL/images/s4.png">

### Thermodynamical properties
Via CoolProp, an open source thermodynamical properties library.
Install:
<pre><code>pip install coolprop</code></pre>
- The pyENL function "prop" it's used for this purpose: [CoolProp Documentation](http://www.coolprop.org/coolprop/examples.html#sample-props-code)

- Example: Water enthalpy at atmosferic pressure and 300 K:
 <pre><code>prop('H', 'P', 101325, 'T', 300, 'Water')</code></pre>

### Strings variables:

<pre><code>#ref# = 'R134a'</code></pre>
<pre><code>P = prop('P', 'T', 300, 'Q', 0, #ref#)</code></pre>
<pre><code>H = prop('H', 'P', P, 'T', 300, #ref#)</code></pre>
<sup>Icon by @fabianalexisinostroza<sub>
