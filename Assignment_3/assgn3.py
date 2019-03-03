from pylab import *
import scipy.special as sp

data = loadtxt('fitting.dat')

##Splitting the data
t = data[:,0]
yy = data[:,1:]
sigma = logspace(-1,-3,9)

def g(t, A, B):
    ##Step 4
    return A*sp.jn(2,t) + B*t

def plot_curves_legend(_t, y):
    ##Step 3
    plot(_t, y)
    legend(sigma)
    show()

def plot_ideal():
    ##Step 4
    plot(t, g(t, 1.05, -0.105))
    show()

def plot_error_bars(t, data, sigma):
    plot(t, g(t, 1.05, -0.105))
    errorbar(t[::5],data[::5], sigma, fmt='ro')
    show()

###### Plots ######
plot_ideal()
plot_curves_legend(t,yy)
plot_error_bars(t, yy[:,0], sigma[0])

def mse(fk):
    #step 7 and 8
    error = zeros((21,21))
    for a in range(0,21,1):
        for b in range(-20,1,1):
            error[a,b+20] = sum((fk - g(t,float(a)/10,float(b)/100))**2)/101
    x = linspace(0,2,21)
    y = linspace(-0.2,0,21)
    cont = contour(x,y,error,20)
    clabel(cont, cont.levels[0:5])
    colorbar()
    show()
mse(yy[:,0])

def create_mat():
    #step 6
    M = concatenate((sp.jn(2,t).reshape((len(t),1)),t.reshape((len(t),1))), axis = 1)
    return M

def best_estimate(fk):
    #Step 9
    # Returns the value of (A,B) and the error for fk
    M = create_mat()
    p, residue, rank, s = lstsq(M, fk)
    #error = sum((fk - g(t, p[0],p[1]))**2)
    print(p)
    return p
#print(best_estimate(yy[:,0]))

def plot_error():
    error = zeros((len(sigma),2))
    for i in range(len(sigma)):
        p = best_estimate(yy[:,i])
        error[i,0] = abs(p[0]-1.05)
        error[i,1] = abs(p[1]+0.105)
    plot(sigma,error,'o-')
    leg = ['errorA','errorB']
    legend(leg)
    show()
plot_error()

def plot_log_error():
    error = zeros((len(sigma),2))
    for i in range(len(sigma)):
        p = best_estimate(yy[:,i])
        error[i,0] = abs(p[0]-1.05)
        error[i,1] = abs(p[1]+0.105)
    loglog(sigma,error,'o-')
    leg = ['errorA','errorB']
    legend(leg)
    show()
plot_log_error()
