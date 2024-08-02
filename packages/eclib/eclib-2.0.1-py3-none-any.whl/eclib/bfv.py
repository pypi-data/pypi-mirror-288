#! /usr/bin/env python

from eclib.numutils import *
from eclib.randutils import *
from eclib.primeutils import *
from eclib.modutils import *
from collections import namedtuple
import numpy as np
from numpy.polynomial import polynomial as P
from math import floor, log
from copy import deepcopy

class poly_ring:
    def __init__(self, coef, size):
        self.size = size

        self.poly_modulus = np.zeros(self.size + 1, dtype=int)
        self.poly_modulus[0] = 1
        self.poly_modulus[-1] = 1

        if isinstance(coef, int):
            _, self.coef = P.polydiv(np.array([coef], dtype=int), self.poly_modulus)
        elif isinstance(coef, list) or isinstance(coef, tuple):
            _, self.coef = P.polydiv(np.array(coef, dtype=int), self.poly_modulus)
        elif isinstance(coef, np.ndarray):
            _, self.coef = P.polydiv(coef, self.poly_modulus)
        else:
            raise TypeError()
        self.coef = np.array([int(e) for e in self.coef] ,dtype=int)
        
    def __add__(self, other):
        res = deepcopy(self)

        if type(other) == poly_ring:
            res.coef = P.polyadd(self.coef, other.coef)
            res.coef = np.array([int(e) for e in res.coef] ,dtype=int)
            return res
        
        raise TypeError()

    def __sub__(self, other):
        res = deepcopy(self)

        if type(other) == poly_ring:
            res.coef = P.polysub(self.coef, other.coef)
            res.coef = np.array([int(e) for e in res.coef] ,dtype=int)
            return res
        
        raise TypeError()

    def __mul__(self, other):
        res = deepcopy(self)

        if type(other) == poly_ring:
            _, res.coef = P.polydiv(P.polymul(self.coef, other.coef), self.poly_modulus)
            res.coef = np.array([int(e) for e in res.coef] ,dtype=int)
            return res
        elif type(other) == int:
            res.coef = self.coef * other
            return res
        
        raise TypeError()

    def __pow__(self, other):
        res = deepcopy(self)

        if type(other) == int:
            _, res.coef = P.polydiv(P.polypow(self.coef, other), self.poly_modulus)
            res.coef = np.array([int(e) for e in res.coef] ,dtype=int)
            return res
        
        raise TypeError()

    def __mod__(self, other):
        res = deepcopy(self)

        if type(other) == int:
            res.coef = self.coef % other
            # res.coef = self.coef - other * np.floor((self.coef - other // 2) / other)
            return res
        
        raise TypeError()

    def __rmul__(self, other):
        if type(other) == poly_ring or type(other) == int:
            return self * other
        
        raise TypeError()

    def __iadd__(self, other):
        if type(other) == poly_ring:
            self = self + other
            return self

        raise TypeError()

    def __isub__(self, other):
        if type(other) == poly_ring:
            self = self - other
            return self

        raise TypeError()

    def __imul__(self, other):
        if type(other) == poly_ring:
            self = self * other
            return self

        raise TypeError()

    def __ipow__(self, other):
        if type(other) == int:
            self = self ** other
            return self

        raise TypeError()

    def __imod__(self, other):
        if type(other) == int:
            self = self % other
            return self
        
        raise TypeError()

    def __pos__(self):
        self.coef = +self.coef
        return self
    
    def __neg__(self):
        self.coef = -self.coef
        return self

    def get_rand(min, max, size):
        return poly_ring([get_rand(min, max) for _ in range(size)], size)

    def get_int_gaussian(sigma, size):
        return poly_ring(get_int_gaussian(0, sigma, size), size)

    def base_decomp(poly, base, size):
        return np.array([poly_ring(poly.coef // (base ** i), poly.size) for i in range(size)], dtype=object)

def bit_reverse(params, v):
    if isinstance(v, list) or isinstance(v, tuple):
        v = np.array(v, dtype=int)
    elif isinstance(v, np.ndarray):
        pass
    else:
        raise TypeError()
    
    a = v.copy()
    i = 0
    for j in range(1, params.N):
        k = params.N // 2
        while(k <= i):
            i -= k
            k //= 2
        i += k
        if j < i:
            a[i], a[j] = a[j], a[i]
    
    return a

def ntt(v, n, q, table):
    if isinstance(v, list) or isinstance(v, tuple):
        v = np.array(v, dtype=int)
    elif isinstance(v, np.ndarray):
        pass
    else:
        raise TypeError()
    
    a = v.copy()
    t = n
    m = 1

    while m < n:
        t //= 2

        for i in range(m):
            j1 = 2 * i * t
            j2 = j1 + t - 1
            S = table[m + i]
            
            for j in range(j1, j2 + 1):
                U = int(a[j])
                V = int(a[j + t] * S)
                a[j] = (U + V) % q
                a[j + t] = (U - V) % q

        m *= 2
    
    return a

def intt(v, n, q, table):
    if isinstance(v, list) or isinstance(v, tuple):
        v = np.array(v, dtype=int)
    elif isinstance(v, np.ndarray):
        pass
    else:
        raise TypeError()
    
    a = v.copy()
    t = 1
    m = n

    while m > 1:
        j1 = 0
        h = m // 2

        for i in range(h):
            j2 = j1 + t - 1
            S = table[h + i]

            for j in range(j1, j2 + 1):
                U = int(a[j])
                V = int(a[j + t])
                a[j] = (U + V) % q
                a[j + t] = ((U - V) * S) % q

            j1 = j1 + 2 * t

        t *= 2
        m //= 2
    
    n_inv = minv(n, q)
    for j in range(n):
        a[j] = (a[j] * n_inv) % q
    
    return a

def keygen(N, t, q, sigma, T=2):
    params = namedtuple('Parameters', ['N', 't', 'q', 'sigma', 'scale', 'rescale', 'T', 'f', 'l', 'roots', 'roots_inv'])
    params.N = N
    params.t = t
    params.q = q
    params.sigma = sigma
    params.scale = floor(params.q / params.t)
    params.rescale = params.t / params.q
    params.T = T
    params.l = floor(log(params.q, params.T))

    root = 2
    while mpow(root, (params.t - 1) // 2, params.t) == 1:
        root += 1
    Mth_root = mpow(root, (params.t - 1) // (2 * params.N), params.t)
    params.roots = bit_reverse(params, np.array([mpow(Mth_root, i, params.t) for i in range(params.N)], dtype=int))
    params.roots_inv = np.array([minv(w, params.t) for w in params.roots], dtype=int)

    sk = poly_ring.get_rand(0, 2, params.N)

    a = poly_ring.get_rand(0, params.q, params.N)
    e = poly_ring.get_int_gaussian(params.sigma, params.N)

    pk = np.array([-(a * sk + e) % params.q, a], dtype=object)

    rlk = []
    for i in range(params.l + 1):
        a = poly_ring.get_rand(0, params.q, params.N)
        e = poly_ring.get_int_gaussian(params.sigma, params.N)
        rlk.append(np.array([(-(a * sk + e) + (params.T ** i) * (sk ** 2)) % params.q, a], dtype=object))
    rlk = np.array(rlk, dtype=object)

    return params, pk, sk, rlk

def encrypt(params, pk, m):
    u = poly_ring.get_rand(0, 2, params.N)
    e1 = poly_ring.get_int_gaussian(params.sigma, params.N)
    e2 = poly_ring.get_int_gaussian(params.sigma, params.N)

    c_0 = (pk[0] * u + e1 + params.scale * m) % params.q
    c_1 = (pk[1] * u + e2) % params.q

    return np.array([c_0, c_1], dtype=object)

def decrypt(params, sk, c):
    return poly_ring(np.floor(params.rescale * (c[0] + c[1] * sk).coef + 0.5) % params.t, params.N)

def add(params, c1, c2):
    c_0 = (c1[0] + c2[0]) % params.q
    c_1 = (c1[1] + c2[1]) % params.q
    return np.array([c_0, c_1], dtype=object)

def int_mult(params, m, c):
    c_0 = (m * c[0]) % params.q
    c_1 = (m * c[1]) % params.q
    return np.array([c_0, c_1], dtype=object)

def mult(params, c1, c2):
    c_0 = poly_ring(np.floor(params.rescale * (c1[0] * c2[0]).coef + 0.5) % params.q, params.N)
    c_1 = poly_ring(np.floor(params.rescale * (c1[0] * c2[1] + c1[1] * c2[0]).coef + 0.5) % params.q, params.N)
    c_2 = poly_ring(np.floor(params.rescale * (c1[1] * c2[1]).coef + 0.5) % params.q, params.N)
    return np.array([c_0, c_1, c_2], dtype=object)

def relin(params, rlk, c):
    c_2 = c[2].base_decomp(params.T, params.l + 1)
    c_0 = deepcopy(c[0])
    c_1 = deepcopy(c[1])
    c_0.coef = (c_0.coef + sum([(rlk[i][0] * c_2[i]).coef for i in range(params.l + 1)])) % params.q
    c_1.coef = (c_1.coef + sum([(rlk[i][1] * c_2[i]).coef for i in range(params.l + 1)])) % params.q
    return np.array([c_0, c_1], dtype=object)

def pack(params, v):
    if isinstance(v, int):
        v = np.array([v], dtype=object)
    elif isinstance(v, list) or isinstance(v, tuple):
        v = np.array(v, dtype=object)
    elif isinstance(v, np.ndarray):
        pass
    else:
        raise TypeError()
        
    v = np.pad(v, [0, params.N - v.shape[0]])
    return poly_ring(intt(v, params.N, params.t, params.roots_inv) % params.t, params.N)

def unpack(params, m):
    coef = np.pad(m.coef, [0, params.N - m.coef.shape[0]])
    return ntt(coef, params.N, params.t, params.roots) % params.t

# def rotate(params, m, k):
#     return pmod(P(np.pad(m.coef, [(2 * k) - 1, 0])), params.f, params.q)

def encode(params, x, delta):
    f = np.frompyfunc(_encode, 3, 1)
    return f(params, x, delta)

def decode(params, m, delta):
    f = np.frompyfunc(_decode, 3, 1)
    return f(params, m, delta)

def _encode(params, x, delta):
    m = floor(x / delta + 0.5)

    if m < 0:
        if m < -floor((params.t - 1) / 2):
            print('error: underflow')
            return None
        else:
            m += params.t
    elif m > floor(params.t / 2):
        print('error: overflow')
        return None

    return m

def _decode(params, m, delta):
    return min_residue(m, params.t) * delta

N = pow(2, 3)
q = get_prime(20)
t = get_prime(5)
while t % (2 * N) != 1:
    t = get_prime(5)
sigma = 3.2

params, pk, sk, rlk = keygen(N, t, q, sigma)

print(f'N = {params.N}')
print(f't = {params.t}')
print(f'q = {params.q}')
print(f'\u03C3 = {params.sigma}')

delta = 1

x1 = [1, 2, -3]
x2 = [-3, 2, -1]

v1 = encode(params, x1, delta)
v2 = encode(params, x2, delta)

m1 = pack(params, v1)
m2 = pack(params, v2)

c1 = encrypt(params, pk, m1)
c2 = encrypt(params, pk, m2)
c3 = add(params, c1, c2)
c4 = int_mult(params, m2, c1)
c5 = relin(params, rlk, mult(params, c1, c2))

m3 = decrypt(params, sk, c3)
m4 = decrypt(params, sk, c4)
m5 = decrypt(params, sk, c5)

v3 = unpack(params, m3)
v4 = unpack(params, m4)
v5 = unpack(params, m5)

x3 = decode(params, v3, delta)
x4 = decode(params, v4, delta ** 2)
x5 = decode(params, v5, delta ** 2)

print(x1)
print(x2)
print(np.trim_zeros(x3, 'b'))
print(np.trim_zeros(x4, 'b'))
print(np.trim_zeros(x5, 'b'))
