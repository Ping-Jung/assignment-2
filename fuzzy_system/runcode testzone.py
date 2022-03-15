import matplotlib.pyplot as plt
import numpy as np

X = np.arange(0, 21)
indA = np.array([1 if (4 <= x <= 12) else 0 for x in X])
indB=np.array([1 if(10<=x<=15) else 0 for x in X])

def Intersection(A,B):
    temparray=A.copy()
    i=0
    while i< len(temparray):
        if temparray[i]==B[i] and B[i]==1:
            temparray[i]=1
        else:
            temparray[i]=0
        i=i+1
    return temparray

# Indicator function of intersection of A and B
ind_A_intersect_B = Intersection(indA,indB)
plt.scatter(X, ind_A_intersect_B)
plt.xticks(X)
#plt.show()


def Union(A,B):
    temparray=A.copy()
    i=0
    while i< len(temparray):
        if B[i]==1:
            temparray[i]=1
        i=i+1
    return temparray


ind_A_union_B = Union(indA,indB)
plt.scatter(X, ind_A_union_B)
plt.xticks(X)
#plt.show()


def Negation(A):
    temparray=A.copy()
    i=0
    while i< len(temparray):
        temparray[i]=0 if A[i]==1 else 1
        i=i+1
    return temparray

ind_not_A=Negation(indA)
plt.scatter(X, ind_not_A)
plt.xticks(X)
#plt.show()

