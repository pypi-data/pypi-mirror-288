#! /usr/bin/env python

from eclib.numutils import *
from eclib.randutils import *
from eclib.primeutils import *
from eclib.modutils import *
from collections import namedtuple
import numpy as np
from numpy.polynomial import Polynomial as P
from math import floor, log

def pmod(p, f, m):
    return P(np.array([int(c) % m for c in (p % f).coef], dtype=int))

def get_rand_poly(min, max, size):
    return P(np.array([get_rand(min, max) for _ in range(size)], dtype=int))

def get_int_gaussian_poly(sigma, size):
    return P(np.array(get_int_gaussian(0, sigma, size), dtype=int))

def bit_reverse(params, v):
    if isinstance(v, list) or isinstance(v, tuple):
        v = np.array(v, dtype=int)
    
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

def ntt(params, v):
    a = v.copy()
    n = params.N
    q = params.t
    table = params.roots

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

def intt(params, v):
    a = v.copy()
    n = params.N
    q = params.t
    table = params.roots_inv

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

def base_decomp(params, p):
    return np.array([P((p.coef // pow(params.T, i)) % params.T) for i in range(params.l + 1)], dtype=object)

def keygen(N, t, q, sigma, T=2):
    params = namedtuple('Parameters', ['N', 't', 'q', 'sigma', 'T', 'f', 'l', 'roots', 'roots_inv'])
    params.N = N
    params.t = t
    params.q = q
    params.sigma = sigma
    params.T = T

    coef = np.zeros(params.N + 1, dtype=int)
    coef[0] = 1
    coef[-1] = 1
    params.f = P(coef)

    params.l = floor(log(params.q, T))

    root = 2
    while mpow(root, (params.t - 1) // 2, params.t) == 1:
        root += 1
    Mth_root = mpow(root, (params.t - 1) // (2 * params.N), params.t)
    params.roots = bit_reverse(params, np.array([mpow(Mth_root, i, params.t) for i in range(params.N)], dtype=int))
    params.roots_inv = np.array([minv(w, params.t) for w in params.roots], dtype=int)

    sk = get_rand_poly(0, 2, params.N)

    a = get_rand_poly(0, params.q, params.N)
    e = get_int_gaussian_poly(params.sigma, params.N)
    pk = np.array([pmod(-(a * sk + e), params.f, params.q), a], dtype=object)

    rlk = []
    for i in range(params.l + 1):
        a = get_rand_poly(0, params.q, params.N)
        e = get_int_gaussian_poly(params.sigma, params.N)
        rlk.append(np.array([pmod(-(a * sk + e) + pow(params.T, i) * pow(sk, 2), params.f, params.q), a], dtype=object))
    rlk = np.array(rlk, dtype=object)

    return params, pk, sk, rlk

def encrypt(params, pk, m):
    u = get_rand_poly(0, 2, params.N)
    e1 = get_int_gaussian_poly(params.sigma, params.N)
    e2 = get_int_gaussian_poly(params.sigma, params.N)
    c_0 = pmod(pk[0] * u + e1 + floor(params.q / params.t) * m, params.f, params.q)
    c_1 = pmod(pk[1] * u + e2, params.f, params.q)
    return np.array([c_0, c_1], dtype=object)

def decrypt(params, sk, c):
    return pmod(P(np.floor((params.t / params.q) * pmod(c[0] + c[1] * sk, params.f, params.q).coef + 0.5)), params.f, params.t)

def add(params, c1, c2):
    c_0 = pmod(c1[0] + c2[0], params.f, params.q)
    c_1 = pmod(c1[1] + c2[1], params.f, params.q)
    return np.array([c_0, c_1], dtype=object)

def mult(params, c1, c2):
    c_0 = pmod(P(np.floor((params.t / params.q) * (c1[0] * c2[0]).coef + 0.5)), params.f, params.q)
    c_1 = pmod(P(np.floor((params.t / params.q) * (c1[0] * c2[1] + c1[1] * c2[0]).coef + 0.5)), params.f, params.q)
    c_2 = pmod(P(np.floor((params.t / params.q) * (c1[1] * c2[1]).coef + 0.5)), params.f, params.q)
    return np.array([c_0, c_1, c_2], dtype=object)

def int_mult(params, m, c):
    c_0 = pmod(m * c[0], params.f, params.q)
    c_1 = pmod(m * c[1], params.f, params.q)
    return np.array([c_0, c_1], dtype=object)

def relin(params, rlk, c):
    c_2 = base_decomp(params, c[2])
    c_0 = pmod(c[0] + sum(np.array([rlk[i][0] * c_2[i] for i in range(params.l + 1)], dtype=object)), params.f, params.q)
    c_1 = pmod(c[1] + sum(np.array([rlk[i][1] * c_2[i] for i in range(params.l + 1)], dtype=object)), params.f, params.q)
    return np.array([c_0, c_1], dtype=object)

def pack(params, v):
    if isinstance(v, list) or isinstance(v, tuple):
        v = np.array(v, dtype=int)

    return pmod(P(intt(params, np.pad(v, [0, params.N - v.shape[0]]))), params.f, params.t)

def unpack(params, m):
    return np.mod(ntt(params, np.pad(m.coef, [0, params.N - m.coef.shape[0]])), params.t)

def rotate(params, m, k):
    return pmod(P(np.pad(m.coef, [(2 * k) - 1, 0])), params.f, params.q)

N = pow(2, 8)
q = get_prime(60)
t = get_prime(13)
while t % (2 * N) != 1:
    t = get_prime(13)
sigma = 3.2

params, pk, sk, rlk = keygen(N, t, q, sigma)

print(f'N = {params.N}')
print(f'q = {params.q}')
print(f't = {params.t}')
print(f'\u03C3 = {params.sigma}')
print(f'T = {params.T}')

# v1 = np.array([(params.t // 2) - 1, -(params.t // 2) + 1], dtype=int)
v1 = np.array([1, 2, -3], dtype=int)
v2 = np.array([-4, 5, -6], dtype=int)

m1 = pack(params, v1)
print(f'done: packing v1')
m2 = pack(params, v2)
print(f'done: packing v2')

c1 = encrypt(params, pk, m1)
print(f'done: encrypting m1')
c2 = encrypt(params, pk, m2)
print(f'done: encrypting m2')
c3 = add(params, c1, c2)
print(f'done: addition')
c4 = int_mult(params, m2, c1)
print(f'done: plaintext multiplication')
c5 = relin(params, rlk, mult(params, c1, c2))
print(f'done: multiplication')

m1_ = decrypt(params, sk, c1)
print(f'done: decrypting c1')
m2_ = decrypt(params, sk, c2)
print(f'done: decrypting c2')
m3 = decrypt(params, sk, c3)
print(f'done: decrypting c3')
m4 = decrypt(params, sk, c4)
print(f'done: decrypting c4')
m5 = decrypt(params, sk, c5)
print(f'done: decrypting c5')

v1_ = unpack(params, m1_)
print(f'done: unpacking m1_')
v2_ = unpack(params, m2_)
print(f'done: unpacking m2_')
v1 = unpack(params, m1)
print(f'done: unpacking m1')
v2 = unpack(params, m2)
print(f'done: unpacking m2')
v3 = unpack(params, m3)
print(f'done: unpacking m3')
v4 = unpack(params, m4)
print(f'done: unpacking m4')
v5 = unpack(params, m5)
print(f'done: unpacking m5')

print([min_residue(e, params.t) for e in np.trim_zeros(v1_, 'b')])
print([min_residue(e, params.t) for e in np.trim_zeros(v2_, 'b')])
print([min_residue(e, params.t) for e in np.trim_zeros(v1, 'b')])
print([min_residue(e, params.t) for e in np.trim_zeros(v2, 'b')])
print([min_residue(e, params.t) for e in np.trim_zeros(v1 + v2, 'b')])
print([min_residue(e, params.t) for e in np.trim_zeros(v3, 'b')])
print([min_residue(e, params.t) for e in np.trim_zeros(v1 * v2, 'b')])
print([min_residue(e, params.t) for e in np.trim_zeros(v4, 'b')])
print([min_residue(e, params.t) for e in np.trim_zeros(v5, 'b')])
