from colorama import init, Fore, Back, Style

init(autoreset=True)
print(Fore.YELLOW + 'Welcome, what do you want to do?')
print(Fore.GREEN + '1. Update Google Sheet from XMLs (Safe: New and Empty Entities)')
print(Fore.RED + '2. Update XMLs from Google Sheet (Unsafe: Overwrites)')
print(Style.RESET_ALL)
input('Select [1|2]:')