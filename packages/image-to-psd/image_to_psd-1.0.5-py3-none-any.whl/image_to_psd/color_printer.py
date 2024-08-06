from colorama import Fore, Style

def print_red(value):
    print(Fore.RED + value + Style.RESET_ALL)

def print_green(value):
    print(Fore.GREEN + value + Style.RESET_ALL)

def print_cyan(value):
    print(Fore.CYAN + value + Style.RESET_ALL)

def print_white(value):
    print(Fore.WHITE + value + Style.RESET_ALL)


def print_yellow(value):
    print(Fore.YELLOW + value + Style.RESET_ALL)


def print_blue(value):
    print(Fore.BLUE + value + Style.RESET_ALL)


def print_magenta(value):
    print(Fore.MAGENTA + value + Style.RESET_ALL)


if __name__ == '__main__':
    print_red('This is red')
    print_green('This is green')
    print_cyan('This is cyan')
    print_white('This is white')
    print_yellow('This is yellow')
    print_blue('This is blue')
    print_magenta('This is magenta')