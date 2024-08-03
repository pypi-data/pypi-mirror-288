class RightObject:
    pass

class _Setup:
    @classmethod
    def _get_rfunc(cls, l):
        def ans(self, other):
            c = type(self)
            x = c(other)
            if c is not type(x):
                raise TypeError(x)
            f = getattr(c, l)
            z = f(x, self)
            return z
        return ans
    @classmethod
    def _rmagic(cls, lname, rname=None):
        if rname is None:
            rname = "r" + lname
        lname = "__" + lname + "__"
        rname = "__" + rname + "__"
        rfunc = cls._get_rfunc(lname)
        rfunc.__name__ = rname
        setattr(RightObject, rname, rfunc)
    @classmethod
    def rmagics(cls):
        cls._rmagic("add")
        cls._rmagic("and")
        cls._rmagic("divmod")
        cls._rmagic("floordiv")
        cls._rmagic("lshift")
        cls._rmagic("mod")
        cls._rmagic("mul")
        cls._rmagic("or")
        cls._rmagic("pow")
        cls._rmagic("rshift")
        cls._rmagic("sub")
        cls._rmagic("truediv")
        cls._rmagic("xor")
        cls._rmagic("lt", "gt")
        cls._rmagic("le", "ge")
            
_Setup.rmagics()