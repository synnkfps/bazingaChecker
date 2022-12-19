# Made by Bazinga

# Imports
import requests
import random, colorama
import re, os
fileDir = os.path.dirname(os.path.realpath(__file__))
print('Current file dir: ' + fileDir)

# Generate Pattern
def randomPattern(pattern) -> str:
    vowels: str = 'aeiou'
    consonants: str = 'bcdfghjklmnpqrstvwxyz'
    build: str = ''

    for i in pattern:
        if i == 'v': build += random.choice(list(vowels))
        if i == 'V': build += random.choice(list(vowels)).upper()
        
        if i == 'c': build += random.choice(list(consonants))
        if i == 'C': build += random.choice(list(consonants)).upper()

        if i == 'n': build += str(random.randrange(0, 10)) # numbers
    
    return build

# Variables (pattern to choose | regex matcher | generated nicks list)
pattern: str = 'Cvcv'
matcher: str = '....'
generated: list = []

# Files
unavailable_file = open(rf'{fileDir}\unavailable.txt', 'r+')
unavailable_cache = unavailable_file.readlines()

available_file = open(rf'{fileDir}\available.txt', 'r+')
available_cache = available_file.readlines()

for x, y in enumerate(available_cache): available_cache[x] = y.replace('\n', '')
for x, y in enumerate(unavailable_cache): unavailable_cache[x] = y.replace('\n', '')
    
# Generate 300 nicks
for i in range(1200):
    b = randomPattern(pattern)
    while b in unavailable_cache or b in available_cache: 
        b = randomPattern(pattern)
    
    generated.append(b)

# Send requests
for i in generated:
    r = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{i}', headers={'User-Agent': 'Chrome'}).text # get the requested API's text

    if '"name"' in r:
        print(f'> {i} {colorama.Fore.RED}UNAVAILABLE{colorama.Fore.RESET}', f'{colorama.Fore.BLACK}{r}{colorama.Fore.RESET}')
        unavailable_file.write('\n'+i)
    elif '"error"' in r:
        print(f'> {i} {colorama.Fore.YELLOW}RATE-LIMIT{colorama.Fore.RESET}', f'{colorama.Fore.BLACK}{r}{colorama.Fore.RESET}')
        break
    else:
        print(f'{i} {colorama.Fore.GREEN}AVAILABLE{colorama.Fore.RESET}', f'{colorama.Fore.BLACK}{r}{colorama.Fore.RESET}')
        available_file.write('\n'+i)

available_file.close()
unavailable_file.close()