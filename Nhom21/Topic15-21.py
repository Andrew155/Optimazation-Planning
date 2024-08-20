input_string = input()
n_k = input_string.split(' ')

N = int(n_k[0])
K = int(n_k[1])

QuatityAndCost = []
LowerAndUpperBounds = []

for i in range(N):
    quatity_cost = input()
    quatity_cost_new = quatity_cost.split(' ')
    QuatityAndCost.append((int(quatity_cost_new[0]), int(quatity_cost_new[1])))

for i in range(K):
    capacity = input()
    capacity_new = capacity.split(' ')
    LowerAndUpperBounds.append((int(capacity_new[0]), int(capacity_new[1])))

currentMaxCapacity = 0
currentBinCapacity = [0] * K

solution = []

def CheckBinStoreAll():
    global currentBinCapacity
    for i in range(K):
        if(currentBinCapacity[i] < LowerAndUpperBounds[i][0] or currentBinCapacity[i] > LowerAndUpperBounds[i][1]):
            return False
    return True

def BackTracking(pack, maxCapacity, currentBinStores):
    global currentMaxCapacity, solution  # Declare these as global variables

    if pack == N:
        return

    for i in range(K + 1):
        if(i == K):
            BackTracking(pack + 1, maxCapacity, currentBinStores)
            continue
        if currentBinCapacity[i] + QuatityAndCost[pack][0] > LowerAndUpperBounds[i][1]:
            continue

        currentBinCapacity[i] += QuatityAndCost[pack][0]
        maxCapacity += QuatityAndCost[pack][1]
        currentBinStores.append((pack + 1, i + 1))

        if currentMaxCapacity < maxCapacity and CheckBinStoreAll():
            solution = currentBinStores.copy()
            print(currentBinCapacity)
            currentMaxCapacity = maxCapacity

        BackTracking(pack + 1, maxCapacity, currentBinStores)

        currentBinCapacity[i] -= QuatityAndCost[pack][0]
        maxCapacity -= QuatityAndCost[pack][1]
        currentBinStores.remove((pack + 1, i + 1))

BackTracking(0, 0, [])
print(len(solution))
for i in range(len(solution)):
    print(str(solution[i][0]) + " " + str(solution[i][1]))