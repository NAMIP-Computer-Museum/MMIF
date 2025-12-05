from typing import List
from pprint import pprint
import math

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
    def __init__(self, s_man=+1, man="000000000000000", s_exp=+1, exp="00"):
        super().__init__()  # Call Word.__init__
        self.set_from_man_exp(s_man, man, s_exp, exp)

    def __str__(self):
        return f"Float {self.get_float()}"

    def get_float(self):
        return self.get_mantissa()*10**self.get_exponent()

    def get_mantissa(self) -> float:
        sm = "0."+Tetrad.decode_tetrad(self.content[1:16])
        return self.get_m_sign()*float(sm)

    def get_exponent(self) -> int:
        se = Tetrad.decode_tetrad(self.content[16:18])
        return self.get_e_sign()*float(se)

    def set_exponent(self, exp: str):
        if len(exp) != 2:
            raise ValueError("Exponent digit string of length 2 expected")
        self.content[-2:] = Tetrad.encode_string(exp)

    def set_mantissa(self, mantissa: str):
        if len(mantissa) != 15:
            raise ValueError("Mantissa digit string of length 15 expected")
        self.content[1:16] = Tetrad.encode_string(mantissa)

    # TODO not sure assume "bit" 1
    def get_m_sign(self) -> int:
        ss = Tetrad.decode_tetrad(self.content[0:1])
        sg = int(ss)
        if sg % 2 == 0:
            return +1
        else:
            return -1

    def set_m_sign(self, s_man: int):
        s_exp = self.get_e_sign()
        sgn = 0
        if s_man<0: sgn = sgn+1
        if s_exp<0: sgn = sgn+2
        self.content[0:1] = Tetrad.encode_string(f"{sgn}")

    # TODO not sure assume "bit" 2
    def get_e_sign(self) -> int:
        ss = Tetrad.decode_tetrad(self.content[0:1])
        sg = int(ss)//2
        if sg % 2 == 0:
            return +1
        else:
            return -1

    def set_e_sign(self, s_exp: int):
        s_man = self.get_m_sign()
        sgn = 0
        if s_man<0: sgn = sgn+1
        if s_exp<0: sgn = sgn+2
        self.content[0:1] = Tetrad.encode_string(f"{sgn}")

    def set_from_string(self,s:str):
        if len(s) != 18:
            raise ValueError("Initialise from string requires 18 characters")
        self.content = Tetrad.encode_string(s)

    def set_from_man_exp(self, s_man: int, man: str, s_exp: int, exp:str):
        if s_man == 0:
            raise ValueError("Bad mantissa sign")
        if s_exp == 0:
            raise ValueError("Bad exponent sign")
        if len(man) != 15:
            raise ValueError("Bad mantissa length")
        if len(exp) != 2:
            raise ValueError("Bad exponent length")

        sgn = 0
        if s_man<0: sgn = sgn+1
        if s_exp<0: sgn = sgn+2
        s = f"{sgn}{man}{exp}"
        self.content = Tetrad.encode_string(s)

    def set_from_float(self, f):
        if f == 0:
            s_man=+1
            man="000000000000000"
            s_exp=+1
            exp="00"  # TODO not sure how zero is encoded
        else:
            s_man = +1 if f >= 0 else -1
            f_abs = abs(f)

            exponent = int(math.floor(math.log10(f_abs))) + 1  # +1 because digit point before mantissa
            if abs(exponent)>49:
                raise ValueError(f"Exponent cannot too large: {exponent}")
            mantissa = f_abs / (10 ** exponent)
            mantissa_scaled = int(round(mantissa * 10 ** 15))  # 15 digits after decimal
            man = f"{mantissa_scaled:015d}"

            s_exp = +1 if exponent >= 0 else -1
            exp = f"{abs(exponent):02d}"

        self.set_from_man_exp(s_man, man, s_exp, exp)

    def get_accent(self):
        return int(Tetrad.decode_tetrad(self.content[1:5]))

    def alter(self, alt: str):
        if alt is None:
            return
        elif alt == "12": # +man
            self.set_exponent("00")
            self.set_m_sign(+1)
            self.set_e_sign(+1)
        elif alt == "62": # -man
            self.set_exponent("00")
            self.set_m_sign(-1)
            self.set_e_sign(+1)
        elif alt == "22": # +sgn
            sgn = self.get_m_sign()
            self.set_from_man_exp(+sgn, "100000000000000", +1, "01")
        elif alt == "32": # +mod
            self.set_m_sign(+1)
        elif alt == "32": # -mod
            self.set_m_sign(-1)
        elif alt == "72": # -sgn
            sgn = self.get_m_sign()
            self.set_from_man_exp(-sgn, "100000000000000", +1, "01")
        elif alt == "42": # +exp
            self.set_mantissa("100000000000000")
            self.set_m_sign(+1)
        elif alt == "92": # -exp
            self.set_mantissa("100000000000000")
            self.set_m_sign(+1)
            sgn = self.get_e_sign()
            self.set_e_sign(-sgn)
        else:
            raise ValueError(f"Alteration {alt} is not supported")

        print(f"ALT {self}")

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

    # not sur if static of class better
    @classmethod
    def opcode_to_mnemonic(cls, opcode: str) -> str:
        return Instruction.TO_MNEMONIC[opcode]

    @classmethod
    def mnemonic_to_opcode(cls, mnemonic: str) -> str:
        return Instruction.TO_OPCODE[str]

    @classmethod
    def compute(cls, op, a, b):
        fa = a.get_float()
        fb = b.get_float()
        if op == "16":  # +
            fr = fa+fb
        elif op == "26":  # -
            fr = fa-fb
        elif op == "66":  # +*  # TODO non normalised not supported
            fr = fa+fb
        elif op == "76":  # -* # TODO non normalised not supported
            fr = fa-fb
        elif op == "36":
            fr = fa*fb
        elif op == "35":
            fr = fa*(-fb)
        else:
            raise ValueError(f"Arithmetic operation not supported {op}")
        res = Float()
        res.set_from_float(fr)
        print(f"a: {fa}  b:{fb}  res:{res.get_float()}")
        return res

    def execute(self, pi: int, m:"Machine"):
        oc = self.get_opcode(pi)
        ad = self.get_address(pi)

        mne = Instruction.opcode_to_mnemonic(oc)
        s_ad = ad
        i_ad = int(ad)
        if s_ad == "0000": s_ad = ""  # remove some noise
        print("----------------------------------------")
        nw = m.get_f_reg("w")
        ne = m.get_f_reg("E")
        nf = m.get_f_reg("F")
        print(f"w: {nw} E:{ne} F:{nf}")
        print(f"{m.pc:<5}{oc:<6}{mne:<8}{s_ad:<5}")

        # config
        if oc.startswith("9"):
            if oc=="90000":
                if i_ad==6: # TODO normal configuration - this is our default but need to adapt
                    return

        # jumps and stop points
        if oc.startswith("4"):
            if oc=="40000":
                m.pc = int(ad)
                return
            if oc=="41000" and m.ch:
                m.pc = int(ad)
                return
            if oc=="41400":
                m.running = False # TODO used here for testing routine
                return
            if oc=="42000":
                m.running = False
                return
            if oc=="47000":
                m.running = False
                m.alarm = True
                return

        # comparison (for jump)
        if oc == "07446":  # =ch
            w = m.get_f_reg("w")
            m.ch = (w.get_m_sign()<0)
            m.reset_f_reg("w")   # TODO check but consistent with =
            return

        # alteration: it is provisioned and interpreted on next order register
        if (oc.startswith("000")):
            m.alt = oc[3:5]
#            print(f"Alteration recorded {m.alt}")
            return

        # immediate operation
        if oc.startswith("03"):
            idx = int(oc[2])
            op  = oc[3:5]
            imm = i_ad+idx       # address is interpreted as immediate value, index is added
            man = f"{imm:04d}" + "0"*11
            val = Float(+1,man,+1,"00")
            val.alter(m.alt)
            m.alt = None
            w = m.get_f_reg("w")
            w = Instruction.compute(op, w, val)
            m.set_f_reg("w",w)
            return

        # operation with E or F register
        if oc.startswith("020") or oc.startswith("021"):
            op  = oc[3:5]
            if oc.startswith("020"):
                val = m.get_f_reg("F")
            else:
                val = m.get_f_reg("E")
            copy = Float()
            copy.set_from_string(Tetrad.decode_tetrad(val.content))
            copy.alter(m.alt)
            m.alt = None
            w = m.get_f_reg("w")
            w = Instruction.compute(op, w, copy)
            m.set_f_reg("w",w)
            return

        # operation with memory
        if oc.startswith("04"):
            idx = int(oc[2])
            op  = oc[3:5]
            word = m.drum_p.read(int(ad))
            copy = Float()
            copy.set_from_string(Tetrad.decode_tetrad(word.content))
            copy.alter(m.alt)
            m.alt = None
            w = m.get_f_reg("w")
            w = Instruction.compute(op, w, copy)
            m.set_f_reg("w",w)
            return

        if oc.startswith("070") or oc.startswith("071"):
            reg = "F"
            if oc[2]=="1": reg = "E"
            if oc.endswith("96"):
                m.set_f_reg(reg, m.get_f_reg("w"))
                return
            if oc.endswith("46"):
                print(f"w: {m.get_f_reg('w')}")
                m.set_f_reg(reg, m.get_f_reg("w"))
                m.reset_f_reg("w")
                print(f"F: {m.get_f_reg('F')}")
                return

        # transfer back to memory
        if oc.startswith("090"):
            val = m.get_f_reg("w")
            copy = Float()
            copy.set_from_string(Tetrad.decode_tetrad(val.content))

            if oc == "09096":    # ->
                print(val)
                m.drum_p.write(i_ad, copy)
                print(f"CHECK {m.drum_p.read(i_ad)}")
                return
            if oc == "09046":  # =  resets to 0
                m.drum_p.write(i_ad, copy)
                m.reset_f_reg("w")
                return


        # tape operations
        if oc.startswith("5"):
            if oc=="50000":
                raise NotImplemented("A->prn")
            elif oc=="53000":
                raise NotImplemented("A->C")
            elif oc=="54000":
                raise NotImplemented("A->drum")
            elif oc=="55000":
                raise NotImplemented("B->prn")
            elif oc=="5800":
                raise NotImplemented("B->C")
            elif oc=="54000":
                raise NotImplemented("B->drum")
            elif oc=="52100":
                raise NotImplemented("A->E")
            elif oc=="52000":
                print("TODO A->F") # TODO
                return
            elif oc=="57100":
                raise NotImplemented("B->E")
            elif oc=="57000":
                raise NotImplemented("B->F")

        raise ValueError(f"Instruction {oc} not yet supported")

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