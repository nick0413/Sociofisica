import numpy as np 
import matplotlib.pylab as plt 
import pandas as pd 
import networkx as nx
import SBMLDiagrams as SBML
import libsbml
import re 


def find_indices(list_to_check, item_to_find):
    indices = []
    for idx, value in enumerate(list_to_check):
        if value == item_to_find:
            indices.append(idx)
    return indices


def cargar_datos(tipo):
	if tipo=='C':
		my_file = open("Datos_componentes3.txt", "r")

		data = my_file.read()

		data_into_list = data.split("\n")
		my_file.close()

		return data_into_list
	
	if tipo=='R':
		my_file = open("Datos_reacciones3.txt", "r")

		data = my_file.read()

		data_into_list = data.split("\n")
		my_file.close()

		return data_into_list

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
	parejas_index=[]
	parejas2=[]

	#print(frase)

	for elemento in elementos:
		esta=False
		grande=False
		X=None
		if not (elemento==''):
			if frase.find(elemento)!=-1:
				parejas.append(elemento)
				parejas_index.append(frase.find(elemento))


	for e1 in parejas:
		big_brother_exists=False
		big_brother=None
		append=True

		for e2 in parejas:
			if e2.find(e1)!=-1:
				if e1!=e2:
					big_brother_exists=True
					big_brother=e2

		if big_brother_exists:
			reps_bb=len(re.findall(big_brother,frase))
			reps_e1=len(re.findall(e1,frase))
			# print(big_brother,e1)
			# print(reps_bb,reps_e1)
			if reps_e1>reps_bb:
				append=True
			elif reps_e1<reps_bb:
				append=False
			else:
				indexes_e1 = [match.start() for match in re.finditer(e1, frase)]
				indexes_e2 = [match.start() for match in re.finditer(e1, frase)]
				# print('|||||||||||||||||||||')
				# print(indexes_e2,indexes_e1)
				if indexes_e2==indexes_e1:
					# print(False)
					append=False

		if append:
			# print(e1)
			parejas2.append(e1)



	lista_listas=[]
	sorted_matches = [x for _,x in sorted(zip(parejas_index,parejas))]

	parejas3=[]
	for e1 in sorted_matches:
		if e1 in parejas2:
			parejas3.append(e1)

	
	start=parejas3[0]
	if len(parejas3)==1:
		lista_listas.append([start,start])

	else:
		for i in range(1,len(parejas3)):
			h=[start,parejas3[i]]
			lista_listas.append(h)

	#print(lista_listas)


	return lista_listas






R=cargar_datos('R')
C=cargar_datos('C')

interacciones=cargar_interacciones()

print_datos(R,C,'')

edges=[]
for r in R:
	h=uniones_4(r,interacciones,C)
	for conexion in h:
		edges.append(conexion)


Conex=open("Conexiones.txt",'w')

for edge in edges:
	print(edge)

	Conex.write(edge[0].strip('-')+','+edge[1].strip('-')+'\n')
Conex.close()

com_final=open("Componentes.txt","w")

for c in C:
	com_final.write(c.strip('-')+'\n')
com_final.close()












