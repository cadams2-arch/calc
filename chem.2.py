# ---- CHAPTER 3 ----

def wl(f):
    return 3e8 / f

def fr(w):
    return 3e8 / w

def e_f(f):
    return 6.626e-34 * f

def e_w(w):
    return 6.626e-34 * 3e8 / w

def bohr(n):
    return -2.18e-18 / (n * n)

def bohr_t(n1, n2):
    return bohr(n2) - bohr(n1)

def orb(s):
    if s == 's': return 1
    if s == 'p': return 3
    if s == 'd': return 5
    if s == 'f': return 7
    return None

# ---- CHAPTER 6 ----
# atomic masses
H = 1.008
C = 12.01
O = 16.00
N = 14.01
S = 32.06
Cl = 35.45
Na = 22.99
Mg = 24.31

def mm(element_mass, count):
    return element_mass * count

def pct(part, total):
    return (part / total) * 100

def emp(m1, a1, m2, a2):
    r1 = m1 / a1
    r2 = m2 / a2
    s = min(r1, r2)
    return round(r1 / s), round(r2 / s)

def mol_form(e1, e2, molar_mass_actual, molar_mass_emp):
    k = round(molar_mass_actual / molar_mass_emp)
    return e1 * k, e2 * k

# ---- CHAPTER 9 ----

def mr(nA, cA, cB):
    return nA * (cB / cA)

def m2m(mA, mmA, cA, cB, mmB):
    return (mA / mmA) * (cB / cA) * mmB

def lr(mA, mmA, cA, mB, mmB, cB):
    nA = mA / mmA
    nB = mB / mmB
    if nA * (cB / cA) < nB:
        return "A"
    return "B"

def ty(nL, cL, cP, mmP):
    return nL * (cP / cL) * mmP

def py(actual, theoretical):
    return (actual / theoretical) * 100

def M(n, L):
    return n / L

def ionM(Mc, count):
    return Mc * count