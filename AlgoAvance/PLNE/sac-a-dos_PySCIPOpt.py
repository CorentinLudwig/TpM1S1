#!/usr/bin/python3
# coding: utf-8

from pyscipopt import Model

c = -1

O = []
N = []

x = []

M = Model()   # Le "modèle" est initialisé, et affecté à la variable M

#ouverture et lecture du fichier
f = open("sac-a-dos-24.txt")
for i in f:
    toks= i.split()
    if len(toks) == 0 : continue
    if toks[0] == '#': continue
    
    if c == -1 : 
        c = int(toks[0])
        continue
    O.append((int(toks[1]),int(toks[2])))
    N.append(toks[0])
    x.append(M.addVar("x"+str(i),vtype="B"))

f.close()


# Création de la contrainte "poids" : somme des poids pris <= C
M.addCons(sum(O[i][0] * x[i] for i in range(len(O))) <= c)

# Création de l'obectif : max. somme des valeurs
M.setObjective(sum(O[i][1]*x[i] for i in range(len(O))),"maximize")

#creation du fichier lp
M.writeProblem("sac-a-dos-auto.lp")

# Lancement du solveur
print("-----------Exécution du solveur--------")
M.optimize()
print("-----------Exécution terminée--------")

# Si pas de solution optimale trouvée : on quitte l'interpréteur Python avec quit()
if M.getStatus() != 'optimal': print('Pas de solution ?!',quit())

# Lorsqu'il y a une solution optimale : on affiche les valeurs des x[i] et la valeur de l'objectif
print("\nSolution optimale trouvée :")
for i in range(len(O)) : print(x[i],":",M.getVal(x[i]),sep="",end=" ")
print("\nValeur =", M.getObjVal())

# Affichage des numéros des objets sélectionnés
print("Objets sélectionnés : ",end="")
for i in [i for i in range(len(O)) if M.getVal(x[i]) != 0]: print(N[i],end=" ")
print()