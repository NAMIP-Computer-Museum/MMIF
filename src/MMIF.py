from typing import List, Tuple
from Encoding import Instruction
import re

class Drum:
    N_SECTORS = 20
    N_TRACKS  = 100

    def __init__(self):
        content = [[0 for _ in range(Drum.N_SECTORS)] for _ in range(Drum.N_TRACKS)]    # TODO Words

    def read(self, sector: int, track: int) -> int:
        if sector < 0 or sector > 99 or sector % 5 != 0:
            raise ValueError(f"Bad sector {sector}")
        if track < 0 or track > 99:
            raise ValueError(f"Bad track {sector}")
        return self.content[sector//5][track]

    def write(self, sector: int, track: int, w: int):  #
        if sector < 0 or sector > 99 or sector % 5 != 0:
            raise ValueError(f"Bad sector {sector}")
        if track < 0 or track > 99:
            raise ValueError(f"Bad track {sector}")
        self.content[sector//5][track] = w


class Machine:

    def __init__(self):
        self.program = Drum("Program")
        self.data    = Drum("Data")

    @classmethod
    def parse(cls, text: str) -> List[Tuple[str,str]]:
        # reading lines
        lines = [l.strip() for l in text.strip().split("\n")]
        result = []

        # Vérification séquence du premier nombre
        expected = None

        for idx, line in enumerate(lines):
            parts = line.split()  # Découpage sur espaces multiples

            if len(parts) != 5:
                raise ValueError(f"Ligne {idx + 1}: 5 nombres attendus, obtenu {len(parts)} -> {line}")

            # Vérification de la séquence du premier nombre
            first = int(parts[0])
            if expected is None:
                expected = first  # Premier attendu = premier trouvé
            elif first != expected:
                raise ValueError(f"Ligne {idx + 1}: séquence incorrecte, attendu {expected}, trouvé {first}")

            expected += 5  # Incrément pour la prochaine ligne

            # Vérifie formats (5,4,5,4 chiffres)
            pattern = [5, 4, 5, 4]
            for p, n_digits in zip(parts[1:], pattern):
                if not re.fullmatch(rf"\d{{{n_digits}}}", p):
                    raise ValueError(
                        f"Ligne {idx + 1}: '{p}' n'a pas {n_digits} chiffres"
                    )

            # Extraction des deux paires
            pair1 = (first, parts[1], parts[2])  # AAAAA, BBBB
            pair2 = (first, parts[3], parts[4])  # CCCCC, DDDD

            result.append(pair1)
            result.append(pair2)

        return result

    @classmethod
    def decompile(cls, program: str) -> str:
        instructions = Machine.parse(program)
        for mem, opcode, address in instructions:
            mnemonic = Instruction.opcode_to_mnemonic(opcode)
            print(f"{mem:>5}{opcode:>6}{mnemonic:>8}{address:>5}")
