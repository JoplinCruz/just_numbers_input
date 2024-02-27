from jn_input import jn_input
import time

i = jn_input('\033[2J'+'\033[6;12H'+'Your age: ')

if i == None or i == '':
    print ('\033[8;12H'+'Hmm, I think you don\'t want to reveal your age.')
else:
    print ('\033[8;12H'+f'Cool, you were born in {2024-i}.')

t = 5
while t > 0:
    if t > 1:
        print ('\033[9;12H'+f'continues in {t} seconds...')
    else:
        print ('\033[9;12H'+f'continues in {t} second... ')
    t -= 1
    time.sleep(1)
