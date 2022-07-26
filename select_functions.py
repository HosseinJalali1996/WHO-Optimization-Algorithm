import numpy as np

def Ufun(x,a,k,m):
    o = k*((x-a)**m)*(x>a) + k*((-x-a)**m)*(x<(-a))
    return o

#F1
def F1(x):
    R = sum(x**2)
    return R
#F2
def F2(x):
    R = sum(np.abs(x))+np.prod(np.abs(x)) 
    return R
#F3
def F3(x):
    dim = len(x)
    R = 0
    for i in range(dim):
        R = R+sum(x[0:i])**2
    return R
#F4
def F4(x):
    R = np.max(np.abs(x))
    return R
#F5
def F5(x):
    dim = len(x)
    R = sum(100*(x[1:dim]-(x[0:dim-1]**2))**2 + (x[0:dim-1]-1)**2)
    return R
#F6
def F6(x):
    R = sum(np.abs((x+0.5))**2)
    return R
#F7
def F7(x):
    dim = len(x)
    R = sum(np.arange(1,dim+1)*(x**4)) + np.random.rand()
    return R
#F8
def F8(x):
    R = sum(-x*np.sin(np.sqrt(np.abs(x))))
    return R
#F9
def F9(x):
    dim = len(x)
    R = sum(x**2 - 10*np.cos(2*np.pi*x)) + 10*dim
    return R
#F10
def F10(x):
    dim = len(x)
    R = -20*np.exp(-0.2*np.sqrt(sum(x**2)/dim)) - np.exp(sum(np.cos(2*np.pi*x))/dim) + 20 + np.exp(1)
    return R
#F11
def F11(x):
    dim = len(x)
    R = sum(x**2)/4000 - np.prod(np.cos(x/np.sqrt(np.arange(1,dim+1)))) + 1
    return R
#F12
def F12(x):
    dim = len(x)
    R = (np.pi/dim)*(10*((np.sin(np.pi*(1+(x[0]+1)/4)))**2)+sum((((x[0:dim-1]+1)/4)**2)\
                    *(1+10*((np.sin(np.pi*(1+(x[1:dim]+1)/4))))**2))+((x[dim-1]+1)/4)**2)+sum(Ufun(x,10,100,4))
    return R
#F13
def F13(x):
    dim = len(x)
    R = 0.1*((np.sin(3*np.pi*x[0]))**2 + sum((x[0:dim-1]-1)**2 * (1+(np.sin(3*np.pi*x[1:dim]))**2))\
            +((x[dim-1]-1)**2)*(1+(np.sin(2*np.pi*x[dim-1]))**2))+sum(Ufun(x,5,100,4))
    return R


def Function_Name(Name):
    k = 30
    return{
        'F1': {
            'fitness': F1,
            'lower_bound':-100,
            'upper_bound':100,
            'dimensions':k
        },
        'F2': {
            'fitness': F2,
            'lower_bound':-10,
            'upper_bound':10,
            'dimensions':k
        } ,
        'F3': {
            'fitness': F3,
            'lower_bound':-100,
            'upper_bound':100,
            'dimensions':k 
        },
        'F4': {
            'fitness': F4,
            'lower_bound':-100,
            'upper_bound':100,
            'dimensions':k
        },
        'F5': {
            'fitness': F5,
            'lower_bound':-30,
            'upper_bound':30,
            'dimensions':k
        },
        'F6': {
            'fitness': F6,
            'lower_bound':-100,
            'upper_bound':100,
            'dimensions':k
        },
        'F7': {
            'fitness': F7,
            'lower_bound':-1.28,
            'upper_bound':1.28,
            'dimensions':k
        },
        'F8': {
            'fitness': F8,
            'lower_bound':-500,
            'upper_bound':500,
            'dimensions':k
        },
        'F9': {
            'fitness': F9,
            'lower_bound':-5.12,
            'upper_bound':5.12,
            'dimensions':k
        },
        'F10': {
            'fitness': F10,
            'lower_bound':-32,
            'upper_bound':32,
            'dimensions':k
        },
        'F11': {
            'fitness': F11,
            'lower_bound':-600,
            'upper_bound':600,
            'dimensions':k
        },
        'F12': {
            'fitness': F12,
            'lower_bound':-50,
            'upper_bound':50,
            'dimensions':k
        },
        'F13': {
            'fitness': F13,
            'lower_bound':-50,
            'upper_bound':50,
            'dimensions':k
        }
    }.get(Name, f'{Name} is not exist!' )
