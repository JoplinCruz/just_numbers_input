from jn_input import jn_input
import time

i = jn_input('\033[2J'+'\033[6;12H'+'Idade: ')

if i == None or i == '':
    print ('\033[8;12H'+'Hum! Acho que você não quer revelar a sua idade.')
else:
    print ('\033[8;12H'+f'Muito bem, você nasceu em {2024-i}.')

t = 5
while t > 0:
    if t > 1:
        print ('\033[9;12H'+f'continue em {t} segundos...')
    else:
        print ('\033[9;12H'+f'continue em {t} segundo... ')
    t -= 1
    time.sleep(1)
