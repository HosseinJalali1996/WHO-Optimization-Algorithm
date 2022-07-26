import numpy as np
from structure_class import struct

def WHO(parameters,problem):

    # 1. Algorithm's parameters
    N = parameters.N               # Number of search agents
    Max_iter = parameters.Max_iter # Maximum number of iterations
    PS = parameters.PS             # Stallions Percentage 
    PC = parameters.PC             # Crossover Percentage
    NStallion = int(np.ceil(PS*N)) # number Stallions
    Nfoal = int(N - NStallion)     # number foals

    # 2. Extract Problem Info
    CostFunction = problem['fitness']   # Fitness function or Cost function
    varmin = problem['lower_bound']     # Low Bound
    varmax = problem['upper_bound']     # Up Bound
    nvar = problem['dimensions']        # Dimension variable

    # 3. Gbest definition
    Convergence_curve = np.zeros(Max_iter)
    gBest = np.zeros(nvar)
    gBestScore = np.inf

    # 4. Create initial population
    Empty_for_foal = struct()
    Empty_for_foal.position = None
    Empty_for_foal.cost = None

    foal = Empty_for_foal.repeat(Nfoal)
    for i in range(Nfoal):
        foal[i].position = np.random.uniform(varmin,varmax,nvar)
        foal[i].cost = CostFunction(foal[i].position)
        if gBestScore > foal[i].cost:
            gBestScore = foal[i].cost
            gBest = foal[i].position
            

    Empty_for_Stallion = struct()
    Empty_for_Stallion.position = None
    Empty_for_Stallion.cost = None
    Empty_for_Stallion.Group = None


    Stallion = Empty_for_Stallion.repeat(NStallion)
    for j in range(NStallion):
        Stallion[j].position = np.random.uniform(varmin,varmax,nvar)
        Stallion[j].cost = CostFunction(Stallion[j].position)
        if gBestScore > Stallion[j].cost:
            gBestScore = Stallion[j].cost
            gBest = Stallion[j].position

    # 5. Category the *foal* and merging to *Stallion*
    NGroup = int(np.floor(Nfoal/NStallion))
    for i in range(NStallion):
        Stallion[i].Group = foal[i*NGroup:(i+1)*NGroup]

    # 6. Exchange function
    def exchange(Stallion):
    
        NStallion = len(Stallion)
        NGroup = int(len(Stallion[0].Group))
        Value_Stack = []
        
        for i in range(NStallion):
            for j in range(NGroup):
                Value_Stack.append(Stallion[i].Group[j].cost)

            value = np.amin(Value_Stack)
            index = np.argmin(Value_Stack)
            Value_Stack.clear()

            if value < Stallion[i].cost:

                bestgroup = Stallion[i].Group[index].deepcopy()

                Stallion[i].Group[index].position = Stallion[i].position
                Stallion[i].Group[index].cost = Stallion[i].cost

                Stallion[i].position = bestgroup.position
                Stallion[i].cost = bestgroup.cost
      
        return Stallion
    
    # using the exchange function
    Stallion = exchange(Stallion)

    # 7. Selected global best from *Stallion*
    minimum_index = []

    for i in range(NStallion):
        minimum_index.append(Stallion[i].cost)
        
    index = np.argmin(minimum_index)
    WH = Stallion[index]
    gBest = WH.position
    gBestScore = WH.cost
    Convergence_curve[0] = WH.cost

    # 8. Function for sort the cost value of *Groups* for each row in *Stallion*
    def SortFunc(Stallion,RowNum):
    
        NGroup = int(len(Stallion[RowNum].Group))
            
        Value_Stack = []
        sorting = []
        
        for j in range(NGroup):
            Value_Stack.append(Stallion[RowNum].Group[j].cost)
        index = np.argsort(Value_Stack)
        for x in index:
            sorting.append(Stallion[RowNum].Group[x])
        for j in range(NGroup):
            Stallion[RowNum].Group[j] = sorting[j] 
            
        Value_Stack.clear()
        sorting.clear()
        
        return Stallion[RowNum]

    # 9. The original loop
    I = []
    Iter = 1
    while Iter<Max_iter+1:
        TDR = 1-Iter*(1/Max_iter)
        for i in range(NStallion):

            # sort the cost value of Groups for each row in Stallion
            Stallion[i] = SortFunc(Stallion,i)
            
            for j in range(NGroup):
                
                if np.random.rand() > PC:
                    
                    r1 = np.random.rand(nvar) < TDR
                    r2 = np.random.rand()
                    r3 = np.random.rand(nvar)
                    idx = (r1 == 0)
                    z = r2*idx + r3*~idx
                    rr = -2+4*z # this variable is between -2 to 2
                    
                    Stallion[i].Group[j].position = 2*z*np.cos(2*np.pi*rr)\
                                                            *(Stallion[i].position-Stallion[i].Group[j].position)\
                                                            +(Stallion[i].position)
                else:
                    
                    A = np.random.permutation(NStallion)
                    A = np.delete(A, A==i)
                    a = A[0]
                    b = A[1]
                    
                    x1 = Stallion[a].Group[-1].position
                    x2 = Stallion[b].Group[-1].position
                    y = (x1+x2)/2
                    Stallion[i].Group[j].position = y
                    
                Stallion[i].Group[j].position = np.minimum(Stallion[i].Group[j].position,varmax)
                Stallion[i].Group[j].position = np.maximum(Stallion[i].Group[j].position,varmin)
                Stallion[i].Group[j].cost = CostFunction(Stallion[i].Group[j].position)
                
            if np.random.rand() < 0.5:
                kk = 2*z*np.cos(2*np.pi*rr)*(WH.position - Stallion[i].position) + WH.position
            else:
                kk = 2*z*np.cos(2*np.pi*rr)*(WH.position - Stallion[i].position) - WH.position
            
            kk = np.minimum(kk,varmax)
            kk = np.maximum(kk,varmin)
            fk = CostFunction(kk)
            
            if fk < Stallion[i].cost:
                Stallion[i].position = kk
                Stallion[i].cost = fk
        
        Stallion = exchange(Stallion)
        valueWH = []
        for x in range(NStallion):
            valueWH.append(Stallion[x].cost)
        M1= np.argmin(valueWH)

        WH = Stallion[M1]
        gBest = WH.position
        gBestScore = WH.cost
        Convergence_curve[Iter-1] = WH.cost
        
        print(f"Iteration : {Iter-1} , Best Cost : {Convergence_curve[Iter-1]}")
        I.append(Iter-1)
        Iter+=1

    return Convergence_curve, gBest, gBestScore, I

    
