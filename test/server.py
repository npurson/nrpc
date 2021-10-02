import array
import argparse
import numpy as np

import sys
sys.path.append('..')
from nrpc import Server


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int)
    parser.add_argument('--mode', type=str)
    return parser.parse_args()


def main(args):
    server = Server(args.port, mode=args.mode, bufsz=8194)

    def func(x):
        out = bytes(map(lambda x: x + 1, x.encode())).decode() \
            if args.mode == 'str' else \
            np.asarray(x) * 2
            # lambda a: array.array('d', list(map(lambda x: x * 2, a)))
        return out

    server.loop(callback=func)


if __name__ == '__main__':
    args = parse_args()
    main(args)
