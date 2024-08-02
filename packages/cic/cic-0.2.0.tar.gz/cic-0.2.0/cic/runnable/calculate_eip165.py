# standard imports
import logging
import sys

# external imports
import sha3

logging.basicConfig(level=logging.WARNING)
#logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

def main():
    if __name__ == '__main__':
        f = open(sys.argv[1], 'r')
        z = b''
        for i in range(32):
            z += b'\x00'
        while True:
            l = f.readline().rstrip()
            if l == '':
                break
            logg.debug('line {}'.format(l))
            h = sha3.keccak_256()
            h.update(l.encode('utf-8'))
            r = h.digest()
            z = bytes([a ^ b for a, b in zip(r, z)])
            logg.debug('{} -> {}'.format(r.hex(), z.hex()))
        f.close()

        print(z[:4].hex())


if __name__ == '__main__':
    main()
