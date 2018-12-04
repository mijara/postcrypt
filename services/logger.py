from termcolor import colored


class Logger:
    def __init__(self, just, verbose):
        self.just = just
        self.verbose = verbose

    def log(self, verb, bold, rest, end='\n'):
        print(colored(verb.upper().ljust(self.just), 'yellow'), colored(bold, attrs=['bold']), rest, end=end)

    def error(self, rest):
        print(colored('error'.upper().ljust(self.just), 'red', attrs=['bold']), rest)
