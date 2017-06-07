Complex Numbers - python 
========================

https://docs.python.org/2/library/cmath.html

This module is always available. It provides access to mathematical functions for complex numbers. 
The functions in this module accept integers, floating-point numbers or complex numbers as arguments. 
They will also accept any Python object that has either a __complex__() or a __float__() method. 

.. code-block:: python
	z == z.real + z.imag*1j
	cmath.pi
	cmath.e
	
The generic methods available at cmath
--------------------------------------	
.. code-block:: python
	phase(complex(-1.0, 0.0))	# Return the phase of x 
	polar(x)					# Return the representation of x in polar coordinates.
	rect(r, phi)				# Return the complex number x with polar coordinates r and phi.
	exp(x)						# Return the exponential value e**x
	log(x[, base])				# Returns the logarithm of x to the given base.
	sqrt(x)						# Return the square root of x
	
Trigonometri
------------
.. code-block:: python
	atan / tan(x)	 	# Return the arc tangent of x / tangent
	asin / sin(x)		# Return the arc sine of x / sine
	acos / cos(x)		# Return the arc cosine of x / cosine
	
Hyberbolic
----------
https://en.wikipedia.org/wiki/Hyperbolic_geometry
.. code-block:: python
	acosh / cosh(x)		# Return the inverse hyperbolic cosine of x / hyperbolic cosine of x
	asinh / sinh(x)
	atanh / tanh(x)
	