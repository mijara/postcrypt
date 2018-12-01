import sys

from postcrypt import Postcrypt

if __name__ == '__main__':
    """
    options = []
    if len(sys.argv) > 2:
        options = [arg.replace('--', '') for arg in sys.argv[2:]]
        print(options)
    """

    postcrypt = Postcrypt(sys.argv[1], sys.argv[2])
    postcrypt.process()
