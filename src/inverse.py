import math

import math

def sgn(x: float) -> int:
    """Sign of x as -1, 0, or +1."""
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def mexp(x: float) -> float:
    """Unbiased base-10 exponent for decimal mantissa in [0.1, 1)."""
    if x == 0:
        return 0
    print(math.log10(x))
    pq = math.floor(math.log10(abs(x)))+1
    print(f"exp {pq}")
    return 0.1*10**(-pq)  # floor(log10(|x|))

def exp(x: float) -> float:
    """Unbiased base-10 exponent for decimal mantissa in [0.1, 1)."""
    if x == 0:
        return 0
    pq = math.floor(math.log10(abs(x)))+1
#    print(f"exp {pq}")
    return 0.1*10**(pq)  # floor(log10(|x|))

def man(x: float) -> float:
    """Decimal mantissa in [0.1, 1)."""
    if x == 0:
        return 0.0
    e = exp(x)
    return abs(x) / e / 10


a0 = -0.49689441  * 10
b0 = +0.546583851 * 10
a1 = +0.216457031 * 10
a2 = +0.2016019   * 10
a3 = +0.200013038 * 10

x = 0.9

print(sgn(x))
print(f"man={man(x)}")
print(f"exp={exp(x)}")
print(f"mexp={mexp(x)}")

y0 = sgn(x)*(mexp(x))*(a0*man(x)+b0)*10
y1 = y0 * (a1-x*y0)
y2 = y1 * (a2-x*y1)
y3 = y2 * (a3-x*y2)
y4 = y3 * (2.0-x*y3)
y5 = y4 * (2.0-x*y4)

print(f"   x={x}")
print(f"  y1={y1}")
print(f"  y2={y2}")
print(f"  y3={y3}")
print(f"  y4={y4}")
print(f"  y5={y5}")
print(f" 1/x={1/x}")

