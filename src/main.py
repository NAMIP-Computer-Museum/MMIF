from ALU import Tetrad, Mantissa

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
