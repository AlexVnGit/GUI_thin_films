with open('teste.txt', 'w') as file:
    for i in range(7501, 8001):
        file.write(str(i * 0.001) + '\n')