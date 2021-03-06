#!/usr/bin/env python3

# Unit test for pyENL core
import numpy as np
import sys
from os import path

try:
    sys.path.append(path.realpath("."))
except:
    pass

from utils import *

def test_esalfanum():
	pruebas = [".", "a", "g", "c", "e", "z", "5", "0", "9", "4", "s"]
	for prueba in pruebas:
		assert esalfanum(prueba)
	npruebas = ["/", "ç", "(", ")", "-", "~", "ł", "í", "+"]
	for prueba in npruebas:
		assert not esalfanum(prueba)

def test_buscainds():
	textos = ["Hola, esta es una prueba",
		"Esta es otra prueba",
		"Acá va sutanito de Melbourne",
		"548963254875421 548",
		"ET es - 1 extraTerrestre",
		"Ajá, cinco * por dos + - un *-+ a",
		'prop("Water", "rho", 1, 2)']
	busquedas = ["a", "e", "a", "5", "1", "*", 'r']
	resultados = [[3,9,16,23],[5,16],[5,10],[0,7,11,16],[8],[11,28], [1,10,15]]
	for i, texto in enumerate(textos):
		assert buscainds(texto, busquedas[i]) == resultados[i]

def test_probar():
	no_vars1 = ["e", "pi", "cos", "log", "log10", "sin", "exp",
		"ln", "prop", "vars", "sinh", "cosh", "quadsum"]
	vars1 = ["a", "b", "c", "d", "propS", "tab", "a1", "log20",
			"sind", "cosd", "mu", "nu", "density"]
	for var1 in vars1:
		assert probar(var1)
	for novar1 in no_vars1:
		assert not probar(novar1)

def test_variables():
	# Ecuaciones sin espacios
	eqns = ["5*cos(x)+32-(41-sqrt(y))",
		"a-b-(cos(a*b))",
		"cos(log10(x*y**2-z))+ln(exp(e*Rx-d))-(8*tan(x-8+e))",
		"(x+y)-0",
		'Cp0Mass_1-prop("Cp0mass","Dmass",0[kg/m^3],"Hmass",0[J/kg],"1-Butene")']
	tvars = [["x", "y"],
			["a", "b"],
			["x","y","z","Rx","d"],
			["x","y"],
			["Cp0Mass_1"],
		]
	for i, eqn in enumerate(eqns):
		assert variables(eqn) == tvars[i]

def test_random_lim():
	nums = 100*np.random.rand(1000)
	for num in nums:
		aleat = random_lim(num, num+100)
		assert (aleat < num+100) and (aleat > num)

def test_variables_string():
	texto = ["#f#='R510'","#g#='R134A'",
		"H1=prop('H','P', 101325, 'T', 300, #f#)",
		"H2=prop('H','P', 101325, 'T', 300, #g#)"]
	check = ["H1=prop('H','P', 101325, 'T', 300, 'R510')",
		"H2=prop('H','P', 101325, 'T', 300, 'R134A')"]
	assert variables_string(texto) == check

def test_cantidadEqnVar():
	eqns = [['x+5=y*e^2'], ['x-cos(y) = 8','z = 5*pi'],
	        ['<<Comentario>>', '#f# = "R22"', 'H = prop("H", "P", 1[atm], "Q", 1, "Water")'],
			["x=1","y=2[m]"]]
	cantidades = [[1,2,{}],[2,3,{'z': {'guess':5*np.pi}}],
				[1,1,{}], [2,2,{'y':{'guess':2,'units':'meter'}, 'x':{'guess':1}}]]
	for i, eqn in enumerate(eqns):
		ecu, varss, dic = cantidadEqnVar(eqn)
		ecu_, varss_, dic_ = cantidades[i]
		assert ecu == ecu_ and len(varss) == varss_
		assert len(dic_.keys()) == len(dic.keys())
		for key in dic.keys():
			if dic[key].get('guess'):
				assert abs(dic[key]['guess'] - dic_[key]['guess']) < 1e-5
			if dic[key].get('units'):
				assert dic[key]['units'].format_babel() == dic_[key]['units']
			
