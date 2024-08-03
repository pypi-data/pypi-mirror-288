=========
rightness
=========

Installation
------------

To install rightness, you can use `pip`. Open your terminal and run:

.. code-block:: bash

    pip install rightness

Usage
-----

The project contains the class RightObject that defines 

.. code-block:: python

    def __radd__(self, other):
        return type(self)(other) + self

as well as __ge__, __gt__, __radd__, __rand__, __rdivmod__, __rfloordiv__, __rlshift__, __rmatmul__, __rmod__, __rmul__, __ror__, __rpow__, __rrshift__, __rsub__, __rtruediv__, and __rxor__ accordingly.
The class RightObject may serve as a parent for custom datatypes. 

License
-------

This project is licensed under the MIT License.

Links
-----

* `Download <https://pypi.org/project/rightness/#files>`_
* `Source <https://github.com/johannes-programming/rightness>`_

Credits
-------
- Author: Johannes
- Email: johannes-programming@mailfence.com

Thank you for using rightness!
