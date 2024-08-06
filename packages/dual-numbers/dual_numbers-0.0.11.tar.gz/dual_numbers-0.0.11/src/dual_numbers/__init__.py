#import dual_numbers
__all__ = ["dual"]

from custom_literals import *
import math
import cmath

class dual():
	def __init__(self,real,dl=0):
		self.real=real
		self.dl=dl
	def __format__(self):
		return f"{self.real}+{self.dl}d"
	def __repr__(self):
		return f"({self.real}+{self.dl}d)"
	def __add__(self,a):
		if type(a)!=type(dual(0,0)):
			return self+dual(a,0)
		return dual(self.real+a.real,self.dl+a.dl)
	def __radd_(self,a):
		return self+a
	def __mul__(self,a):
		if type(a)!=type(dual(0,0)):
			return dual(self.real*a,self.dl*a)
		return dual(self.real*a.real,self.real*a.dl+self.dl*a.real)
	def __rmul__(self,a):
		return self*a
	def __sub__(self,a):
		if type(a)!=type(dual(0,0)):
			return dual(self.real-a,self.dl)
		return dual(self.real-a.real,self.dl-a.dl)
	def __rsub__(self,a):
		return (self-a)*(-1)
	def conjugate(self):
		return dual(self.real,-1*self.dl)
	def __truediv__(self,a):
		if type(a)!=type(dual(0,0)):
			return dual(self.real/a,self.dl/a)
		return self*(a.conjugate())*(a.real**-2)
	def __rtruediv__(self,a):
		if type(a)!=type(dual(0,0)):
			return dual(a,0)/self
		return a/self
	def exp(self,a=False,fexp=cmath.exp): #return exp(self)
		if type(a)==type(dual(0,0)): # as method
			return a.exp()
		if type(self.real)==type(1) or type(self.real)==type(1.0):
			fexp=math.exp
		k=dual(fexp(self.real),0)
		return dual(fexp(0),self.dl)*k
	def log(self,a=False,flog=math.log):
		if type(a)==type(dual(0,0)): # as method
			return a.log()
		#if type(a)!=type(True) and type(a)!=type(dual(0,0)):
		#	return dual(a,0).log()
		if type(self.real)==type(1+1j):
			flog=cmath.log
		return dual(flog(self.real),self.dl/self.real)
	def __pow__(self,a,f=cmath.exp): # greater precision for int values
		#if type(a)==type(1) and a>0 and iter:
		#	r=self
		#	for i in range(1,a):
		#		r=r*self
		#	return r
		return dual.exp(self.log()*a,fexp=f)
	def __rpow__(self,a):
		return (dual.log(a))**(self)
	def pow(self,a,b,fexp=cmath.exp):
		return a.__pow__(b,f=fexp)
	def __eq__(self,a):
		return (self.real==a.real)and(self.dl==a.dl)
	def abs(self):
		return self.real
	def arg(self):
		return self.dl/self.real

@literal(float,int,name="d")
def makedual(self):
	return dual(0,self)
