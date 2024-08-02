# standard imports
import sys
import json

def main():
    merged = []
    for a in sys.argv[1:]:
        f = open(a, 'r')
        j = json.load(f)
        f.close()
        merged += j

    print(json.dumps(merged))

if __name__ == '__main__':
    main()
