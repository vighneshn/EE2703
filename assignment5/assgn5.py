#!/usr/bin/python3.5
from pylab import *
import mpl_toolkits.mplot3d.axes3d as p3
Nx=25 # Size along x
Ny=25 # Size along y
radius= 8# Radius of central lead
Niter=1500 # Number of iterations to perform
errors = zeros(Niter)

def plot_any(y, x=None, fig=1, _ylabel='y', _xlabel='x', _title='title', plot_type=1, color='r', l_dots='-',_legend = 'Curve', save='fig.png'):
    '''
    This function plots any of the function/coefficient plots.
    It takes parameters for the x and y values, labels, titles, structure and color.
    '''
    figure(fig) # Choosing figure number
    title(_title) # Plot title
    ylabel(_ylabel) # Setting labels
    xlabel(_xlabel)
    ## To check what kind of plot we need, a regular, semilog or loglog
    if plot_type == 1:
        plot(x,y,color+l_dots, label = _legend)
    elif plot_type == 2:
        semilogy(x,y,color+l_dots, label = _legend)
    else:
        loglog(x,y,color+l_dots, label = _legend)
    legend()
    savefig(save)

#Code as given in pdf, to index the resistor
phi = zeros((Ny,Nx), dtype=float)
y = linspace(-0.5,0.5,Ny,dtype = float)
x = linspace(-0.5,0.5,Nx,dtype = float)
Y,X = meshgrid(y,x)

#Code to find the resistor region of the simulation, through which the current flows.
ii = where(X*X+Y*Y <= 0.35*0.35)
x_c, y_c = where(X*X+Y*Y <= 0.35*0.35)
phi[ii] = 1
phi_orig = phi.copy()

fig = figure(1)
title('Graph of the resistor potentials initially') # Plot title
ylabel('Length of resistor') # Setting labels
xlabel('Width of resistor')
imshow(phi)
savefig('phi.png')
for k in range(Niter):
    #1) Saving a copy of phi
    oldphi = phi.copy()
    #2) Updating phi
    phi[1:-1,1:-1] = 0.25*(phi[1:-1,0:-2] + phi[1:-1,2:] + phi[0:-2,1:-1] + phi[2:,1:-1])
    #3) Asserting the boundary condition
    phi[:,0] = phi[:,1]
    phi[:,Nx-1] = phi[:,Nx-2]
    phi[0,1:-1] = phi[1,1:-1]
    phi[Ny-1,:] = 0
    # Asserting the source condition
    phi[ii] = 1
    #4) Finding the error
    errors[k] = abs(phi - oldphi).max()

def fit_error(error, x2):
    # lstsq, Ax=b, x = logA,B, A is [1 x], b is logy
    matA = concatenate((ones((len(error),1)),x2.reshape((len(x2),1))), axis = 1)
    matb = log(error)
    logA_B = lstsq(matA,matb)[0]
    #logA_B contains the required coefficients for the error fit.
    return exp(logA_B[0]),logA_B[1]

#Plotting the error in a loglog and semilog plot
x_ = linspace(0,Niter,Niter)
plot_any(errors[::50], x_[::50], 2, 'error', 'Iterations', 'Variation of error vs iterations', 2, 'r', '.', 'Error curve','error.png')
A1,B1 = fit_error(errors,x_)
print(A1,B1)
A2,B2 = fit_error(errors[500:],x_[500:])

plot_any(A2*exp(B2*x_), x_, 2, 'error', 'Iterations', 'Variation of error vs iterations', 2,'b','-', 'fit 500 onwards','error.png')
plot_any(A1*exp(B1*x_), x_, 2, 'error', 'Iterations', 'Variation of error vs iterations', 2,'g','-', 'fit with all points','error.png')
plot_any(A2*exp(B2*x_), x_, 7, 'error', 'Iterations', 'Variation of error vs iterations', 2,'b','-', 'fit 500 onwards','error_fit_500.png')

plot_any(errors[::50], x_[::50], 8, 'error', 'Iterations', 'Variation of error vs iterations on loglog', 3, 'r', '.', 'Error curve','error_ll.png')
plot_any(A1*exp(B1*x_), x_, 8, 'error', 'Iterations', 'Variation of error vs iterations on loglog', 3,'g','-', 'fit with all points','error_ll.png')

#3D plot
fig1=figure(3)     # open a new figure
ax=p3.Axes3D(fig1) # Axes3D is the means to do a surface plot
title('The 3-D surface plot of the potential')
ylabel('Length of resistor') # Setting labels
xlabel('Width of resistor')
surf = ax.plot_surface(Y, X, phi.T, rstride=1, cstride=1, cmap=cm.jet)
savefig('3d.png')

fig = figure(4)
#Contour plot of potential.
title('Contour plot of potential') # Plot title
ylabel('Length of resistor') # Setting labels
xlabel('Width of resistor')
cont = contourf(x[::-1],y[::-1],phi,10)
colorbar()
plot((x_c-Nx/2)/(Nx*1.0),(y_c-Ny/2)/(Ny*1.0),'ro')
savefig('pot_cont.png')

fig = figure(5)
## Finding the current derivatives
Jx = 0.5*(phi[0:-2,1:-1]-phi[2:,1:-1])
Jy = 0.5*(phi[1:-1,2:]-phi[1:-1,0:-2])
title('Quiver plot of current') # Plot title
ylabel('Length of resistor') # Setting labels
xlabel('Width of resistor')
quiver(Y[1:-1,1:-1],-X[1:-1,1:-1],Jy[:,::-1],-Jx)
plot((x_c-Nx/2)/(Nx*1.0),(y_c-Ny/2)/(Ny*1.0),'ro')
savefig('quiver.png')

##Solving for the temperature
temp = 300*ones((Ny,Nx))
for i in range(Niter):
    #1) Save a copy of temp
    oldtemp = temp.copy()
    #2) Update temp
    temp[1:-1,1:-1] = 0.25*(temp[1:-1,0:-2] + temp[1:-1,2:] + temp[0:-2,1:-1] + temp[2:,1:-1] + Jx**2 + Jy**2)
    #3) Assert boundary conditions
    temp[:,0] = temp[:,1]
    temp[:,Nx-1] = temp[:,Nx-2]
    temp[0,1:-1] = temp[1,1:-1]
    temp[Ny-1,:] = 300
    #4) Assert source condition
    temp[ii] = 300
fig = figure(6)
#Contour plot of the temperature variation
cont = contourf(x[::-1],y[::-1],temp,10)
title('Contour plot of Temperature') # Plot title
ylabel('Length of resistor') # Setting labels
xlabel('Width of resistor')
plot((x_c-Nx/2)/(Nx*1.0),(y_c-Ny/2)/(Ny*1.0),'ro')
colorbar()
savefig('temp.png')
show()

