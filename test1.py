import libsbml as sb
import networkx as nx
import matplotlib.pylab as plt
reader= sb.SBMLReader()
doc=reader.readSBML("cascada.sbml")
xml_datos=sb.writeSBMLToFile(doc,"cascada.xml")

file = "./cascada.xml"
G=nx.Graph()

print(f"numero de errores {doc.getNumErrors() }")
print('corre')