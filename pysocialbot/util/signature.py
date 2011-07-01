import random
import datetime

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
def lcm(a, b):
    return a * b / gcd(a, b)
def gcd2(a, b):
    if b == 0:
        u, v = 1, 0
    else:
        q, r = divmod(a, b)
        u0, v0 = gcd2(b, r)
        u, v = v0, (u0 - q * v0)
    return (u, v)
def isprime(q, k=50):
    if q == 2:
        return True
    if q < 2 or q & 1 == 0: return False
    d = (q - 1) >> 1
    while d&1 == 0: d >>= 1
    for i in xrange(k):
        a, t = random.randint(1, q - 1), d
        y = pow(a,t,q)
        while t != q-1 and y != 1 and y != q-1: 
            y = pow(y, 2, q)
            t <<= 1
        if y != q-1 and t&1 == 0: return False
    return True
def generateprime(bit):
    min = 1 << (bit - 1)
    max = (min << 1) - 1
    x = random.randint(min, max)
    while True:
        if isprime(x): break
        x = x + 1 if x + 1 <= max else min
    return x

max = 1 << 192
def generatekey(bit):
    min = 1 << (bit - 1)
    max = (min << 1) - 1
    while True:
        t = random.randint(3, bit-3)
        p, q = generateprime(t), generateprime(bit - t)
        n = p * q
        if min < n < max: break
    L = lcm(p - 1, q - 1)
    e = random.randint(5, L - 1) | 1
    while True:
        e = e + 2 if e + 2 <= L - 1 else 5
        if gcd(e, L) == 1: break
    d = gcd2(e, L)[0]
    if d < 0: d += L
    return (e, d, n)

def divmod_1(value, modulo):
    return value % modulo + 1, value / modulo

def integer_to_datetime(value):
    value, microsecond = divmod(value, 1000000)
    value, second = divmod(value, 60)
    value, minute = divmod(value, 60)
    value, hour = divmod(value, 24)
    return datetime.datetime.combine(datetime.datetime.fromordinal(value),
                                     datetime.time(hour, minute, second))

def datetime_to_integer(value):
    return (((value.toordinal() \
               * 24 + value.hour) * 60 + value.minute) * 60 + value.second) \
               * 1000000 + value.microsecond