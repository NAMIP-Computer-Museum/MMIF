import math
from typing import List, Tuple
from Encoding import Word, Instruction, Float, Tetrad
from random import randint
import re

class Drum:
    N_SECTORS = 20
    N_TRACKS  = 100

    def __init__(self, name):
        self.name = name
        self.content = [[Word() for _ in range(Drum.N_SECTORS)] for _ in range(Drum.N_TRACKS)]    # TODO Words

    def read(self, mem: int) -> Word:
        return self._read(Drum.track(mem), Drum.sector(mem))

    def _read(self, track: int, sector: int) -> Word:
        if sector < 0 or sector > 99 or sector % 5 != 0:
            raise ValueError(f"Bad sector {sector}")
        if track < 0 or track > 99:
            raise ValueError(f"Bad track {sector}")
        return self.content[track][sector//5]

    def write(self, mem: int, w: Word):
        self._write(Drum.track(mem), Drum.sector(mem), w)

    def _write(self, track: int, sector: int, w: Word):
#        print(f"write {sector} {track}")
        if sector < 0 or sector > 99 or sector % 5 != 0:
            raise ValueError(f"Bad sector {sector}")
        if track < 0 or track > 99:
            raise ValueError(f"Bad track {sector}")
        self.content[track][sector//5] = w

    @staticmethod
    def sector(mem: int) -> int:
        return mem % 100

    @staticmethod
    def track(mem: int) -> int:
        return mem // 100

    def store(self, instructions: List[Tuple[int, str, str]]):
        if len(instructions)%2 == 1:
            raise ValueError("Instruction list should be even !")
        for i in range(0, len(instructions) - 1, 2):
            mem1, opcode1, address1 = instructions[i]
            mem2, opcode2, address2 = instructions[i+1]
            if mem1 != mem2:
                raise ValueError(f"Bad address pair {mem1} {mem2}")
            instr = Instruction()
            instr.set_instruction(0, opcode1, address1)
            instr.set_instruction(1, opcode2, address2)
            self.write(mem1, instr)

    def dump(self, mem: int, num: int):
        print(f"ICI {mem} {num}")
        for addr in range(mem, mem+num,5):
            inst = self.read(addr)
            oc1 = inst.get_opcode(0)
            oc2 = inst.get_opcode(1)
            ad1 = inst.get_address(0)
            ad2 = inst.get_address(1)
            print(f"{addr} {oc1} {ad1}")
            print(f"{addr} {oc2} {ad2}")

class Machine:

    @staticmethod
    def _init_regs():
        regs = {}
        regs["w"] = Float()
        regs["E"] = Float()
        regs["F"] = Float()
        regs["G"] = 0
        regs["H"] = 0
        regs["I"] = 0
        regs["J"] = 0
        # TODO more regs
        return regs

    def __init__(self):
        self.drum_p = Drum("Program")
        self.drum_d = Drum("Data")
        self.pc = 0
        self.pi = 0
        self.ch = False
        self.alt= None
        self.running = False
        self.alarm = False
        self.REGS = Machine._init_regs()

    def get_f_reg(self, reg: str) -> Float:
        if reg not in ("w", "E", "F"):
            raise ValueError(f"Not a float register: {reg}")
        return self.REGS[reg]

    def get_i_reg(self, reg: str) -> int:
        if reg not in ("G", "H", "I", "J"):
            raise ValueError(f"Not an index register: {reg}")
        return self.REGS[reg]

    def set_f_reg(self, reg:str, val:Float):
        if reg not in ("w", "E", "F"):
            raise ValueError(f"Not a float register: {reg}")
        print(f"ICI set reg {reg} {val}")
        copy = Float()
        print(f"ICI: {Tetrad.decode_tetrad(val.content)}")
        copy.set_from_string(Tetrad.decode_tetrad(val.content))
        self.REGS[reg] = copy

    def reset_f_reg(self, reg: str, sgn=+1):
        if reg not in ("w", "E", "F"):
            raise ValueError(f"Not a float register: {reg}")
        if sgn == 0:
            raise ValueError(f"Bad sign for reset")
        self.REGS[reg].set_from_man_exp(sgn, "00000000000000", +1, "00")

    @classmethod
    def parse(cls, text: str) -> List[Tuple[int, str,str]]:
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
            if address=="0000": address="" # remove some noise
            print(f"{mem:<5}{opcode:<6}{mnemonic:<8}{address:<5}")

    def load(self, program: str):
        instructions = Machine.parse(program)
        self.drum_p.store(instructions)

    def run(self, start: int):
        self.pc = start
        self.pi = 0
        self.running = True
        self.alarm = False
        self.ch = True # test
        while self.running:
            if self.pi == 0:
                inst = self.drum_p.read(self.pc)
            else:
                self.pc = self.pc + 5
            inst.execute(self.pi, self)
            self.pi = (self.pi+1) % 2
            input("Key to continue ...")

    def test(self):
        for i in range(1000):
            mem = randint(0,100)*100+randint(0,20)*5
            op1 = randint(0,10000)
            op1 = f"{op1:05}"
            ad1 = randint(0,1000)
            ad1 = f"{ad1:04}"
            op2 = randint(0,10000)
            op2 = f"{op2:05}"
            ad2 = randint(0,1000)
            ad2 = f"{ad1:04}"
            inst = Instruction()
            inst.set_instruction(0,op1,ad1)
            inst.set_instruction(1,op2,ad2)
            rop1 = inst.get_opcode(0)
            rop2 = inst.get_opcode(1)
            rad1 = inst.get_address(0)
            rad2 = inst.get_address(1)

            print(f"ASS {repr(op1)} {repr(rop1)}")
            assert op1 == rop1
            print(f"ASS {repr(op2)} {repr(rop2)}")
            assert op2 == rop2
            print(f"ASS {repr(ad1)} {repr(rad1)}")
            assert ad1 == rad1
            print(f"ASS {repr(ad2)} {repr(rad2)}")
            assert ad2 == rad2
            print("ok")

