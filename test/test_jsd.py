from experiments.utils import jsd

def test_jsd():
    p = {"000": 50, "111": 50}
    q_uni = {"000": 12.5, "001": 12.5, "010": 12.5, "011": 12.5, "100": 12.5, "101": 12.5, "110": 12.5, "111": 12.5}
    q_noisy = {"000": 68, "001": 10, "010": 8, "011": 8, "111": 6}

    d_uni = jsd(p, q_uni, num_clbits=3)
    d_noi = jsd(p, q_noisy, num_clbits=3)
    d_exa = jsd(p, p, num_clbits=3)

    print(d_uni)
    print(d_noi)
    print(d_exa)

if __name__ == "__main__":
    test_jsd()