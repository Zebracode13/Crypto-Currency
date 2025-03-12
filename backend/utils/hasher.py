import hashlib
import json

# hashs a given data and returns a 16


def hasher(*args):
    """retures a sha-256 hash of the given arguments"""

    stringify_args = sorted(map(lambda data: json.dumps(data), args) )
    str_data = ''.join(stringify_args)
    
    return hashlib.sha256(str_data.encode('utf-8')).hexdigest()


def main():
    print(hasher("hi", 8, [0]))
    print(hasher(8, [0],"hi",))

if __name__ == '__main__':
    main()