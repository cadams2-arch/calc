# CH6 Bonding Study Tool
# TI-84 Plus CE Python

def pause():
    input("\nPress ENTER...")

def ionic():
    print("\n--- IONIC BONDING ---")
    print("Metal loses e- → cation (+)")
    print("Nonmetal gains e- → anion (-)")
    print("Ions form 3D lattice, not molecules")
    print("Strength ∝ (Q+)(Q-) / d^2")
    print("Higher charge = stronger bond")
    print("Smaller ions = stronger bond")
    pause()

def covalent():
    print("\n--- COVALENT BONDING ---")
    print("Nonmetal + nonmetal")
    print("Share electrons to reach octet")
    print("Single = 1 pair")
    print("Double = 2 pairs")
    print("Triple = 3 pairs")
    print("H follows duet rule")
    pause()

def lewis():
    print("\n--- LEWIS STRUCTURE STEPS ---")
    print("1) Count valence electrons")
    print("2) Choose central atom (least EN, never H)")
    print("3) Single bonds to outer atoms")
    print("4) Complete octets on outer atoms")
    print("5) Put leftover e- on central atom")
    print("6) If central lacks octet → double/triple bonds")
    print("7) Check total e- count")
    pause()

def polyatomic():
    print("\n--- POLYATOMIC IONS ---")
    print("Add e- for negative charge")
    print("Subtract e- for positive charge")
    print("Put structure in brackets w/ charge")
    print("Common patterns:")
    print("O: 2 bonds, 2 lone pairs")
    print("N: 3 bonds, 1 lone pair")
    print("Halogens: 1 bond, 3 lone pairs")
    pause()

def examples():
    print("\n--- QUICK EXAMPLES ---")
    print("CHCl3:")
    print("C center, all single bonds")
    print("Cl has 3 lone pairs")
    print("\nCH2O (formaldehyde):")
    print("C center, double bond to O")
    print("O has 2 lone pairs")
    print("\nClO2-:")
    print("Cl center, 2 single-bonded O")
    print("Add 1 e- for charge")
    print("Cl has 2 lone pairs")
    pause()

def bondcount():
    print("\n--- BOND COUNT FORMULA ---")
    print("Total bonds needed =")
    print("(8*non-H atoms + 2*H atoms - valence e-) / 2")
    pause()

def main():
    while True:
        print("\n=== CH6 BONDING REVIEW ===")
        print("1) Ionic Bonding")
        print("2) Covalent Bonding")
        print("3) Lewis Structures")
        print("4) Polyatomic Ions")
        print("5) Examples")
        print("6) Bond Count Shortcut")
        print("7) Quit")

        choice = input("Select: ")

        if choice == "1":
            ionic()
        elif choice == "2":
            covalent()
        elif choice == "3":
            lewis()
        elif choice == "4":
            polyatomic()
        elif choice == "5":
            examples()
        elif choice == "6":
            bondcount()
        elif choice == "7":
            print("Good luck on your quiz!")
            break
        else:
            print("Invalid choice.")

main()