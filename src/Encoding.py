from typing import List
from pprint import pprint

class Tetrad:
    """
    Represents a decimal digit (0–9) with conversion to bi-quinary 4 bits format.
    Mostly for fun because no low level processing is done at this physical representation level
    """

    # Table bi-quinary 4 bits modifiée
    _to_biquinary_table = {
        0: 0b0000,
        1: 0b0001,
        2: 0b0010,
        3: 0b0101,
        4: 0b0100,
        5: 0b1000,
        6: 0b1001,
        7: 0b1010,
        8: 0b1101,
        9: 0b1100
    }

    # Table inverse pour décoder : tous les autres codes -> 15
    _from_biquinary_table = {}
    for i in range(10):
        e = _to_biquinary_table[i]
        _from_biquinary_table[e] = i

    def __init__(self, val: int):
        self.bq = self._to_biquinary_table[val]

    def __repr__(self):
        return f"Tetrad({self.from_biquinary(self.bq)})"

    def __int__(self):
        return self.from_biquinary(self.bq)

    def __str__(self):
        return str(self.from_biquinary(self.bq))

    def __eq__(self, other):
        if isinstance(other, Tetrad):
            return self.bq == other.bq
        raise ValueError("Expecting a Tetrad")

    def __lt__(self, other):
        if isinstance(other, Tetrad):
            return int(self) < int(other)
        raise ValueError("Expecting a Tetrad")

    # -------------------------------
    # Méthodes bi-quinary
    # -------------------------------
    @classmethod
    def to_biquinary(cls, val:int) -> int:
        if not (0 <= val <= 9):
            raise ValueError("Tetrad must be between 0 and 9.")
        return cls._to_biquinary_table[val]

    @classmethod
    def from_biquinary(cls, bits: int) -> int:
        if not (0 <= bits <= 15):
            raise ValueError("Tetrad must be between 0 and 9.")
        val = cls._from_biquinary_table[bits]
        if val == None:
            raise ValueError(f"Invalid tetrad: {bits:04b}")
        return val

    @classmethod
    def encode_string(cls, s: str) -> List["Tetrad"]:  # forward ref
        print(s)
        tab = [Tetrad(int(d)) for d in s]
        return tab

    @classmethod
    def decode_tetrad(self, lst: List["Tetrad"]) -> str: # forward ref
        return "".join(map(str, lst))

class Word:

    def __init__(self):
        self.content = [Tetrad(0) for _ in range(18)]

    def __str__(self):
        return f"Word with value: {self.value}"


class Float(Word):
    def __init__(self):
        super().__init__()  # Call Word.__init__

    def __str__(self):
        return f"Float"


class Instruction(Word):

    INDS = [ "I", "J", "K", "L"]

    OPS = {
        "+":  "16",
        "-":  "26",
        "+*": "66",
        "-*": "76",
        "x":  "36",
        "x-": "35",
        "*":  "86",
        "*-": "85",
    }

    # removed no understood
    # MODS = {
    #     "+man": "12",
    #     "-man": "62",
    #     "+sgn": "22",
    #     "-sgn": "72",
    #     "+mod": "32",
    #     "-mod": "82",
    #     "+exp": "42",
    #     "-exp": "92",
    #     "noex": "13",
    #     "exno": "23",
    # }

    REGS = {
        "":  "40",   # w (acc)
        "E": "21",
        "F": "20",
        "V": "25",
        "W": "22",
        "A": "23",   # ruban A sans piste aux
        "Aa": "28",  # ruban A avec piste aux
        "B": "24",   # ruban B sans piste aux
        "Ba": "29"   # ruban B avec piste aux
    }

    BASE_TO_OPCODE = {
        "noop": "00000",

        #modifiers
        "+man": "00012",
        "-man": "00062",
        "+sgn": "00022",
        "-sgn": "00072",
        "+mod": "00032",
        "-mod": "00082",
        "+exp": "00042",
        "-exp": "00092",
        "noex": "00013",
        "exno": "00023",

        #inscriptions
        "->":  "09096",
        "=":   "09046",
        "->E": "07196",
        "=E":  "07146",
        "->F": "07096",
        "=F":  "07046",

        #registre d'indice
        "+wc=G": "06646",
        "+wc=H": "06746",
        "+wc=I": "06846",
        "+wc=J": "06946",

        "+wc->G": "06696",
        "+wc->H": "06796",
        "+wc->I": "06896",
        "+wc->J": "06996",

        "=G":  "06600",
        "=H":  "06700",
        "=I":  "06800",
        "=J":  "06900",

        "+M=G": "01600",
        "+M=H": "01700",
        "+M=I": "01800",
        "+M=J": "01900",

        #drum config
        "drum": "90000",

        # control
        "rv":    "40000",
        "end":   "42000",
        "=ch":   "07446",
        "rv-":   "41000",
        "+(H)":  "04216",
        "-(H)":  "09246",
        "rv(H)": "40200",
        "rvV=S": "43000",  # a clarifier
        "rvVft": "48000",  # a clarifier
        "rv-K":  "41400",  # back for routine with cond ?

         # transfert
        "A->prn" : "50000",
        "A->C"   : "53000",
        "A->drum": "54000",
        "B->prn":  "55000",
        "B->C":    "58000",
        "B->drum": "59000",
        "A->E":    "52100",
        "A->F":    "52000",
        "B->E":    "57100",
        "B->F":    "57000",
        "endA":    "92000",
        "grpA":    "91000",
        "posA":    "93000",
        "endB":    "97000",
        "grpB":    "96000",
        "posB":    "98000",
        "modA":    "95000",  # with i variants
        "modB":    "94000",  # with i variants
        "=W":      "07700",  # verifier manual says 0770 ?
        "->W":     "07296",
        "=W":      "07246",

        # config
        "float.pt":  "00011",
        "fixed.pt":  "00021",
        "end1":      "00031",
        "end2":      "00041",

        # alarmes
        "bloc.al":   "00014",
        "debloc.al": "00024",
        "eff.al":    "00034",
        "rv.al.gc":  "04600",  # TODO vérifier i
        "end.al":    "47000"
    }

    def _init_to_opcode(base, regs, ops, inds):
        # static list
        res = base.copy()

        # combinatory for operations on registers
        for mn_reg, oc_reg in regs.items():
            for mn_op, oc_op in ops.items():
                mn = f"{mn_op}{mn_reg}"
                oc = f"0{oc_reg}{oc_op}"
                res[mn] = oc

        # apply indices where appropriate
        prefixes = ("040", "090", "400")
        matching_keys = [k for k, v in res.items() if v.startswith(prefixes)]
        print("*** KEYS")
        print(matching_keys)
        for key in matching_keys:
            val = res[key]
            for i in [1,2,3,4]:
                mn = key+"("+inds[i-1]+")"
                oc = res[key]
                oc = oc[:2]+str(i)+oc[3:]
                res[mn] = oc

                if val.startswith("040"):
                    mn = key+"(v+"+inds[i-1]+")"
                    oc = "03"+str(i)+oc[3:]
                    res[mn] = oc

            if val.startswith("040"):
                mn = key + "(v)"
                oc = "030" + oc[3:]
                res[mn] = oc

        # removed not understood
        # combinatory for modifiers on registers
        # for mn_reg, oc_reg in regs.items():
        #     for mn_mod, oc_mod in mods.items():
        #         mn = f"{mn_mod}{mn_reg}"
        #         oc = f"0{oc_reg}{oc_mod}"
        #         res[mn] = oc

        return res

    def _init_to_mnemonic(to_opcode):
        res = {v: k for k, v in to_opcode.items()}
        return res

    TO_OPCODE = _init_to_opcode(BASE_TO_OPCODE,REGS,OPS, INDS)
    TO_MNEMONIC = _init_to_mnemonic(TO_OPCODE)

    pprint(TO_OPCODE)
    pprint(TO_MNEMONIC)

    def __init__(self):
        super().__init__()

    def set_instruction(self, i, opcode: str, address: str):
        if i not in (0, 1):
            raise ValueError("Bad instruction index")

        # 5 tetrad for opcode
        t_opcode = Tetrad.encode_string(opcode)

        # 4 tetrad for address
#        if int(address) % 5 != 0:
#            raise ValueError(f"Bad Address {address}")
        t_address = Tetrad.encode_string(address)

        # store
        self.content[i*9:i*9+5] = t_opcode
        self.content[i*9+5:i*9+9] = t_address

    def get_opcode(self, i) -> str:
        if i not in (0, 1):
            raise ValueError("Bad instruction index")
        return Tetrad.decode_tetrad(self.content[i*9:i*9+5])

    def get_address(self, i) -> str:
        if i not in (0, 1):
            raise ValueError("Bad instruction index")
        return Tetrad.decode_tetrad(self.content[i*9+5:i*9+9])

    def __str__(self):
        return f"Instruction word (opcode {self.opcode}) with value: {self.value}"

    @classmethod
    def opcode_to_mnemonic(cls, opcode: str) -> str:
        return Instruction.TO_MNEMONIC[opcode]

    @classmethod
    def mnemonic_to_opcode(cls, mnemonic: str) -> str:
        return Instruction.TO_OPCODE[str]

    def execute(self, pi: int, m:"Machine"):
        oc = self.get_opcode(pi)
        ad = self.get_address(pi)

        if oc.startswith("4"): # jump
            if oc=='40000':
                m.pc = int(ad)
            if oc=="41000" and m.ch:
                m.pc = int(ad)
            if oc=="42000":
                m.running = False
            if oc=="47000":
                m.running = False
                m.alarm = True



class Mantissa:
    """
    Represents a fixed-point decimal number with N Tetrads.
    Each Tetrad is a digit (0–9). N must be 14 or 18.
    """

    def __init__(self, digits: List['Tetrad']):
        if len(digits) not in (3, 15, 18): # 3 is for testing
            raise ValueError("Mantissa must have 14 or 18 tetrads")
        if not all(isinstance(d, Tetrad) for d in digits):
            raise TypeError("All elements must be Tetrad instances")
        self.digits = digits.copy()  # Most significant digit first
        self.N = len(digits)

    def __repr__(self):
        return f"Mantissa({''.join(str(d) for d in self.digits)})"

    def __getitem__(self, index):
        return self.digits[index]

    def __len__(self):
        return self.N

    def to_biquinary_list(self) -> List[int]:
        """Return the list of bi-quinary codes for the mantissa."""
        return [d.bq for d in self.digits]

    @classmethod
    def from_int_list(cls, values: List[int]) -> 'Mantissa':
        """Create a Mantissa from a list of integer digits (0-9)."""
        tetrads = [Tetrad(v) for v in values]
        return cls(tetrads)

    def add(self, other: 'Mantissa', carry=0) -> 'Mantissa':
        """
        Add two mantissas with the same number of digits.
        Returns a new Mantissa (modulo 10^N, carry truncated).
        """
        if self.N != other.N:
            raise ValueError("Mantissas must have the same length")

        result_digits = []

        # Add from least significant digit to most significant
        for d1, d2 in zip(reversed(self.digits), reversed(other.digits)):
            s = int(d1) + int(d2) + carry
            carry = s // 10
            result_digits.append(Tetrad(s % 10))

        # If there is a carry left, it is ignored (fixed-point truncation)
        result_digits.reverse()
        return Mantissa(result_digits)

    def complement9(self) -> 'Mantissa':
        """Return the 9's complement of this mantissa."""
        new_digits = [Tetrad(9 - int(d)) for d in self.digits]
        return Mantissa(new_digits)

    def sub(self, other: 'Mantissa') -> 'Mantissa':
        """
        Add two mantissas with the same number of digits.
        Returns a new Mantissa (modulo 10^N, carry truncated).
        """
        if self.N != other.N:
            raise ValueError("Mantissas must have the same length")
        return self.add(other.complement9(),1)