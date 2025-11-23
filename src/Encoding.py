from typing import List

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
        tab = [Tetrad(int(d)) for d in s]

class Word:

    def __init__(self):
        self.tab = [Tetrad() for _ in range(18)]

    def __str__(self):
        return f"Word with value: {self.value}"


class Float(Word):
    def __init__(self, mantissa, exponent):
        super().__init__()  # Call Word.__init__

    def __str__(self):
        return f"Float"


class Instruction(Word):

    TO_OPCODE = {
        #arithmetic
        "+":  "04016",
        "-":  "04026",
        "+*": "04066",
        "-*": "04076",
        "x":  "04036",
        "x-": "04035",
        "*-": "04086",
        "*-": "04085",

        "+E":  "02116",
        "-E":  "02126",
        "+*E": "02166",
        "-*E": "02176",
        "xE":  "02136",
        "x-E": "02135",
        "*-E": "02186",
        "*-E": "02185",

        "+F":  "02016",
        "-F":  "02026",
        "+*F": "02066",
        "-*F": "02076",
        "xF":  "02036",
        "x-F": "02035",
        "*-F": "02086",
        "*-F": "02085",

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

        #alterations --> sur W E F
        "+man": "04012",
        "-man": "04062",
        "+sgn": "04022",
        "-sgn": "04072",
        "+mod": "04032",
        "-mod": "04082",
        "+exp": "04042",
        "-exp": "04092",
        "noex": "04013",
        "exno": "04023",

        "+manF": "02012",
        "-manF": "02062",
        "+sgnF": "02022",
        "-sgnF": "02072",
        "+modF": "02032",
        "-modF": "02082",
        "+expF": "02042",
        "-expF": "02092",
        "noexF": "02013",
        "exnoF": "02023",

        "+manE": "02112",
        "-manE": "02162",
        "+sgnE": "02122",
        "-sgnE": "02172",
        "+modE": "02132",
        "-modE": "02182",
        "+expE": "02142",
        "-expE": "02192",
        "noexE": "02113",
        "exnoE": "02123",

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

        # alarmes
        "bloc.al":   "00014",
        "debloc.al": "00024",
        "eff.al":    "00034",
        "rv.al.gc":  "04600",  # TODO vérifier i
        "end.al":    "47000"
    }

    TO_MNEMONIC = {v: k for k, v in TO_OPCODE.items()}
    print(TO_MNEMONIC)

    def __init__(self, mnemonic: str, address: int):
        super().__init__()
        # 5 tetrad for opcode
        t_opcode = Tetrad.encode_string(self.mnemonic_to_opcode(str))

        # 4 tetrad for address
        if address % 5 != 0:
            raise ValueError(f"Bad Address {address}")
        t_address = Tetrad.encode_string(address)

    def __str__(self):
        return f"Instruction word (opcode {self.opcode}) with value: {self.value}"

    @classmethod
    def opcode_to_mnemonic(cls, opcode: str) -> str:
        print(opcode)
        return Instruction.TO_MNEMONIC[opcode]

    @classmethod
    def mnemonic_to_opcode(cls, mnemonic: str) -> str:
        return Instruction.TO_OPCODE[str]

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