import sys

k = int(sys.argv[1]) # Number of layers
network_name = str(sys.argv[2])

for i in range(1, k + 1):
    layer = open("G_" + str(i) + ".edges", 'w') 
    with open(network_name + ".edges") as file:
        for line in file:
            if line[0] == str(i):
                layer.write(line.split(' ')[1] + ' ' + line.split(' ')[2] + '\n')

    layer.close()
