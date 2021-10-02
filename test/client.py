import array
import random
import string
import argparse
import numpy as np

np.ndarray([1, 2])

import sys
sys.path.append('..')
from nrpc import Client


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--addr', type=str)
    parser.add_argument('--port', type=int)
    parser.add_argument('--mode', type=str)
    return parser.parse_args()


def main(args):

    for i in range(10):
        if i % 4 == 0:
            client = Client(args.addr, args.port, mode=args.mode, bufsz=8194)

        if args.mode == 'str':
            digits = [random.choice(string.digits + string.ascii_letters) for _ in range(8188)]
            tx = ''.join(digits)
        elif args.mode == 'array':
            tx = array.array('d', (random.random() * 100 for _ in range(8188)))

        client.send(tx)
        _, rx = client.recv()

        try:
            if args.mode == 'str':
                assert rx == bytes(map(lambda x: x + 1, tx.encode())).decode()
            elif args.mode == 'array':
                assert (rx == np.asarray(tx) * 2).all()
            client.logger(('VERIFIED',))
        except AssertionError:
            import pdb; pdb.set_trace()
            raise

        if (i + 1) % 4 == 0:
            client.close_connect()
    client.close_remote()


if __name__ == '__main__':
    args = parse_args()
    main(args)
