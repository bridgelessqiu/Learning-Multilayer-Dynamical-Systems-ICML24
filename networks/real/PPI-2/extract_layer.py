import sys

k = int(sys.argv[1]) # Number of layers
network_name = str(sys.argv[2])

S = set() # Count how many vertices are there

n = 900

m = 0

for i in range(1, k + 1):
    layer = open("G_" + str(i) + ".edges", 'w') 
    with open(network_name + ".edges") as file:
        for line in file:
            if line[0] == str(i):
                if int(line.split(' ')[1]) <= n and int(line.split(' ')[2]) <= n:
                    S.add(int(line.split(' ')[1]))
                    S.add(int(line.split(' ')[2]))
                    layer.write(line.split(' ')[1] + ' ' + line.split(' ')[2] + '\n')
                    m += 1

    layer.close()

print("N: {}".format(len(S)))
print("M: {}".format(m))
