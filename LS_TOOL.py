# Simple Lewis structure helper for TI-84 Plus CE Python
# Limitations:
# - Neutral molecules only
# - One central atom
# - No resonance, no formal charge calculation
# - Works best for small molecules: CH4, NH3, H2O, CO2, BF3, etc.

VALENCE = {
    "H": 1,
    "C": 4,
    "N": 5,
    "O": 6,
    "F": 7,
    "Cl": 7,
    "Br": 7,
    "I": 7,
    "B": 3,
    "P": 5,
    "S": 6
}

# Rough electronegativity order (low to high) for picking central atom
EN_ORDER = ["B","C","P","S","N","H","O","F","Cl","Br","I"]

def parse_formula(formula):
    atoms = []
    i = 0
    n = len(formula)
    while i < n:
        ch = formula[i]
        if ch.isupper():
            symbol = ch
            i += 1
            if i < n and formula[i].islower():
                symbol += formula[i]
                i += 1
            # read number (if any)
            num_str = ""
            while i < n and formula[i].isdigit():
                num_str += formula[i]
                i += 1
            count = int(num_str) if num_str != "" else 1
            atoms.append((symbol, count))
        else:
            # invalid char, skip
            i += 1
    # expand into list of symbols
    expanded = []
    for sym, cnt in atoms:
        for _ in range(cnt):
            expanded.append(sym)
    return expanded

def total_valence(atoms):
    total = 0
    for a in atoms:
        if a in VALENCE:
            total += VALENCE[a]
        else:
            print("Unknown element:", a)
            return None
    return total

def choose_central(atoms):
    # Not H, and lowest EN_ORDER index
    candidates = [a for a in atoms if a != "H"]
    if not candidates:
        return None
    best = candidates[0]
    best_rank = EN_ORDER.index(best) if best in EN_ORDER else 999
    for a in candidates[1:]:
        r = EN_ORDER.index(a) if a in EN_ORDER else 999
        if r < best_rank:
            best = a
            best_rank = r
    # central index: first occurrence of that symbol
    for i, a in enumerate(atoms):
        if a == best:
            return i
    return 0

def build_initial_structure(atoms, central_idx):
    # Represent structure as:
    # bonds: list of (i, j, order)
    # lone_pairs: list of integers (pairs) per atom
    n = len(atoms)
    bonds = []
    lone_pairs = [0]*n
    # connect each non-central atom to central with single bond
    for i in range(n):
        if i != central_idx:
            bonds.append((central_idx, i, 1))
    return bonds, lone_pairs

def electrons_in_bonds(bonds):
    # each bond order * 2 electrons
    e = 0
    for i, j, order in bonds:
        e += 2*order
    return e

def octet_target(symbol):
    if symbol == "H":
        return 2
    # simple octet rule
    return 8

def current_electrons_on_atom(idx, atoms, bonds, lone_pairs):
    # electrons in bonds around atom + lone pair electrons
    e = 0
    for i, j, order in bonds:
        if i == idx or j == idx:
            e += 2*order
    e += 2*lone_pairs[idx]
    return e

def add_lone_pairs(atoms, bonds, lone_pairs, remaining_e):
    n = len(atoms)
    # First fill terminal atoms (not central) to octet/duet
    # We'll decide central outside this function
    changed = True
    while changed and remaining_e >= 2:
        changed = False
        for i in range(n):
            need = octet_target(atoms[i]) - current_electrons_on_atom(i, atoms, bonds, lone_pairs)
            if need >= 2 and remaining_e >= 2:
                lone_pairs[i] += 1
                remaining_e -= 2
                changed = True
    return remaining_e

def central_index_from_bonds(bonds, n):
    # central is atom with highest degree
    deg = [0]*n
    for i, j, order in bonds:
        deg[i] += order
        deg[j] += order
    best = 0
    for i in range(1, n):
        if deg[i] > deg[best]:
            best = i
    return best

def make_multiple_bonds(atoms, bonds, lone_pairs, total_e):
    n = len(atoms)
    used_e = electrons_in_bonds(bonds) + 2*sum(lone_pairs)
    remaining_e = total_e - used_e
    # put any remaining electrons on central as lone pairs
    c = central_index_from_bonds(bonds, n)
    while remaining_e >= 2:
        lone_pairs[c] += 1
        remaining_e -= 2

    # Now check central octet; if not full, convert lone pairs on terminals to bonds
    central_e = current_electrons_on_atom(c, atoms, bonds, lone_pairs)
    target = octet_target(atoms[c])
    # try to increase bond order with neighbors that have lone pairs
    while central_e < target:
        improved = False
        for idx, (i, j, order) in enumerate(bonds):
            if i == c:
                other = j
            elif j == c:
                other = i
            else:
                continue
            if lone_pairs[other] > 0:
                # convert one lone pair on other into bonding pair
                lone_pairs[other] -= 1
                bonds[idx] = (i, j, order+1)
                central_e = current_electrons_on_atom(c, atoms, bonds, lone_pairs)
                improved = True
                if central_e >= target:
                    break
        if not improved:
            break
    return bonds, lone_pairs

def print_structure(atoms, bonds, lone_pairs):
    n = len(atoms)
    print("Atoms (index: symbol):")
    for i in range(n):
        print(i, ":", atoms[i])
    print()
    print("Bonds (i-j: order):")
    for i, j, order in bonds:
        print(i, "-", j, ":", order)
    print()
    print("Lone pairs per atom:")
    for i in range(n):
        print(i, atoms[i], ":", lone_pairs[i])
    print()
    # crude linear drawing: central in middle, terminals around
    c = central_index_from_bonds(bonds, n)
    print("Approximate structure:")
    # collect neighbors
    neighbors = []
    for i, j, order in bonds:
        if i == c:
            neighbors.append((j, order))
        elif j == c:
            neighbors.append((i, order))
    # print like: X=O, etc.
    line = ""
    for idx, order in neighbors:
        bond_char = "-" if order == 1 else "=" if order == 2 else "≡"
        if line != "":
            line += " "
        line += atoms[idx] + bond_char
    line += atoms[c]
    print(line)
    print("(Lone pairs not shown in this line; see list above.)")

def main():
    print("Lewis Structure Helper")
    formula = input("Formula (e.g. CO2, H2O): ")
    atoms = parse_formula(formula)
    if not atoms:
        print("Could not parse formula.")
        return
    total = total_valence(atoms)
    if total is None:
        return
    print("Total valence electrons:", total)
    c_idx = choose_central(atoms)
    if c_idx is None:
        print("No suitable central atom.")
        return
    print("Central atom index:", c_idx, "symbol:", atoms[c_idx])
    bonds, lone_pairs = build_initial_structure(atoms, c_idx)
    used = electrons_in_bonds(bonds)
    remaining = total - used
    if remaining < 0:
        print("Not enough electrons for even single bonds.")
        return
    remaining = add_lone_pairs(atoms, bonds, lone_pairs, remaining)
    bonds, lone_pairs = make_multiple_bonds(atoms, bonds, lone_pairs, total)
    print_structure(atoms, bonds, lone_pairs)

# Run once
main()