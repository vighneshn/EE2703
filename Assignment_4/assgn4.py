#!/usr/bib/python3.5
from pylab import *
from scipy.integrate import quad

def ex(v):
    return exp(v) # Function for e^x
def coscos(v):
    return cos(cos(v)) # Function for cos(cos(x))

def u_x(x, k, func=ex):
    return func(x)*cos(k*x) # Passing the function to be multiplied by cos, will be integrated while finding coefficient
def v_x(x, k, func=ex):
    return func(x)*sin(k*x) # Passing the function to be multiplied by sin at that value, will be integrated.

def find_coeff(func=ex):
    a0 = quad(u_x,0,2*pi,args=(0,func))[0]/2/pi # code to compute the dc constant
    a = [quad(u_x,0,2*pi,args=(k,func))[0]/pi for k in range(1,26,1)] # code to compute the coefficients of cos
    b = [quad(v_x,0,2*pi,args=(k,func))[0]/pi for k in range(1,26,1)] # code to compute the coefficients of sin
    coeff = [a[i/2] if i%2 == 0 else b[(i-1)/2] for i in range(50)] # Code merging a and b
    coeff.insert(0,a0); a.insert(0,a0)
    return coeff, a, b
    
def plot_any(coeff, x, fig, _ylabel, _xlabel, _title, plot_type, color, l_dots,_legend = 'Actual Curve'):
    '''
    This function plots any of the function/coefficient plots.
    It takes parameters for the x and y values, labels, titles, structure and color.
    '''
    figure(fig) # Choosing figure number
    title(_title) # Plot title
    ylabel(_ylabel) # Setting labels
    xlabel(_xlabel)
    grid(True); a = None
    ## To check what kind of plot we need, a regular, semilog or loglog
    if plot_type == 1:
        plot(x,coeff,color+l_dots, label=_legend)
    elif plot_type == 2:
        semilogy(x,coeff,color+l_dots, label=_legend)
    else:
        loglog(x,coeff,color+l_dots, label=_legend)
    legend()

def matrix(func=ex):
    x=linspace(0,2*pi,400)
    #x=x[:-1] # drop last term to have a proper periodic integral 
    b=func(x) # f has been written to take a vector 
    A=zeros((400,51)) # allocate space for A
    A[:,0]=1 # col 1 is all ones
    for k in range(1,26):
        A[:,2*k-1]=cos(k*x) # cos(kx) column
        A[:,2*k]=sin(k*x)   # sin(kx) column
    cl =lstsq(A,b)[0]      # the '[0]' is to pull out the best fit vector. lstsq returns a list.
    return cl, dot(A,cl), x

def compare_coeff(coeff_1, coeff_2):
    v = abs(coeff_1-coeff_2)
    return v, max(v)

if __name__ == '__main__':
    data = linspace(-2*math.pi,4*math.pi,100)
    plot_any(ex(data), data, 1, 'log(e^x)','x','Semilog plot of e^x',2,'b','-')
    plot_any(coscos(data), data, 2, 'cos(cos(x))','x','Plot of cos(cos(x))',1,'b','-')
    ##coscos
    coef, a, b = find_coeff(coscos) # Finding coefficients through integration
    mat, estim, _range = matrix(coscos) # Finding coefficients through matrix method
    plot_any(estim, _range, 2, 'cos(cos(x))','x','loglog plot of cos(cos(x))',1,'g','.','Estimated curve')
    plot_any(coscos(data), data, 2, 'log(e^x)','x','Semilog plot of e^x',2,'y','-','2Pi periodic')
    cc_diff, cc_maxdiff = compare_coeff(coef, mat) # Finding absolute error between the two found coefficients
    print('MaxError for cos(cos(x)) is ',cc_maxdiff)
    x = [(i+1)//2 for i in range(50)];x.append(25);x = asarray(x) # Finding the relevant indices
    plot_any(abs(asarray(coef)), x, 5, 'coeff of cos(cos(x))','x','Semilog plot of fourier coefficients of cos(cos(x))',2,'r','.','Coefficients from integration')
    plot_any(abs(asarray(mat)), x, 5, 'coeff of cos(cos(x))','x','Semilog plot of fourier coefficients of cos(cos(x))',2,'g','.','Matrix Method')
    plot_any(abs(asarray(coef)), x, 6, 'coeff of cos(cos(x))','x','loglog plot of fourier coefficients of cos(cos(x))',3,'r','.','Integration')
    plot_any(abs(asarray(mat)), x, 6, 'coeff of cos(cos(x))','x','loglog plot of fourier coefficients of cos(cos(x))',3,'g','.','Matrix  Method')

    ###ex
    coef, a, b = find_coeff() # Finding coefficients through integration
    mat, estim, _range = matrix() # Finding coefficients through matrix method
    plot_any(estim, _range, 1, 'log(e^x)','x','Semilog plot of e^x',2,'g','.','Estimated plot')
    plot_any(ex(data%(2*pi)), data, 1, 'log(e^x)','x','Semilog plot of e^x',2,'y','-','2Pi periodic')
    ex_diff, ex_maxdiff = compare_coeff(coef, mat) # Finding absolute error between the two found coefficients
    print('MaxError for e^x is ',ex_maxdiff)
    plot_any(abs(asarray(coef)), x, 3, 'coeff of e^x','x','Semilog plot of fourier coefficients of e^x',2,'r','.','Coefficients from Integration')
    plot_any(abs(asarray(mat)), x, 3, 'coeff of e^x','x','Semilog plot of fourier coefficients of e^x',2,'g','.','Coefficients from matrix Method')
    plot_any(abs(asarray(coef)), x, 4, 'coeff of e^x','x','loglog plot of fourier coefficients of e^x',3,'r','.','Coefficients from Integration')
    plot_any(abs(asarray(mat)), x, 4, 'coeff of e^x','x','loglog plot of fourier coefficients of e^x',3,'g','.','Coefficients from matrix method')

    show()
