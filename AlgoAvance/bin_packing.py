import itertools
from pyscipopt import Model
import sys

# Q 6.1 le nombre d'objet

if len(sys.argv) != 2:
    print("use = python3 ",sys.argv[0]," path_input_file")

C = -1

tO = []
O = range(len(tO))

M = Model()

Name = None



#ouverture et lecture du fichier
f = open(sys.argv[1])
for i in f:
    toks= i.split()
    if Name == None:
        Name = toks[0]
        continue
    if C==-1:
        C = int(toks[0])
        O = range(int(toks[1]))
        continue
    tO.append(int(toks[0]))
f.close()

tO.sort(reverse= True)

# Dictionnaire de var. bool.  : bi = 1 si la boite i est utiliser
b = {}
for i in O:
    b[i] = M.addVar(f"y{i}",vtype="B")

# Dictionnaire de var. bool.  : xij = 1 si objet i est dans la boite j
x = {}
for i,j in itertools.product(O,b):
  x[i,j] = M.addVar(f"x{i}{j}",vtype="B")

#contrainte

#chaque objet doit être dans exactement une boite
for i in O : M.addCons(sum(x[i,j] for j in b) == 1)

#une boite est utilisée (bj = 1 > 0) si et seulement si elle contient au moins un objet 
for j in b : M.addCons(  sum(x[i,j] for i in O) >= b[j])
for j in b : M.addCons(  sum(x[i,j] for i in O) <= b[j]*C)

#dans chaque boite, la somme des tailles des objets ne doit pas dépasser la capacité
for j in b : M.addCons(sum(x[i,j]*tO[i] for i in O) <= C)

#contrainte d'optimisation
#Les boites doivent etre utiliser dans l'ordre (symetrie des boites)
for j in range(len(O)-1):
    M.addCons(b[j] >= b[j+1])
    
# Si l'objet i dans la boite j alors les objet i-n doivent etre dans les boites j-n (symetrie objet)
for i in range(1, len(O)):
    M.addCons(x[i,j] <= sum(x[k, j-1] for k in range(i)))

#creation objectif
M.setObjective(sum(b[j] for j in O), "minimize")

# Lancement du solveur
print("-----------Exécution du solveur--------")
M.optimize()
print("-----------Exécution terminée--------")

# Si pas de solution optimale trouvée : on quitte l'interpréteur Python avec quit()
if M.getStatus() != 'optimal': print('Pas de solution ?!',quit())

# Lorsqu'il y a une solution optimale : on affiche les valeurs des x[i] et la valeur de l'objectif
print("\nSolution optimale trouvée :")
for i in O:
    val = M.getVal(b[i])
    if val == 1:
        for j in O:
            print(x[i,j],":",M.getVal(x[i,j]),sep="",end=" ")
        print("\n")
    
print("\nValeur =", M.getObjVal())
