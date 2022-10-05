class poly():
    """
    Implements polynomial
        p(x) = a_d x^d + ... + a_1 x + a_0
    as formal object with coefficients
        [a_0, a_1, ..., a_d]
    belonging to any numerical class with arithmetic.
    
    Input is 
        list:  [p_0, p_1, ..., p_d] 
        tuple: (p_0, p_1, ..., p_d)
        dict: {0:p_0, 1:p_1, ..., d:p_d}

    Empty list/tuple/dict produces 0 polynomial.

    Regardless of input, polynomial is initialized 
    as list of coefficients with trailing zeroes 
    stripped away (above degree of polynomial).

    Variable name is arbitrary string ('x' by default).

    Attributes of p = poly(coeffs) 
        p.coeffs    ->  list of coefficients
        p.deg       ->  degree of polynomial
        p.var_name  ->  variable name for string representation
    
    Methods 
        p.get_coeff(k)  ->  coefficient of x^k
        p.evaluate(x0)  ->  value p(x0)

    Dunder methods (polynomials a, b and natural number n)
        unary: +a, -a
        binary: a + b, a - b, a * b, a // b, a % b, a ** n
    
    e.g. 
    
    > p = poly([1, -2, 0, 1]) 
    > print(p)
    x^3 - 2x + 1
    > q = poly({5:1, 0:-1})
    > q.deg
    5
    > q.coeffs 
    [-1, 0, 0, 0, 0, 1]
    > print(q)
    x^5 - 1
    > q + p
    x^5 + x^3 - 2x
    > q // p

    """    

    def __init__(self, coeffs, var_name='x'): 
        # initialize coefficient list from input 
        # list: [p_0, p_1, ..., p_d] 
        # or tuple: (p_0, p_1, ..., p_d)
        if type(coeffs) in [list, tuple]:
            self.coeffs = list(coeffs)
        # from dictionary: {degree: coefficient}
        elif type(coeffs) == dict:
            self.coeffs = []
            keys = list(coeffs.keys())
            if keys: 
                deg = max(keys)
                for d in range(deg+1):
                    c = coeffs.get(d)
                    if c:
                        self.coeffs.append(c)
                    else:
                        self.coeffs.append(0)
        if any(self.coeffs):
            while self.coeffs[-1] == 0:         # strip trailing zeroes
                self.coeffs.pop()
            self.deg = len(self.coeffs) - 1
        else:
            self.coeffs = []                    # deg(0) = -1
            self.deg = -1
        self.var_name = var_name                # "pretty print" variable

    def __hash__(self):
        """"
        Returns hash(p) 
        for polynomial p.
        """
        return hash(self.coeffs)

    def __eq__(self, other):
        """
        Returns boolean a == b 
        for polynomials a and b 
        by comparing coefficient lists.
        """
        return self.deg == other.deg and self.coeffs == other.coeffs

    def __ne__(self, other): 
        """
        Returns boolean a != b 
        for polynomials a and b.
        by comparing coefficient lists.
        """
        return not(self == other)

    def __repr__(self): 
        """
        Returns "pretty print" string representation 
        of polynomial p with terms in order of descending degree
        and nonzero terms excluded. 

        e.g. 

        > p = poly([1, -2, 0, -1]) 
        > print(p)
        -x^3 - 2x + 1
        """
        if self.deg == -1:
            st = '0'
        else:
            nonzero_coeffs = [(d, c) for (d, c) in enumerate(self.coeffs) if c != 0]
            (d, c) = nonzero_coeffs.pop()
            if c == -1: 
                terms = [print_monomial(d, '-', self.var_name)]
            else: 
                terms = [print_monomial(d, c, self.var_name)]
            while nonzero_coeffs:
                (d, c) = nonzero_coeffs.pop()
                terms.append(sgn(c))
                terms.append(print_monomial(d, abs(c), self.var_name))
            st = ' '.join(terms)
        return st

    def __pos__(self):
        """
        Returns positive copy 
            +a
        where a is a polynomial.
        """
        return poly(self.coeffs, var_name=self.var_name)

    def __neg__(self):
        """
        Returns negation 
            -a
        where a is a polynomial.
        """
        neg_coeffs = [-c for c in self.coeffs]
        return poly(neg_coeffs, var_name=self.var_name)

    def __add__(self, other):
        """
        Returns sum 
            a + b 
        where a and b are polynomials.
        """
        if self.deg == -1:                  # self == 0
            return other
        elif other.deg == -1:               # other == 0
            return self

        L_coeffs = self.coeffs
        R_coeffs = other.coeffs
        deg = max(self.deg, other.deg)
        L_coeffs.extend((deg - self.deg)*[0])
        R_coeffs.extend((deg - other.deg)*[0])
        sum_coeffs = [L + R for (L, R) in zip(L_coeffs, R_coeffs)]
        return poly(sum_coeffs, var_name=self.var_name)
    
    def __sub__(self, other):
        """
        Returns difference 
            a - b 
        where a and b are polynomials.
        """
        return self + (-other)
    
    def __mul__(self, other):
        """
        Returns product 
            a * b
        where a and b are polynomials.

        If b is of class int or float, 
        then b is silently converted to 
        constant (degree 0) polynomial.
        """ 
        if type(other) in (int, float):
            return self * poly([other])
        
        if self.deg == -1:                  # self == 0
            return self
        elif other.deg == -1:               # other == 0
            return other

        prod_coeffs = []
        # discrete convolution 
        for d in range(self.deg + other.deg + 1):
            coeff = sum([self.get_coeff(k) * other.get_coeff(d-k) for k in range(d+1)])
            prod_coeffs.append(coeff)
        return poly(prod_coeffs, var_name=self.var_name) 

    # to fix: DivisionByZero error with sparse polynomials
    # to improve: reduce common factors x^c before long division

    def __floordiv__(self, other, int_coeffs=True): 
        """
        Returns quotient q = a // b for polynomials a and b, 
        where a = q * b + r and
        either r == 0 or deg(r) < deg(b).
        """
        deg_diff = self.deg - other.deg
        if deg_diff < 0:
            return poly([0])
        else: 
            if int_coeffs:
                quot_coeff = self.coeffs[-1] // other.coeffs[-1]
            else:
                quot_coeff = self.coeffs[-1] / other.coeffs[-1]
            quot_term = poly({deg_diff: quot_coeff}) 
            return quot_term + (self - quot_term*other).__floordiv__(other, int_coeffs)

    def __mod__(self, other):
        """
        Returns remainder r = a % b for polynomials a and b, 
        where a = q * b + r and 
        either r == 0 or deg(r) < deg(b).
        """
        return self - (self // other) * other

    def __divmod__(self, other):
        """
        Returns quotient and remainder (q, r) = (a // b, a % b) 
        for polynomials a and b, 
        where a = q * b + r and 
        either r == 0 or deg(r) < deg(b).
        """
        return (self // other, self % other)

    def __pow__(self, n): 
        """
        Returns non-negative integer power
            p^n = p**n
        for polynomial p.

        """
        if n == 0: 
            return poly([1])
        else: 
            return self * (self**(n-1))
    
    def get_coeff(self, k):
        """
        Returns coefficient of degree k term 
        of polynomial, 
        defaulting to 0 if not available.
        """
        if 0 <= k and k <= self.deg:
            return self.coeffs[k]
        else:
            return 0

    def evaluate(self, x0): 
        """
        Evaluate polynomial at input x0 
            p(x0)
        using Horner's method.
        """
        y0 = 0
        for c in reversed(self.coeffs):
            y0 = x0*y0 + c
        return y0

##### 
# END of class definition 
#####


def sgn(n):
    """
    Returns sign of input as string. 
    For positive n, 
        sgn(+n) = '+'
        sgn(0)  = ''
        sgn(-n) = '-'        
    """
    if n > 0:
        return '+'
    elif n < 0:
        return '-'
    else:
        return ''

def print_monomial(deg, coeff, var):
    """
    Returns "pretty print" string representation 
    of degree k term of polynomial p.

    e.g. 
    
    > print_monomial(2, -5, 'x')
    '-5x^2'
    
    > print_monomial(1, 3, 'y')
    '3y'
    
    > print_monomial(4, 1, 'z')
    'z^4'
    """
    if deg == 0:
        st = str(coeff)
    else:
        if coeff == 1:
            coeff_str = ''
        else:
            coeff_str = str(coeff)
        if deg == 1:
            st = '{}{}'.format(coeff_str, var)
        else:
            st = '{}{}^{}'.format(coeff_str, var, deg)
    return st


# Testing 

p = poly([13, 10, 5, 1]);               # x^3 + 5x^2 + 10x + 13
q = poly([2, 1]);                       # x + 1
r = poly([1 for i in range(8)]);        # x^7 + x^6 + ... + x + 1
z = poly([]);                           # 0

