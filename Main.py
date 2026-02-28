import base64
import textwrap
import sys

# =============================================================================
# PRIME DNA TABLE
# Each character is mapped to a unique prime number.
# =============================================================================

TABELA_DNA = {
    "A": 2,   "B": 3,   "C": 5,   "D": 7,   "E": 11,  "F": 13,  "G": 17,  "H": 19,
    "I": 23,  "J": 29,  "K": 31,  "L": 37,  "M": 41,  "N": 43,  "O": 47,  "P": 53,
    "Q": 59,  "R": 61,  "S": 67,  "T": 71,  "U": 73,  "V": 79,  "W": 83,  "X": 89,
    "Y": 97,  "Z": 101,
    "a": 103, "b": 107, "c": 109, "d": 113, "e": 127, "f": 131,
    "g": 137, "h": 139, "i": 149, "j": 151, "k": 157, "l": 163,
    "m": 167, "n": 173, "o": 179, "p": 181, "q": 191, "r": 193,
    "s": 197, "t": 199, "u": 211, "v": 223, "w": 227, "x": 229,
    "y": 233, "z": 239,
    "0": 241, "1": 251, "2": 257, "3": 263, "4": 269,
    "5": 271, "6": 277, "7": 281, "8": 283, "9": 293,
    " ": 397
}

REVERSO_DNA = {v: k for k, v in TABELA_DNA.items()}

# =============================================================================
# PRIME POSITION GENERATOR
# =============================================================================

def proximo_primo(n):
    n += 1
    while True:
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                break
        else:
            return n
        n += 1

# =============================================================================
# ENCODING
# M = ∏ (DNA_char ^ prime_position)
# =============================================================================

def codificar(texto):
    massa = 1
    pos_primo = 2  # First positional prime

    for char in texto:
        if char not in TABELA_DNA:
            raise ValueError(f"Unsupported character: {char}")

        dna = TABELA_DNA[char]
        massa *= pow(dna, pos_primo)
        pos_primo = proximo_primo(pos_primo)

    # Convert big integer to bytes
    b = massa.to_bytes((massa.bit_length() + 7) // 8, "big")
    encoded = base64.b64encode(b).decode()

    return textwrap.fill(encoded, width=64)

# =============================================================================
# DECODING (Factorization-based reconstruction)
# =============================================================================

def decodificar(chave):
    limpa = chave.replace("\n", "").strip()
    massa = int.from_bytes(base64.b64decode(limpa), "big")

    resultado = ""
    pos_primo = 2

    while massa > 1:
        exp = 0
        while massa % pos_primo == 0:
            massa //= pos_primo
            exp += 1

        if exp > 0:
            if exp in REVERSO_DNA:
                resultado += REVERSO_DNA[exp]
            else:
                resultado += "?"
        else:
            break

        pos_primo = proximo_primo(pos_primo)

    return resultado

# =============================================================================
# CLI INTERFACE
# =============================================================================

def menu():
    print("\n" + "=" * 40)
    print(" PRIME DNA ENCODING SYSTEM ")
    print("=" * 40)
    print("[1] Encode")
    print("[2] Decode")
    print("[0] Exit")

def main():
    while True:
        menu()
        op = input(">>> ")

        if op == "1":
            texto = input("Enter text: ")
            try:
                chave = codificar(texto)
                print("\nEncoded Key:\n")
                print(chave)
            except Exception as e:
                print("Error:", e)

        elif op == "2":
            print("\nPaste encoded key (end with empty line):")
            linhas = []
            while True:
                linha = input()
                if linha.strip() == "":
                    break
                linhas.append(linha)

            chave = "".join(linhas)
            try:
                texto = decodificar(chave)
                print("\nDecoded Text:", texto)
            except Exception as e:
                print("Error:", e)

        elif op == "0":
            sys.exit()

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
