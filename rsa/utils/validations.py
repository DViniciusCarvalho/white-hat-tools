def numbers_are_coprimes(public_key: int, phi_n: int) -> bool:
    mdc = 0
    while phi_n != 0:
        mdc = phi_n
        phi_n = public_key % phi_n
        public_key = mdc
    if mdc == 1:
        return True
    else:
        return False