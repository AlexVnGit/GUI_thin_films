import os
decision = input('Create or Destroy Files? C/D ')

if decision == 'c' or decision == 'C':
    with open('energies1.txt', 'w') as file:
        for i in range(4000, 4501):
            file.write(str(i * 0.001) + '\n')

    with open('energies2.txt', 'w') as file:
        for i in range(4501, 5001):
            file.write(str(i * 0.001) + '\n')

    with open('energies3.txt', 'w') as file:
        for i in range(5001, 5501):
            file.write(str(i * 0.001) + '\n')

    with open('energies4.txt', 'w') as file:
        for i in range(5501, 6001):
            file.write(str(i * 0.001) + '\n')

    with open('energies5.txt', 'w') as file:
        for i in range(6001, 6501):
            file.write(str(i * 0.001) + '\n')

    with open('energies6.txt', 'w') as file:
        for i in range(6501, 7001):
            file.write(str(i * 0.001) + '\n')

    with open('energies7.txt', 'w') as file:
        for i in range(7001, 7501):
            file.write(str(i * 0.001) + '\n')

    with open('energies8.txt', 'w') as file:
        for i in range(7501, 8001):
            file.write(str(i * 0.001) + '\n')

elif decision == 'd' or decision == 'D':
    if os.path.isfile('energies1.txt') == True:
        os.remove('energies1.txt')
        os.remove('energies2.txt')
        os.remove('energies3.txt')
        os.remove('energies4.txt')
        os.remove('energies5.txt')
        os.remove('energies6.txt')
        os.remove('energies7.txt')
        os.remove('energies8.txt')

else:
    print('Nothing Happened')        