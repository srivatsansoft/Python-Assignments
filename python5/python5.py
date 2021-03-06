from pylab import *
import mpl_toolkits.mplot3d.axes3d as p3 #Import for 3D plot
import sys #import for command line arguments

#default values of the variables
Nx = 25
Ny = 25
Nbegin = 8
Nend = 17
Niter = 1500

if(len(sys.argv)==6):   #values obtained from command line
        Nx,Ny,Nbegin,Nend,Niter = int(sys.argv[1:])

phi = zeros((Nx,Ny))    #2D array which contains the potential distribution
phi[0][Nbegin:Nend+1] = ones(Nend-Nbegin+1)     #assigning the electrode potential
oldphi = phi.copy()
errors = zeros(Niter)
for i in range(Niter):
        oldphi = phi.copy()     #creating a copy of potential
        #mean value theorem for finding potential
        phi[1:-1,1:-1] = 0.25*(phi[1:-1,0:-2] + phi[1:-1,2:] + phi[0:-2,1:-1] + phi[2:,1:-1])
        #boundary conditions
        phi[1:-1,0] =  phi[1:-1,1]
        phi[1:-1,-1] =  phi[1:-1,-2]
        phi[0,1:Nbegin] = phi[1,1:Nbegin]
        phi[0,Nend+1:-1] = phi[1,Nend+1:-1]
        phi[-1,1:Nbegin] = phi[-2,1:Nbegin]
        phi[-1,Nend+1:-1] = phi[-2,Nend+1:-1]
        #storing errors in a list
        errors[i] = amax(abs(phi - oldphi))
        
#plot of errors and their best fits
figure(1)
xdata = arange(1,Niter+1,1)
A = c_[xdata,ones(size(xdata))]
out1 = lstsq(A, np.log(errors))[0]
#taken from 500 values as it is approx. linear after that
out2 = lstsq(A[500:], np.log(errors[500:]))[0] 
#finding y data by maultiplying coeff. matrix and variable matrix
ydata1 = np.exp(dot(A,out1))
ydata2 = np.exp(dot(A,out2))
#plotting every 50 th value for better readability
plot(xdata[::50], errors[::50], 'ro', xdata, ydata1, 'b', xdata[500:], ydata2[500:], 'g')
legend(('error','fit1','fit2')) #legend for the plot
yscale('log') #making the yscale in log
xlabel('Number of iterations')
ylabel('Error')
title('Error vs Number of Iterations')

#Potential distribution of a surface in 3D plot
fig=figure(2) # open a new figure
ax=p3.Axes3D(fig) # Axes3D is the means to do a surface plot
x=arange(1,Nx+1) # create x and y axes
y=arange(1,Ny+1)
X,Y=meshgrid(x,y) # creates arrays out of x and y
title("The 3-D surface plot of the potential")
surf = ax.plot_surface(Y, X, phi, rstride=1, cstride=1, cmap=cm.jet)

#Plots the contour of the potential in the resistor
figure(3)
contour(y,x,phi.transpose())
xlabel('y')
ylabel('x')
title('Contour Plot of Potential')

#Vector plot of the J vector
figure(4)
Jx = zeros((Nx,Ny))
Jy = zeros((Nx,Ny))
Jx[1:-1,1:-1] = 0.5*(phi[1:-1,0:-2]-phi[1:-1,2:])
Jy[1:-1,1:-1] = 0.5*(phi[0:-2,1:-1]-phi[2:,1:-1])
quiver(y,x,Jy.transpose(),Jx.transpose())
xlabel('y')
ylabel('x')
title('Vector Plot of J')

Iavg = sum(sqrt(Jx[2]**2 + Jy[2]**2) + sqrt(Jx[-2]**2 + Jy[-2]**2))/Ny
Idif = abs(sum(sqrt(Jx[2]**2 + Jy[2]**2) - sqrt(Jx[-2]**2 + Jy[-2]**2)))/Ny
#printing the Average current entering and leaving and the difference between them
print Iavg,Idif

#Error is calculated by varying Nx and Ny
error = []
def meanSquare( Nx, Ny):
        phi = zeros((Nx,Ny))
        phi[0] = ones(Ny)
        for i in range(Niter):
                phi[1:-1,1:-1] = 0.25*(phi[1:-1,0:-2] + phi[1:-1,2:] + phi[0:-2,1:-1] + phi[2:,1:-1])
                phi[1:-1,0] =  phi[1:-1,1]
                phi[1:-1,-1] =  phi[1:-1,-2]
        #Theoretical value of potential varies linearly and is constructed by the dot product given below
        theory_phi = dot(ones(Nx).reshape(Nx,1),linspace(1,0,Nx).reshape(1,Nx))
        #appends the difference between calculated and theoretical phi
        error.append(sum((phi - theory_phi)**2)/(Nx*Ny))
        
#running it for only two times as the process takes lots of time to run
r = Ny/Nx
N = 10
Nx = arange(0,N)*10+Nx
Ny = r*Nx
for i in range(0,N):
        meanSquare(Nx[i], Ny[i])
        
#Plotting the error list
figure(5)
plot(Nx,error)
xlabel('Nx')
ylabel('Difference')
title('Error vs Nx')
show()

