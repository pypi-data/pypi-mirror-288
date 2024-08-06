# dual_numbers
2D Dual numbers for python, can trivially use complex numbers as scalars.

## What are dual numbers?
Python uses ```j``` for the imaginary unit, here we use ```d```  for
the dual unit, in order to differentiate it from scientific notation.
 
```d^2 = 0```

```exp(a*d)=1+a*d```

Since complex numbers can make rotations be done as multiplication,
dual numbers can make posible translation as multiplication. As the dual
part squares to 0, they can also be used for automatic differentiation:

```f(x+d) = f(x) + f'(x)d```

Note: in complex numbers, `f'(x) = Img(f(x+i*dx))/dx`. See [this](https://www.hedonisticlearning.com/posts/complex-step-differentiation.html)
for an explanation.

More info in [wikipedia](https://en.wikipedia.org/wiki/Dual_number).
## How to use:
To declare a dual number:
```
a=dual(1,2)
a
>>> (1+2d)
b=3 .d + 1
b
>>> (1+3d)
b=3.0.d+1
b
>>> (1+3d)
c=dual(1) # same as complex(1)
c
>>> (1+0d)
c.real
>>> 1
c.dl
>>> 0
dual(1+1j,2).real
>>> (1+1j) # This is not a bug, but a feature.
```

To add them, make sure the dual number comes first, since we cannot modify
python's integer and float methods for adding:

```
a=1 .d + 2
b=1
a+b
>>> (3+1d) # CORRECT!!
b+a
>>> Error: "+" not defined for int with dual
```

So make sure to declare all your numbers as dual if you dont 
want to deal with these.

Basic arithmetic operations `+,-,*,/,exp,log,abs,arg` work as intended if both
operands are dual. See docs or code for the cases when numbers are promoted.

* `a+b`,`a-b`,`a*b`, `a/b`, `a**b` work as expected.
* `a.exp()` and `a.log()` return their respective values. 
* `a.abs()` returns the real part, and `a.arg()` returns `a.dl/a.real`
See docs or code for extending to other algebras ex.: `exp(self,f=mathmodule)`.

In case there is a math domain error, python handles them as usual, ex.:
```
a=1 .d # pure dual numbers do not have inverse
a**-1
>>> ValueError: math domain error
```
## Requirements
Install these with pip install as usual:

* custom_literals (for easy dual declaration with `.d`)
* forbiddenfruit (dependency for the former)

### Use case example: Dual quaternions

Lets import a sane quaternion lib, like `pip install quaternions`.

In order to extend all operations, all "scalars" of a dual must be
quaternions, and we can also [define](https://en.wikipedia.org/wiki/Quaternion#Functions_of_a_quaternion_variable) 
our own exp() and log() functions for them, 
and provide them to the library for use:

```
import quaternions.quaternion
from dual_numbers import *
import math as m

qt=quaternions.quaternion.Quaternion

def qtexp(q):
        if type(q) in [type(1),type(1.0)]:
                return qt(m.exp(q),0,0,0)
        v=qt(0,q.x,q.y,q.z)
        norm=v.norm()
        v_u=v.unit()
        real=m.cos(norm)
        return (v_u*m.sin(norm)+qt(real,0,0,0))*m.exp(q.w)

def qtlog(q):
        v=qt(0,q.x,q.y,q.z)
        v_u=v.unit()
        return v_u*m.acos(q.w/q.norm())+qt(m.log(q.norm),0,0,0)
```

Then, we can extend quaternions easily to dual quaternions:

```
q1=qt(1,1,0,0)
q2=qt(1,1,0,0)
unit=qt(1,0,0,0)
dual(q1,q2).exp(fexp=qtexp)
>>> (<1.469, 2.287, 0.0, 0.0>+<-0.819, 3.756, 0.0, 0.0>d)
dual(q1,q2)+dual(q1,unit)
>>> (<2, 2, 0, 0>+<2, 1, 0, 0>d)
```

## TODO
- [ ] Test the library
- [X] Add wheel
- [ ] Make docs
- [X] Put more use cases
- [ ] Give more links
