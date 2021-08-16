import random

prevRand=random.random()
for j in range(0,100):
    print prevRand,j,random.random()
    while True:
        currentRand=random.random()
        if prevRand>currentRand:
            continue
        else:
            #print currentRand
            prevRand=currentRand
            break

fileRand=open('rands2.txt','w')
# for k in range(0,)

