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
```Note: in complex numbers, f'(x) = Img(f(x+i*dx))/dx```

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

Basic arithmetic operations `+,-,*,/,exp,log` work as intended if both
operands are dual. See docs or code for the cases when numbers are promoted.

* `a+b`,`a-b`,`a*b`, etc
* `a.exp()` and `a.log()` return their respective values. 
See docs or code for extending to other algebras ex.: `exp(self,f=mathmodule)`.

## Requirements
Install these with pip install as usual:

* custom_literals (for easy dual declaration with `.d`)
* forbiddenfruit (dependency for the former)

## TODO
- [ ] Test the library
- [ ] Make literals optional
- [ ] Add wheel
- [ ] Make docs
- [ ] Put more use cases
- [ ] Give more links
