import sys

from postcrypt import Postcrypt

if __name__ == '__main__':
    postcrypt = Postcrypt(sys.argv[1])
    postcrypt.process()
