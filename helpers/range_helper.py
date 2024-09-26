import argparse
def float_range(x):
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError(f"{x} 0 ile 1 arasında olmalıdır.")
    return x