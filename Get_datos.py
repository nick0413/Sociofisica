import numpy as np 
import matplotlib.pylab as plt 
import pandas as pd 
import networkx as nx
import SBMLDiagrams as SBML
import libsbml
import re 


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
print(i)
j=0
for comp in range(model.getNumSpecies()):#Este ciclo trae las componentes quimicas y las guarda en C
	j=j+1
	componente=model.getSpecies(comp)
	C.append((componente.getName()))
print(j)

C_elementos=[]

'''
Los componentes en el sistema de especies de SBML no estan estructurados correctamente 
para la interpretacion de un grafo. Este bloque de codigo los reestructura apropiadamente.
'''
# for r in R:
# 	print(r)
for i in C:

	C_n1=i.split(",")
	
	for C_n2 in C_n1:
		C_n=C_n2.split(":")
		for componente in C_n:
			#print(componente)
			componente=re.sub("[\(\[].*?[\)\]]", "", componente)#esto borra lo que esta dentro de corchetes
			componente=componente.strip()
			#componente=re.sub(" ","-",componente)
			#print(componente)
			if componente != '':
				C_elementos.append(componente)



C2=[]
R2=[]

for c in C_elementos:
	c2=re.sub(" ","-",c)
	c2='-'+c2+'-'
	if c2 not in C2:
		C2.append(c2)


for r in R:
	r=r.rstrip()
	r=re.sub(",","",r)
	r=re.sub(" ","-",r)
	if r not in R2:
		R2.append('-'+r+'-')


Comp_file=open("1.txt",'w')

for c in C2:
	Comp_file.write(c+'\n')

Comp_file.close()

React_file=open('2.txt','w')

for r in R2:
	React_file.write(r+'\n')

React_file.close()