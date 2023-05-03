import numpy as np 
import matplotlib.pylab as plt 
import pandas as pd 
import networkx as nx
import SBMLDiagrams as SBML
import libsbml
import re 
import openai as gpt


def chachito(pregunta,info=''):

	gpt.api_key="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"
	conectado=pregunta+info
	resultado=gpt.Completion.create(engine="text-davinci-003",prompt=conectado,n=1,max_tokens=4000)
	print(resultado.choices[0].text)



# ? Este bloque trae el archivo sbml como un modelo de libsbml
sbml_file = "Datos.sbml"
reader = libsbml.SBMLReader()
document = reader.readSBMLFromFile(sbml_file)
model = document.getModel()

R=[]
C=[]

i=0
for reaction in range(model.getNumReactions()): #Este ciclo trae las reacciones quimicas y las guarda en R
	i=i+1
	rxn=model.getReaction(reaction)
	for modifier in range(rxn.getNumModifiers()):
		mod=rxn.getModifier(modifier)
		#print(mod.getId(),"en la reaccion", rxn.getId())

	#print(f"{i} reacciones", rxn.getName())
	R.append(rxn.getName())
j=0
for comp in range(model.getNumSpecies()):#Este ciclo trae las componentes quimicas y las guarda en C
	j=j+1
	componente=model.getSpecies(comp)
	C.append((componente.getName()))


for i in R:
	print(i)
C_elementos=[]

'''
Los componentes en el sistema de especies de SBML no estan estructurados correctamente 
para la interpretacion de un grafo. Este bloque de codigo los reestructura apropiadamente.
'''
for i in C:
	C_n=i.split(",")
	for componente in C_n:
		#print(componente)
		componente=re.sub("[\(\[].*?[\)\]]", "", componente)
		componente=componente.strip()
		componente=re.sub(" ","-",componente)
		#print(componente)
		if componente != '':
			C_elementos.append(componente)




# for c in C_elementos:
# 	print(c)

	







