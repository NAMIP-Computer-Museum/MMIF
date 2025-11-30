def encode_float(f):
    if f == 0.0:
        return '+000000000000000+000'

    sign = '+' if f > 0 else '-'
    f_abs = abs(f)

    import math
    exponent = int(math.floor(math.log10(f_abs))) + 1  # +1 because digit point before mantissa
    mantissa = f_abs / (10 ** exponent)

    mantissa_scaled = int(round(mantissa * 10 ** 15))  # 15 digits after decimal
    mantissa_str = f"{mantissa_scaled:015d}"

    exp_sign = '+' if exponent >= 0 else '-'
    exp_str = f"{abs(exponent):03d}"

    return f"{sign}{mantissa_str}{exp_sign}{exp_str}"


def decode_float(s):
    sign_char = s[0]
    mantissa_str = s[1:16]
    exp_sign = s[16]
    exp_str = s[17:]

    mantissa = int(mantissa_str) / 10 ** 15
    exponent = int(exp_str)
    if exp_sign == '-':
        exponent = -exponent

    value = mantissa * (10 ** exponent)
    if sign_char == '-':
        value = -value
    return value


# --- Round-trip check ---
test_values = [123.45, -0.00123, 0.0, 1.23456789012345e10, -9.87654321e-5]

for v in test_values:
    encoded = encode_float(v)
    decoded = decode_float(encoded)
    print(f"Original: {v}")
    print(f"Encoded : {encoded}")
    print(f"Decoded : {decoded}")
    print(f"Match   : {abs(v - decoded) < 1e-14}\n")
