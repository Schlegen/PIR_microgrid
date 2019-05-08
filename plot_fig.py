import matplotlib.pyplot as plt
import numpy as np
import random as rd

T=48
N=100

def plotTotalLoad (M,path_to_folder):
    """
    M is a (N,T) vector. Each line correspond to a scenario and each column to a time t.
    This function plots a bar diagram with the average values of total load for each t. 
    For the path_to_folder, mind putting '\\' instead of '/'.
    """
    
    AL=np.zeros(T)  #vector with the average loads for each t
    E=np.zeros(T)   #vector with the standard deviations of load for each t
    for t in range (T):
        a=0
        for n in range (N):
            a+=M[n,t]
        a/=N
        AL[t]=a
        E[t]=np.std(M[:,t])
        
    ind=np.arange(T)
    
    plt.bar(ind,AL,width=0.5,bottom=None,yerr=E)
    plt.title("Average total load")
    plt.xlabel("t")
    plt.ylabel("l(t)")
    #plt.savefig(path_to_folder)
    

#Affiche quatre fenetres les unes sous les autres
def plotDetailedLoad3(A,B,C,D,flexible,path_to_folder):
    """ 
    A, B, C and D are (N,T) vectors. Each vector corresponds to an actor and each line correspond to a scenario and each column to a time t.
    This function plots a grouped bar diagram with the average values of load for each t for each actor.
    For the path_to_folder, mind putting '\\' instead of '/'.
    """
    
    AL1,AL2,AL3,AL4=np.zeros(T),np.zeros(T),np.zeros(T),np.zeros(T) #vector with the average loads for each t
    E1,E2,E3,E4=np.zeros(T),np.zeros(T),np.zeros(T),np.zeros(T) #vector with the standard deviations of load for each t
    for t in range (T):
        a,b,c,d=0,0,0,0
        for n in range (N):
            a+=A[n,t]
            b+=B[n,t]
            c+=C[n,t]
            d+=D[n,t]
        AL1[t]=a/N
        AL2[t]=b/N
        AL3[t]=c/N
        AL4[t]=d/N
        E1[t]=np.std(A[:,t])
        E2[t]=np.std(B[:,t])
        E3[t]=np.std(C[:,t])
        E4[t]=np.std(D[:,t])
        
    ind=np.arange(T)
    width=0.15

    plt.subplot(4,1,1)
    p1=plt.bar(ind, AL1, 3*width, color='r', bottom=0, label="DC",yerr=E1)
    plt.ylabel("l(t)")
    plt.xlim([0,T+5])
    plt.legend(loc='upper right')
    plt.title('Average '+ flexible +' load by actor and by time')
    
    plt.subplot(4,1,2)
    p2=plt.bar(ind, AL2, 3*width, color='b', bottom=0, label="SB",yerr=E2)
    plt.ylabel("l(t)")
    plt.xlim([0,T+5])
    plt.legend(loc='upper right')
    
    plt.subplot(4,1,3)
    p3=plt.bar(ind, AL3, 3*width, color='g', bottom=0, label="PV",yerr=E3)
    plt.ylabel("l(t)")
    plt.xlim([0,T+5])
    plt.legend(loc='upper right')
    
    plt.subplot(4,1,4)
    p4=plt.bar(ind, AL4, 3*width, color='y', bottom=0, label="CS",yerr=E4)
    plt.xlabel("t")
    plt.ylabel("l(t)")
    plt.xlim([0,T+5])
    plt.legend(loc='upper right')
    
    #plt.savefig(path_to_folder)
    
   

M=np.zeros((N,T))
for n in range (N):
    for t in range (T):
        M[n,t]=rd.randint(-10,10)
        

A=np.zeros((N,T))
for n in range (N):
    for t in range (T):
        A[n,t]=rd.randint(-1,1)
B=np.zeros((N,T))
for n in range (N):
    for t in range (T):
        B[n,t]=rd.randint(-1,1)
C=np.zeros((N,T))
for n in range (N):
    for t in range (T):
        C[n,t]=rd.randint(-1,1)
D=np.zeros((N,T))
for n in range (N):
    for t in range (T):
        D[n,t]=rd.randint(-1,1)
        
plotDetailedLoad3(A,B,C,D,"flexible","C:\\Users\\Elisabeth\\Documents\\PONTS 2018-2019\\Semestre 2\\Detailled Flexible Load")
plotTotalLoad(M,"C:\\Users\\Elisabeth\\Documents\\PONTS 2018-2019\\Semestre 2\\Total Load")
