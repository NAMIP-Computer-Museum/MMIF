from typing import List

class Tetrad:
    """Représente un chiffre décimal (0–9) avec conversion bi-quinary 4 bits."""

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
