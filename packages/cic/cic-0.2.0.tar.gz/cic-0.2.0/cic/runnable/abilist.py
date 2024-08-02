# standard imports
import json
import sys

# external imports
import sha3


def main():
    f = open(sys.argv[1], 'r')
    o = json.load(f)
    f.close()

    ks = []
    r = {}
    for v in o:
        if v['type'] != "function":
            continue
        name = ''
        try:
            name = v['name']
        except KeyError:
            continue
        args = []
        for vv in v['inputs']:
            args.append(vv['type'])
        sig = '{}({})'.format(name, ','.join(args))
        h = sha3.keccak_256()
        h.update(sig.encode('utf-8'))
        z = h.digest()
        k = z[:4].hex()
        #ks.append(k)
        r[k] = sig

    ks = list(r.keys())
    ks.sort()
    for k in ks:
        print("{}\t{}".format(k, r[k]))

if __name__ == '__main__':
    main()
