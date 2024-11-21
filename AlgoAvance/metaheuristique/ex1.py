import numpy as np

MAX_BOUCLE = 20

q1 = np.array([[-17, 10, 10, 10, 0, 20],
            [10, -18, 10, 10, 10, 20],
            [10, 10, -29, 10, 20, 20],
            [10, 10, 10, -19, 10, 10], 
            [0, 10, 20, 10, -17, 10],
            [20, 20, 20, 10, 10, -28]])


def read_file(name):

    f=open(name,'r')
    for ligne in f:
        toks = ligne.split()
        size_matrice = int(toks[0])
        q = np.empty([size_matrice,size_matrice],dtype=int)
        for i in range(size_matrice):
            for j in range(size_matrice):
                q[i,j] = int(toks[j+i*size_matrice])


def f(Q,X):
    return np.dot(X, np.dot(Q, X))

def solution_initial(Q):
    x = np.random.randint(0,high=2,size=6,dtype=int)
    return x

def meilleur_voisin(Q,X):
    X_prime = X.copy()
    X_best = X
    X_best[0] = (X_best[0]+1)%2
    best_sol = f(Q,X_best)

    for i in range(1,np.shape(X)[0]):
        X_prime[i] = (X_prime[i]+1)%2

        sol = f(Q,X_prime)
        if sol<best_sol:
            X_best = X_prime.copy()
            best_sol = sol
    #print(best_sol)
    return X_best


#print(meilleur_voisin(q,solution_initial(q)))


def Steepest_Hill_Climbing(Q,X):
    nb_boucle = 0
    stop = False
    s = X.copy()
    while not stop and nb_boucle <= MAX_BOUCLE:
        print("iteration n° = %d" % nb_boucle)
        ss = meilleur_voisin(Q,s)

        if f(Q,s)>f(Q,ss):
            s = ss.copy()
        else:
            stop = True
        nb_boucle+=1
    print(f(Q,s))
    return s

Steepest_Hill_Climbing(q,solution_initial(q))


