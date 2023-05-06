import numpy as np 
import matplotlib.pylab as plt 
import pandas as pd 
import networkx as nx
import SBMLDiagrams as SBML
import libsbml
import re 

def cargar_interacciones():
	my_file = open("tipos_interaccion.txt", "r")

	data = my_file.read()

	data_into_list = data.split("\n")
	my_file.close()

	return data_into_list
def print_datos(R,C,tipo):
	if tipo=="C":
		for c in C:
			print(c)
	if tipo=='R':
		for r in R:
			print(r)

def uniones(frase,interacciones, elementos):
	lista_listas=[]
	palabras=frase.split(" ")

	found_start=False
	start=None
	targets=[]

	for palabra in palabras:
		#print(palabra)
		if palabra in interacciones:
			tipo_interaccion=interacciones.index(palabra)

		if palabra in elementos:
			if not found_start:
				start=palabra
				found_start=True
			else:
				targets.append(palabra)

	for target in targets:
		conexion=[start,target]
		lista_listas.append(conexion)

	return lista_listas

def uniones_2(frase,interacciones, elementos):
	lista_listas=[]
	inter=None
	found_start=False
	istart=None
	start=None
	targets=[]
	print(frase)

	for elemento in elementos:		#revisa todos los elementos conocidos
		found=frase.find(elemento)	#si no esta en la frase, pasa a la siguiente

		if found==-1:
			pass

		if not found_start: 				#Si no ha encontrado el nodo incial
			if frase.find(elemento)!=-1: 	#si este elemento esta en la frase
				start=elemento				#entonces este elemento debe ser el nodo inicial
				found_start=True			
				#print('found',elemento)


		if found_start:										#si ya encontramos el inicial
			if frase.find(elemento)<frase.find(start):		#y encontramos un elemento que esta mas a la izquierda 
				if frase.find(elemento)!=-1:				#en la frase
					start=elemento							#entonces ese debe ser el inicial

			if elemento.find(start)>-1:						#si hay un elemento mas complejo
				if (frase.find(elemento))!=-1:				#que tambien esta en la frase
					start=elemento							#entonces el inicial debe ser la forma compleja

			if (elemento.find(start))==-1:					#si el elemento no es el inicial
				#print(elemento,start,elemento.find(start))
				if (frase.find(elemento))!=-1:				#pero si esta en la frase
					#print(elemento,start,elemento.find(start))
					if (start.find(elemento))==-1:			#y no es una version mas simple del inicial
						if not (elemento in targets):
							targets.append(elemento)
									

	for interaccion in interacciones:
		found=frase.find(elemento)
		if found==-1:
			pass
		else:
			inter=interaccion

	for target in targets:
		conexion=[start,target]
		lista_listas.append(conexion)
		print(conexion)

	
	#print(len(targets))

	return lista_listas

def uniones_3(frase,interacciones, elementos):
	lista_listas=[]
	matches=[]
	matches_index=[]
	targets=[]

	found_start=False
	print('----------')
	print(frase)

	for elemento in elementos:
		#print(elemento,frase.find(elemento))
		if frase.find(elemento)!=-1:
			print('found')
			if elemento not in matches:
				matches.append(elemento)
				matches_index.append(frase.find(elemento))
	
	print(matches)
	sorted_matches = [x for _,x in sorted(zip(matches_index,matches))]


	if len(matches)==1:
		lista_listas=[matches[0],matches[0]]
		return lista_listas
	else:
		for element in matches:
			if not found_start:
				start=element
				found_start=True
			else:
				targets.append(element)

	for target in targets:
		lista_listas.append([start,target])
		print([start,target])

	
	return lista_listas

def uniones_4(frase,interacciones, elementos):
	parejas=[]

	print(frase)

	for elemento in elementos:
		#print(elemento,frase.find(elemento))
		if frase.find(elemento)!=-1:
			parejas.append(elemento)
	
	print(parejas)

	return parejas




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


C_elementos=[]

'''
Los componentes en el sistema de especies de SBML no estan estructurados correctamente 
para la interpretacion de un grafo. Este bloque de codigo los reestructura apropiadamente.
'''
com_org=open("Componentes_originales.txt",'w')

for c in C:
	com_org.write(c+'\n')

com_org.close()

rec_org=open("reacciones_originales.txt",'w')

for r in R:
	rec_org.write(r+'\n')

rec_org.close()


for i in C:

	C_n1=i.split(",")
	
	for C_n2 in C_n1:
		C_n=C_n2.split(":")
		for componente in C_n:
			#print(componente)
			componente=re.sub("[\[].*?[\]]", "", componente)#esto borra lo que esta dentro de corchetes
			componente=componente.strip()
			#componente=re.sub(" ","-",componente)
			#print(componente)
			if componente != '':
				if componente not in C_elementos:
					C_elementos.append(componente)

C2=[] 						#Listas separadas por guiones
R2=[]
for c in C_elementos:
	h=re.sub(" ", "-", c)
	C2.append('-'+h.lower()+'-')
for r in R:
	h=re.sub(" ", "-", r)
	h=re.sub("bound", "-", h)
	h=re.sub(",", "-", h)
	h=re.sub(":", "-", h)
	h=re.sub("-to-cell-surfaces-", "-to-cell-surface-", h)
	R2.append('-'+h.lower()+'-')

Comp_file=open("Datos_componentes2.txt",'w')
for c in C2:
	Comp_file.write(c+'\n')
Comp_file.close()

reac_file=open("Datos_reacciones2.txt",'w')
for r in R2:
	reac_file.write(r+'\n')
reac_file.close()



interacciones=cargar_interacciones()

print_datos(R,C,'')

t=0
for r in R2:
	h=uniones_4(r,interacciones,C2)
	t=t+1
	#print(t)
	if t>10:
		break

#uniones_3(R2[9],interacciones,C2)
	







