import sys

from postcrypt import Postcrypt

if __name__ == '__main__':
    """
    options = []
    if len(sys.argv) > 2:
        options = [arg.replace('--', '') for arg in sys.argv[2:]]
        print(options)
    """

    mode = None
    if len(sys.argv) > 2:
        mode = sys.argv[2]

    postcrypt = Postcrypt(sys.argv[1], mode)
    postcrypt.process()
