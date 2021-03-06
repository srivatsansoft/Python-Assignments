from scipy import *
from matplotlib.pyplot import * #For plots
import scipy.signal as signal #for analysis of LTI systems

def solveDE( n, d, t ):
	num=poly1d(n) #defining a polynomial with coeffs. n
	den=poly1d(d) #defining a polynomial with coeffs. d
	sys1=signal.lti(num,den) #define an lti signal with transfer function num/den
	y=sys1.impulse(T=t)[1] #exciting the system with an unit impulse function
	return y
	
t=linspace(0,20,201)
#Plot of Time response of Spring system
figure(1)
plot(t,solveDE( [0.1,0], [1,0,1], t) ,'r')
title("Time Response $\ddot{x}+x$")

#Plot of time response of coupled oscillations
figure(2)
plot(t,solveDE( [1,0,2,0], [1,0,3,0,0], t),'r',label='$x(t)$')
plot(t,solveDE( [2,0], [1,0,3,0,0], t),'b',label='$y(t)$')
legend()
xlabel(r'$t$')
title("Time Response of $\ddot{x}+(x-y)=0$ ; $\ddot{y}+2(y-x)=0$")

#R1,L,R2 are connected in series.
L=1e-3 
R1=10 
R2=100 
omega=logspace(3,9,61).reshape((61,1)) # decades in steps
H=R2/((R1+R2) + 1j*omega*L) #Transfer function of the two port network
figure(3)
cla()
subplot(211)
loglog(omega,abs(H),'ro') #A loglog plot
title("Frequency Response")
xlabel(r"$\omega$")
ylabel(r"$|H|$")
subplot(212)
semilogx(omega,180*angle(H)/pi,'ro') #A semilog plot
xlabel(r"$\omega$")
ylabel(r"Arg$(H)$")

#Plot of time response of input and output fot t<30us
figure(4)
t = linspace(0,30e-6,301)
inp=cos(1e3*t)-cos(1e6*t)
num1 = poly1d([1e12-1e6,0]) 
den1 = poly1d([1,0,1e12+1e6,0,1e18]) #Input signals Laplace transform
num2 = poly1d([R2])
den2 = poly1d([L,R1+R2]) #The transfer function of the two port network
num = polymul(num1,num2)
den = polymul(den1,den2) #The Laplace transform of the output
plot(t,solveDE(asarray(num), asarray(den), t),'b',label="Output")
plot(t,inp,'g',label="Input")
xlabel(r'$t$')
title("Time Response of LR Circuit")
legend()

#Plot for t<10ms (output)
figure(5)
t = arange(0,10e-3,1e-6)
plot(t,solveDE(asarray(num), asarray(den), t) ,'r')
xlabel('$t$')
title('Time response of output')

#Plot for t<10ms (input)
figure(6)
inp=cos(1e3*t)-cos(1e6*t)
plot(t,inp ,'g')
title('Time response of input')
xlabel('$t$')
show()
