def calculate_totient_euler(p: int, q: int) -> int:
    phi_n = (p - 1) * (q - 1)
    return phi_n