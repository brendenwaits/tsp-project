import math
import random
import sys

from statistics import stdev, mean
from time import perf_counter
import signal

# globals
nodes = []
distances = []
time_elapsed = 0.0;

# build list from txt file
def build():
    f = open(sys.argv[1], "r")

    for l in f:
        s = l.split(' ')
        nodes.append([float(s[1]), float(s[2]), int(s[0])])

    f.close()

    # distances = [[None for x in range(len(nodes))] for x in range(len(nodes))]
    for x in range(len(nodes)):
        distances.append([])
        for y in range(len(nodes)):
            distances[x].append(None)

    #populate distances
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i == j:
                distances[i][j] = 0

            elif distances[j][i] is not None:
                distances[i][j] = distances[j][i]

            else:
                distances[i][j] = int(math.sqrt((nodes[i][0] - nodes[j][0])**2 + (nodes[i][1] - nodes[j][1])**2))

# distance funciton to compute distance of the entire tour
def distance(t):
    result = 0

    i = 1
    while i < len(t):
        result += distances[t[i][2] - 1][t[i-1][2] - 1]
        i += 1

    return result

# write results to file
def result(best):
    f = open(sys.argv[2], "w")

    f.write(str(distance(best)) + "\n")

    for b in best:
    	f.write(str(b[2]) + " ")

    f.close()

 
def compute():
    results = []
    for i in range(10):
        sa_result = sa()
        if sa_result is not None:
            results.append(distance(sa_result))
        else:
            break #None means time expired

    print(results)
    print("stdev: " + str(stdev(results)))
    print("mean: " + str(mean(results)))

# anneal function
def sa():
    t = 1000000
    cr = .0001

    current = nodes.copy()
    best = current

    while t > 1:
        new = current.copy()

        # p1 = random.randint(0, len(new) - 1)
        # p2 = random.randint(0, len(new) - 1)

        #This is just a test, I dont want to handle edge case of edge swapping so fix this
        p1 = random.randint(1, len(new) - 2)
        p2 = p1
        while (p2 == p1):
            p2 = random.randint(1, len(new) - 2)

        new[p1], new[p2] = new[p2], new[p1]

        c = distance(current)

        curr_p1prev = current[p1 - 1][2] - 1
        curr_p1 = current[p1][2] - 1
        curr_p1next = current[p1 + 1][2] - 1

        curr_p2prev = current[p2 - 1][2] - 1
        curr_p2 = current[p2][2] - 1
        curr_p2next = current[p2 + 1][2] - 1

        #sequential nodes p1 < p2 
        if (p1 - p2 == -1):
            c_removed = (distances[curr_p1prev][curr_p1] + distances[curr_p2][curr_p2next]) 
            n_added = (distances[curr_p1prev][curr_p2] + distances[curr_p1][curr_p2next])

        #sequential nodes p1 > p2 
        elif (p1 - p2 == 1):
            c_removed = (distances[curr_p2prev][curr_p2] + distances[curr_p1][curr_p1next]) 
            n_added = (distances[curr_p2prev][curr_p1] + distances[curr_p2][curr_p1next])

        #non-sequential nodes
        else:
            c_removed = distances[curr_p1prev][curr_p1] + distances[curr_p1][curr_p1next] + distances[curr_p2prev][curr_p2] + distances[curr_p2][curr_p2next] 
            n_added = distances[curr_p1prev][curr_p2] + distances[curr_p2][curr_p1next] + distances[curr_p2prev][curr_p1] + distances[curr_p1][curr_p2next]
        
        n = c - c_removed + n_added

        try:
            if math.exp((c-n)/t) > random.random():
                current = new
        except OverflowError:
            pass

        if n < c:
            best = new

        t *= 1 - cr

    return best

curr_time = perf_counter()
build()
compute()
end_time = perf_counter()
print("time elapsed: ", end_time - curr_time)