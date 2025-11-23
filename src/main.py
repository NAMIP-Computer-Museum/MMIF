from Encoding import Tetrad, Mantissa
from MMIF import Machine

if __name__ == "__main__":
    for i in range(10):
        t = Tetrad(i)
        e = t.bq
        d = int(t)
        print(f"{i} {e} {d}")

#   Tetrad.from_biquinary(0b1110)

    m1 = Mantissa.from_int_list([1, 2, 3])
    m2 = Mantissa.from_int_list([4, 3, 2])

    print("m1 =", m1)
    print("m2 =", m2)

    # Add them
    m3 = m1.add(m2)
    print("m1 + m2 =", m3)

    print(m1.complement9())

    m4 = m2.sub(m1)
    print("m2 - m1 =", m4)

    source = """
    -> r1
    =  F
    -* 0003
    =  r2
    +  man
    +  F
    x 
    """

    bin = """
0015  90000  0006  54000  0000
0020  92000  0000  06800  0000
0025  95000  0009  90000  0005
0030  52000  0000  06900  0001
0035  48000  0040  06900  0000
0040  02566  0000  06646  0000
0045  04168  0000  02078  0000
0050  04169  0000  02079  0000
0055  07146  0000  00082  0000
0060  02116  0000  07446  0000
0065  41000  0090  03476  0000
0070  07446  0000  41000  0030
0075  03376  0000  07446  0000
0080  41000  0095  06800  0001
0085  90000  0006  40000  0030
0090  42000  8888  40000  0030
    """

    Machine.decompile(bin)
