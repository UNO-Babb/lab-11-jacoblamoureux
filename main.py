#GroceryStoreSim.py
#Name:
#Date:
#Assignment:

import simpy
import random
eventLog = []
waitingShoppers = []
idleTime = 0

def shopper(env, id):
    arrive = env.now
    items = random.randint(5, 20)
    shoppingTime = items // 3 # shopping takes 1/3 a minute per item.
    yield env.timeout(shoppingTime)
    # join the queue of waiting shoppers
    waitingShoppers.append((id, items, arrive, env.now))

def checker(env):
    global idleTime
    while True:
        while len(waitingShoppers) == 0:
            idleTime += 1
            yield env.timeout(1) # wait a minute and check again

        customer = waitingShoppers.pop(0)
        items = customer[1]
        checkoutTime = items // 40 + 1
        yield env.timeout(checkoutTime)

        eventLog.append((customer[0], customer[1], customer[2], customer[3], env.now))
    
def customerArrival(env):
    customerNumber = 0
    while True:
        customerNumber += 1
        env.process(shopper(env, customerNumber))
        yield env.timeout(1.25) #New shopper every minute and a quarter

def processResults():
    totalWait = 0
    totalShoppers = 0
    longestwait = 0
    shortestwait = 10000

    for e in eventLog:
        waitTime = e[4] - e[3] #depart time - done shopping time
        totalWait += waitTime
        totalShoppers += 1

        if waitTime > longestwait:
            longestwait = waitTime
        
        if waitTime < shortestwait:
            shortestwait = waitTime

    avgWait = totalWait / totalShoppers

    print("The average wait time was %.2f minutes." % avgWait)
    print("The total idle time was %d minutes" % idleTime)
    print("The longest wait time was %.2f minutes" % longestwait)
    print("The shortest wait time was %.2f minutes" % shortestwait)

def main():
    numberCheckers = 1

    env = simpy.Environment()

    env.process(customerArrival(env))
    for i in range(numberCheckers):
        env.process(checker(env))

    env.run(until=180 )
    print("Amount of shoppers remaining in line:", len(waitingShoppers))
    processResults()

if __name__ == '__main__':
    main()