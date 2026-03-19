# ============================================================
# CHEMISTRY TOOLKIT — FULLY INTERACTIVE VERSION
# ============================================================

# -----------------------------
# CHAPTER 3 — LIGHT & ATOMS
# -----------------------------

def wavelength_from_frequency(frequency_hz):
    c = 3.00e8
    return c / frequency_hz

def frequency_from_wavelength(wavelength_m):
    c = 3.00e8
    return c / wavelength_m

def energy_from_frequency(frequency_hz):
    h = 6.626e-34
    return h * frequency_hz

def energy_from_wavelength(wavelength_m):
    h = 6.626e-34
    c = 3.00e8
    return (h * c) / wavelength_m

def bohr_energy(n):
    return -2.18e-18 / (n**2)

def bohr_transition_energy(n_initial, n_final):
    Ei = bohr_energy(n_initial)
    Ef = bohr_energy(n_final)
    return Ef - Ei

def orbitals_in_subshell(subshell):
    if subshell == 's':
        return 1
    if subshell == 'p':
        return 3
    if subshell == 'd':
        return 5
    if subshell == 'f':
        return 7
    return None

def electron_configuration(Z):
    subshells = [
        ("1s", 2), ("2s", 2), ("2p", 6),
        ("3s", 2), ("3p", 6), ("4s", 2),
        ("3d", 10)
    ]
    remaining = Z
    config = ""

    for name, capacity in subshells:
        if remaining <= 0:
            break
        electrons = min(remaining, capacity)
        config += name + "^" + str(electrons) + " "
        remaining -= electrons

    return config.strip()


# -----------------------------
# CHAPTER 6 — MOLES & FORMULAS
# -----------------------------

atomic_masses = {
    "H": 1.008, "C": 12.01, "O": 16.00, "N": 14.01,
    "S": 32.06, "Cl": 35.45, "Na": 22.99, "Mg": 24.31
}

def molar_mass(formula_dict):
    total = 0
    for element, count in formula_dict.items():
        total += atomic_masses[element] * count
    return total

def percent_composition(formula_dict):
    mm = molar_mass(formula_dict)
    percentages = {}
    for element, count in formula_dict.items():
        percentages[element] = (atomic_masses[element] * count / mm) * 100
    return percentages

def empirical_formula(mass_dict):
    moles = {el: mass / atomic_masses[el] for el, mass in mass_dict.items()}
    smallest = min(moles.values())
    ratio = {el: round(m / smallest) for el, m in moles.items()}
    return ratio

def molecular_formula(empirical_dict, molar_mass_actual):
    mm_emp = molar_mass(empirical_dict)
    multiplier = round(molar_mass_actual / mm_emp)
    return {el: count * multiplier for el, count in empirical_dict.items()}


# -----------------------------
# CHAPTER 9 — STOICHIOMETRY
# -----------------------------

def mole_ratio(moles_A, coeff_A, coeff_B):
    return moles_A * (coeff_B / coeff_A)

def mass_to_mass(mass_A, mm_A, coeff_A, coeff_B, mm_B):
    moles_A = mass_A / mm_A
    moles_B = mole_ratio(moles_A, coeff_A, coeff_B)
    return moles_B * mm_B

def limiting_reactant(mass_A, mm_A, coeff_A, mass_B, mm_B, coeff_B):
    moles_A = mass_A / mm_A
    moles_B = mass_B / mm_B
    possible_B_from_A = mole_ratio(moles_A, coeff_A, coeff_B)

    if possible_B_from_A < moles_B:
        return "A is limiting"
    else:
        return "B is limiting"

def theoretical_yield(moles_limiting, coeff_limiting, coeff_product, mm_product):
    moles_product = mole_ratio(moles_limiting, coeff_limiting, coeff_product)
    return moles_product * mm_product

def percent_yield(actual_mass, theoretical_mass):
    return (actual_mass / theoretical_mass) * 100

def molarity(moles_solute, liters_solution):
    return moles_solute / liters_solution

def ion_molarity(compound_molarity, ion_dict):
    return {ion: compound_molarity * count for ion, count in ion_dict.items()}


# ============================================================
# INTERACTIVE SUBMENUS
# ============================================================

def chapter_3_menu():
    while True:
        print("\n--- Chapter 3 Functions ---")
        print("1. Wavelength from Frequency")
        print("2. Frequency from Wavelength")
        print("3. Energy from Frequency")
        print("4. Energy from Wavelength")
        print("5. Bohr Energy Level")
        print("6. Bohr Transition Energy")
        print("7. Orbitals in Subshell")
        print("8. Electron Configuration")
        print("9. Back")

        choice = input("Select an option: ")

        if choice == "1":
            f = float(input("Enter frequency (Hz): "))
            print("Wavelength (m):", wavelength_from_frequency(f))

        elif choice == "2":
            w = float(input("Enter wavelength (m): "))
            print("Frequency (Hz):", frequency_from_wavelength(w))

        elif choice == "3":
            f = float(input("Enter frequency (Hz): "))
            print("Energy (J):", energy_from_frequency(f))

        elif choice == "4":
            w = float(input("Enter wavelength (m): "))
            print("Energy (J):", energy_from_wavelength(w))

        elif choice == "5":
            n = int(input("Enter energy level n: "))
            print("Energy (J):", bohr_energy(n))

        elif choice == "6":
            n1 = int(input("Initial level n₁: "))
            n2 = int(input("Final level n₂: "))
            print("Transition energy (J):", bohr_transition_energy(n1, n2))

        elif choice == "7":
            s = input("Enter subshell (s, p, d, f): ")
            print("Orbitals:", orbitals_in_subshell(s))

        elif choice == "8":
            Z = int(input("Enter atomic number Z: "))
            print("Electron configuration:", electron_configuration(Z))

        elif choice == "9":
            break


def chapter_6_menu():
    while True:
        print("\n--- Chapter 6 Functions ---")
        print("1. Molar Mass")
        print("2. Percent Composition")
        print("3. Empirical Formula")
        print("4. Molecular Formula")
        print("5. Back")

        choice = input("Select an option: ")

        if choice == "1":
            print("Enter elements and counts (e.g., C 6, H 12, O 6).")
            formula = {}
            while True:
                el = input("Element (or blank to finish): ")
                if el == "":
                    break
                count = int(input("Count: "))
                formula[el] = count
            print("Molar mass:", molar_mass(formula))

        elif choice == "2":
            print("Enter elements and counts.")
            formula = {}
            while True:
                el = input("Element (or blank to finish): ")
                if el == "":
                    break
                count = int(input("Count: "))
                formula[el] = count
            print("Percent composition:", percent_composition(formula))

        elif choice == "3":
            print("Enter masses of each element.")
            masses = {}
            while True:
                el = input("Element (or blank to finish): ")
                if el == "":
                    break
                mass = float(input("Mass (g): "))
                masses[el] = mass
            print("Empirical formula:", empirical_formula(masses))

        elif choice == "4":
            print("Enter empirical formula.")
            emp = {}
            while True:
                el = input("Element (or blank to finish): ")
                if el == "":
                    break
                count = int(input("Count: "))
                emp[el] = count
            mm = float(input("Enter actual molar mass: "))
            print("Molecular formula:", molecular_formula(emp, mm))

        elif choice == "5":
            break


def chapter_9_menu():
    while True:
        print("\n--- Chapter 9 Functions ---")
        print("1. Mole Ratio")
        print("2. Mass-to-Mass")
        print("3. Limiting Reactant")
        print("4. Theoretical Yield")
        print("5. Percent Yield")
        print("6. Molarity")
        print("7. Ion Molarity")
        print("8. Back")

        choice = input("Select an option: ")

        if choice == "1":
            mA = float(input("Moles of A: "))
            cA = float(input("Coefficient of A: "))
            cB = float(input("Coefficient of B: "))
            print("Moles of B:", mole_ratio(mA, cA, cB))

        elif choice == "2":
            massA = float(input("Mass of A (g): "))
            mmA = float(input("Molar mass of A: "))
            cA = float(input("Coefficient of A: "))
            cB = float(input("Coefficient of B: "))
            mmB = float(input("Molar mass of B: "))
            print("Mass of B (g):", mass_to_mass(massA, mmA, cA, cB, mmB))

        elif choice == "3":
            massA = float(input("Mass A (g): "))
            mmA = float(input("Molar mass A: "))
            cA = float(input("Coeff A: "))
            massB = float(input("Mass B (g): "))
            mmB = float(input("Molar mass B: "))
            cB = float(input("Coeff B: "))
            print("Limiting reactant:", limiting_reactant(massA, mmA, cA, massB, mmB, cB))

        elif choice == "4":
            mol_lim = float(input("Moles of limiting reactant: "))
            c_lim = float(input("Coeff of limiting reactant: "))
            c_prod = float(input("Coeff of product: "))
            mm_prod = float(input("Molar mass of product: "))
            print("Theoretical yield (g):", theoretical_yield(mol_lim, c_lim, c_prod, mm_prod))

        elif choice == "5":
            actual = float(input("Actual yield (g): "))
            theo = float(input("Theoretical yield (g): "))
            print("Percent yield:", percent_yield(actual, theo))

        elif choice == "6":
            mol = float(input("Moles solute: "))
            L = float(input("Liters solution: "))
            print("Molarity:", molarity(mol, L))

        elif choice == "7":
            M = float(input("Compound molarity: "))
            ions = {}
            while True:
                ion = input("Ion (or blank to finish): ")
                if ion == "":
                    break
                count = int(input("Count: "))
                ions[ion] = count
            print("Ion molarities:", ion_molarity(M, ions))

        elif choice == "8":
            break


# ============================================================
# MAIN LOOP
# ============================================================

def show_menu():
    print("====================================")
    print("      CHEMISTRY TOOLKIT MENU")
    print("====================================")
    print("1. Chapter 3 — Light & Atoms")
    print("2. Chapter 6 — Moles & Formulas")
    print("3. Chapter 9 — Stoichiometry")
    print("4. Exit")
    print("====================================")

def main():
    while True:
        show_menu()
        choice = input("Select an option: ")

        if choice == "1":
            chapter_3_menu()
        elif choice == "2":
            chapter_6_menu()
        elif choice == "3":
            chapter_9_menu()
        elif choice == "4":
            print("Exiting program.")
            break
        else:
            print("Invalid choice.")

main()