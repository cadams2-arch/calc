# Lewis Structure Helper with Charges and ASCII Drawing
# TI-84 Plus CE Python compatible
# Limitations:
# - Best for small molecules with one central atom
# - Simple resonance handling (structure is one reasonable pattern)
# - Expanded octet only partially handled (S, P, etc. may not be perfect)

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

def parse_charge(formula):
    # Returns (core_formula, net_charge)
    # Supports: NH4+, NO3-, SO4^2-, CO3--, PO4^3-, etc.
    f = formula.strip()
    if f == "":
        return f, 0
    net = 0
    # Look from end for + or -
    i = len(f) - 1
    sign = 0
    count = 0
    while i >= 0 and (f[i] == '+' or f[i] == '-'):
        if f[i] == '+':
            sign += 1
        else:
            sign -= 1
        i -= 1
    if sign != 0:
        net = sign
        core = f[:i+1]
        return core, net
    # Look for ^n+ or ^n-
    if '^' in f:
        pos = f.rfind('^')
        core = f[:pos]
        rest = f[pos+1:]
        num = ""
        sgn = 0
        for ch in rest:
            if ch.isdigit():
                num += ch
            elif ch == '+':
                sgn = 1
            elif ch == '-':
                sgn = -1
        if num == "":
            mag = 1
        else:
            mag = int(num)
        net = mag * sgn
        return core, net
    return f, 0

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
            num_str = ""
            while i < n and formula[i].isdigit():
                num_str += formula[i]
                i += 1
            count = int(num_str) if num_str != "" else 1
            atoms.append((symbol, count))
        else:
            i += 1
    expanded = []
    for sym, cnt in atoms:
        for _ in range(cnt):
            expanded.append(sym)
    return expanded

def total_valence(atoms, net_charge):
    total = 0
    for a in atoms:
        if a in VALENCE:
            total += VALENCE[a]
        else:
            print("Unknown element:", a)
            return None
    # Negative charge adds electrons, positive removes
    total -= net_charge
    return total

def choose_central(atoms):
    candidates = [a for a in atoms if a != "H"]
    if not candidates:
        return 0
    best = candidates[0]
    best_rank = EN_ORDER.index(best) if best in EN_ORDER else 999
    for a in candidates[1:]:
        r = EN_ORDER.index(a) if a in EN_ORDER else 999
        if r < best_rank:
            best = a
            best_rank = r
    for i, a in enumerate(atoms):
        if a == best:
            return i
    return 0

def build_initial_structure(atoms, central_idx):
    n = len(atoms)
    bonds = []
    lone_pairs = [0]*n
    for i in range(n):
        if i != central_idx:
            bonds.append((central_idx, i, 1))
    return bonds, lone_pairs

def electrons_in_bonds(bonds):
    e = 0
    for i, j, order in bonds:
        e += 2*order
    return e

def octet_target(symbol):
    if symbol == "H":
        return 2
    return 8

def current_electrons_on_atom(idx, atoms, bonds, lone_pairs):
    e = 0
    for i, j, order in bonds:
        if i == idx or j == idx:
            e += 2*order
    e += 2*lone_pairs[idx]
    return e

def add_lone_pairs(atoms, bonds, lone_pairs, remaining_e, central_idx):
    n = len(atoms)
    changed = True
    while changed and remaining_e >= 2:
        changed = False
        for i in range(n):
            if i == central_idx:
                continue
            need = octet_target(atoms[i]) - current_electrons_on_atom(i, atoms, bonds, lone_pairs)
            if need >= 2 and remaining_e >= 2:
                lone_pairs[i] += 1
                remaining_e -= 2
                changed = True
    return remaining_e

def central_index_from_bonds(bonds, n):
    deg = [0]*n
    for i, j, order in bonds:
        deg[i] += order
        deg[j] += order
    best = 0
    for i in range(1, n):
        if deg[i] > deg[best]:
            best = i
    return best

def make_multiple_bonds(atoms, bonds, lone_pairs, total_e, central_idx):
    n = len(atoms)
    used_e = electrons_in_bonds(bonds) + 2*sum(lone_pairs)
    remaining_e = total_e - used_e
    # Put remaining electrons on central as lone pairs (allow expanded octet)
    while remaining_e >= 2:
        lone_pairs[central_idx] += 1
        remaining_e -= 2
    # Try to satisfy central octet by converting lone pairs on terminals to bonds
    target = octet_target(atoms[central_idx])
    central_e = current_electrons_on_atom(central_idx, atoms, bonds, lone_pairs)
    while central_e < target:
        improved = False
        for idx, (i, j, order) in enumerate(bonds):
            if i == central_idx:
                other = j
            elif j == central_idx:
                other = i
            else:
                continue
            if atoms[other] == "H":
                continue
            if lone_pairs[other] > 0:
                lone_pairs[other] -= 1
                bonds[idx] = (i, j, order+1)
                central_e = current_electrons_on_atom(central_idx, atoms, bonds, lone_pairs)
                improved = True
                if central_e >= target:
                    break
        if not improved:
            break
    return bonds, lone_pairs

def count_bonds_for_atom(idx, bonds):
    c = 0
    for i, j, order in bonds:
        if i == idx or j == idx:
            c += order
    return c

def formal_charge(idx, atoms, bonds, lone_pairs):
    sym = atoms[idx]
    if sym not in VALENCE:
        return 0
    val = VALENCE[sym]
    bonding_e = 0
    for i, j, order in bonds:
        if i == idx or j == idx:
            bonding_e += 2*order
    lone_e = 2*lone_pairs[idx]
    fc = val - (lone_e + bonding_e//2)
    return fc

def bond_char(order):
    if order == 1:
        return "-"
    elif order == 2:
        return "="
    else:
        return "≡"

def neighbors_of(central_idx, bonds):
    neigh = []
    for i, j, order in bonds:
        if i == central_idx:
            neigh.append((j, order))
        elif j == central_idx:
            neigh.append((i, order))
    return neigh

def atom_label(sym, charge):
    if charge == 0:
        return sym
    elif charge == 1:
        return sym + "+"
    elif charge == -1:
        return sym + "-"
    elif charge > 1:
        return sym + "^" + str(charge) + "+"
    else:
        return sym + "^" + str(-charge) + "-"

def draw_ascii(atoms, bonds, lone_pairs, net_charge, central_idx):
    n = len(atoms)
    neigh = neighbors_of(central_idx, bonds)
    # Compute formal charges
    fcs = [formal_charge(i, atoms, bonds, lone_pairs) for i in range(n)]
    # Label central
    c_label = atom_label(atoms[central_idx], fcs[central_idx])
    # Assign up to 4 neighbors: up, left, right, down
    up = None
    left = None
    right = None
    down = None
    extra = []
    if len(neigh) >= 1:
        up = neigh[0]
    if len(neigh) >= 2:
        left = neigh[1]
    if len(neigh) >= 3:
        right = neigh[2]
    if len(neigh) >= 4:
        down = neigh[3]
    if len(neigh) > 4:
        extra = neigh[4:]

    # Build lines: top, middle, bottom, plus extras
    top = ""
    mid = ""
    bot = ""

    # Top neighbor
    if up is not None:
        idx, order = up
        sym = atom_label(atoms[idx], fcs[idx])
        # Lone pairs around top atom
        lp = lone_pairs[idx]
        top_lp = ""
        if lp > 0:
            top_lp = ".."
        top = "  " + top_lp + sym + top_lp
        # bond between up and central
        bch = bond_char(order)
        mid = "   " + bch
    else:
        top = ""
        mid = ""

    # Middle line: left - central - right
    left_str = ""
    right_str = ""
    if left is not None:
        idx, order = left
        sym = atom_label(atoms[idx], fcs[idx])
        lp = lone_pairs[idx]
        lp_left = ".." if lp > 0 else ""
        left_str = lp_left + sym + lp_left + bond_char(order)
    if right is not None:
        idx, order = right
        sym = atom_label(atoms[idx], fcs[idx])
        lp = lone_pairs[idx]
        lp_right = ".." if lp > 0 else ""
        right_str = bond_char(order) + lp_right + sym + lp_right

    # Lone pairs on central: show above and below as needed
    c_lp = lone_pairs[central_idx]
    c_lp_top = ".." if c_lp > 0 else ""
    c_lp_bot = ".." if c_lp > 1 else ""

    center_part = c_label
    middle_line = ""
    if left_str != "" or right_str != "":
        middle_line = left_str + center_part + right_str
    else:
        middle_line = center_part

    # Combine top bond and central lone pairs
    if up is not None:
        print(top)
        print(mid + center_part)
    else:
        if c_lp_top != "":
            print("   " + c_lp_top)
        print(middle_line)

    # Down neighbor
    if down is not None:
        idx, order = down
        sym = atom_label(atoms[idx], fcs[idx])
        lp = lone_pairs[idx]
        down_lp = ".." if lp > 0 else ""
        bch = bond_char(order)
        print("   " + bch)
        print("  " + down_lp + sym + down_lp)
    else:
        if c_lp_bot != "":
            print("   " + c_lp_bot)

    # Extra neighbors (if any) printed in a row
    if len(extra) > 0:
        line = ""
        for idx, order in extra:
            sym = atom_label(atoms[idx], fcs[idx])
            lp = lone_pairs[idx]
            lp_s = ".." if lp > 0 else ""
            if line != "":
                line += "  "
            line += lp_s + sym + lp_s + "(" + bond_char(order) + ")"
        print(line)

    # Overall charge
    if net_charge != 0:
        if net_charge > 0:
            ch = "+" + (str(net_charge) if net_charge != 1 else "")
        else:
            ch = "-" + (str(-net_charge) if net_charge != -1 else "")
        print("Overall charge:", ch)
    else:
        print("Overall charge: 0")

    print()

    # Per-atom summary
    print("Atom  Bonds  LonePairs  Dots  FormalCharge")
    for i in range(n):
        b = count_bonds_for_atom(i, bonds)
        lp = lone_pairs[i]
        dots = 2*lp
        fc = fcs[i]
        lab = atom_label(atoms[i], fc)
        print(i, lab, " ", b, "      ", lp, "        ", dots, "    ", fc)

def main():
    print("Lewis Structure Helper (with charges)")
    formula = input("Formula (e.g. CO2, H2O, NO3-): ")
    core, net_charge = parse_charge(formula)
    atoms = parse_formula(core)
    if not atoms:
        print("Could not parse formula.")
        return
    total = total_valence(atoms, net_charge)
    if total is None:
        return
    print("Total valence electrons (adjusted for charge):", total)
    c_idx = choose_central(atoms)
    print("Central atom index:", c_idx, "symbol:", atoms[c_idx])
    bonds, lone_pairs = build_initial_structure(atoms, c_idx)
    used = electrons_in_bonds(bonds)
    remaining = total - used
    if remaining < 0:
        print("Not enough electrons for even single bonds.")
        return
    remaining = add_lone_pairs(atoms, bonds, lone_pairs, remaining, c_idx)
    bonds, lone_pairs = make_multiple_bonds(atoms, bonds, lone_pairs, total, c_idx)
    print()
    print("Bonds (i-j: order):")
    for i, j, order in bonds:
        print(i, "-", j, ":", order)
    print()
    print("Lone pairs per atom:")
    for i in range(len(atoms)):
        print(i, atoms[i], ":", lone_pairs[i])
    print()
    print("ASCII Lewis structure:")
    draw_ascii(atoms, bonds, lone_pairs, net_charge, c_idx)

main()