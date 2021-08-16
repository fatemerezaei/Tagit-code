
from __future__ import division
import  Interval

#import socks
import socket
import random

import itertools

import math
class FIBIR:
    landa=10# 10 packet for second,
    #intervalLength=1000# each slot is 1 second. so we have 10 packet for each slot in average:)
    content=""
    def __init__(self, markFlowLength):
        self.markFlowLength=markFlowLength
        self.permutationOne=self.getPermFromFile('/home/fatemeh/Dropbox/NFQ/permOne.txt')#self.getPermutations([0,1,2,3,4,5])#(range(self.numberOfSlots))
        self.permutationZero=self.getPermFromFile('/home/fatemeh/Dropbox/NFQ/permZero.txt')#self.getPermutaionZero(self.permutationOne)#self.getPermutations([0,2,4])#(range(self.numberOfSlots))
        self.randSeeds=self.getRandSeeds()
        self.permutationOneZero=self.getPermutations([0,1,2,3,4,5])#self.getPermutationB(self.permutationOne)
        self.permutationZerOne=self.getPermutaionZero(self.permutationOneZero)
        self.deltaIPDs=[]
        self.markIntervals=[]
        self.baseIntervals=[]
        self.jitterCoefficient=1

        self.fingerPrintLoc=[]#change in here, and
        self.fingerPrintLength=markFlowLength
        self.fingerPrint=self.getFingerPrint()[0:markFlowLength]
        #print 'Fingerptint',self.fingerPrint
        self.threshold=0.5
        self.movingThreshold=1#What percent of packets do we move?...
    def getRandSeeds(self):
        seeds=[]
        for k in range(0,len(self.permutationOne)):
            seeds.append(random.randrange(0,5))
        return seeds

    def getPermutationB(self,permuts):
        permutations=list(itertools.permutations([0,1,2,3,4,5], 6))
        permut2=[]
        for j in range(0,len(permuts)):
            permut2.append(permutations[random.randint(0,720)])
    def setJitterCoefficent(self):
        # print "Ddddddddddddd"
        if self.mSlotLength>=10:
            self.jitterCoefficient=4
        elif self.mSlotLength<=5:
            self.jitterCoefficient=1.5
        else:
            self.jitterCoefficient=1




    def calcParameters(self, intervalLength, numberOfSubintervals, numberOfSlots):
        self.intervalLength=intervalLength#T
        self.numberOfSubintervals=numberOfSubintervals#r
        self.numberOfSlots=numberOfSlots#m
        self.subintervalLength=self.intervalLength/self.numberOfSubintervals
        self.mSlotLength=self.intervalLength/(self.numberOfSubintervals*self.numberOfSlots)
        # print self.mSlotLength,"mslot length",self.numberOfSubintervals,self.numberOfSlots,self.intervalLength
    def getPermutaionZero(self,permutations):
        permuts=[]
        for i in range(0,len(permutations)):
            perm=permutations[i]
            l=[]
            for j in range(0,len(perm)):
                #perm(j)=(perm(j)+3) % 6
                l.append((perm[j]+3)%6)#%6

            permuts.append(l)

        #print permutations[0:10],"one"
        #print permuts[0:10],"zero"
        return permuts
    def setMeanSD(self,mean,sd):
        self.meanDelay=mean
        self.sdDeay=sd

    #number of interval
    def setSwirParameter(self,mslot,numberofSubinterval):
        self.numberOfSlots=mslot
        self.numberOfSubintervals=numberofSubinterval
        #self.

    def getDelay(self):
        return self.delay

    def readFromFile(self,path):
         with open(path, 'r') as content_file:
             content = content_file.read()
             return  content
    def setpMove(self,p_move):
        self.movingThreshold=p_move
        self.threshold=p_move/float(2)

    def getTlengthIntervals(self,content):
        numbers=content.split(" ")
        #print len(numbers)
        intervalList=[]
        #print "getTlengthIntervals: ", self.markFlowLength,self.intervalLength
        for i in range(0, self.markFlowLength):
            intervalList.append(Interval.Interval())

        upperBound=self.intervalLength
        i=0
        condition=True
        count=0
        # print self.intervalLength,"ffffffffffffffffffffffffffffff"
        while condition:
            if upperBound==self.intervalLength+self.markFlowLength*self.intervalLength:
                break
            if numbers[i]=='':# this means we are in the end of our file
                break
            if float(numbers[i])<upperBound:
                intervalList[count].append(float(numbers[i]))#????///
                i+=1
            else:
                upperBound+=self.intervalLength
                count+=1

        #self.fingerPrintLoc=self.getFingerPrintLocations(self.baseIntervals)
        al=0
        for i in range(0,len(intervalList)):
             #print intervalList[i].getlen(),"k"
             al+=intervalList[i].getlen()
        #print al,"gallllllllllllllllllllllllllll"
        return intervalList

    def getFingerPrintLocations(self, baseIntervals):
        fingerPrintLocations=[]
        count=0
        for i in range(0,len(baseIntervals)):
            centroid=self.getCentroid(self.baseIntervals[i],0)#3
            for j in range(0, self.numberOfSubintervals):
                #print(type(count),type(centroid))
                fingerPrintLocations.append(self.permutationOne[count][centroid])
                count+=1
        #print(fingerPrintLocations)
        return fingerPrintLocations


    def getPermFromFile(self,path):
        perm=self.readFromFile(path)#()
        permsArray=perm.split(" ")
        print permsArray[0][1]
        return permsArray
        #print perm
    def getPermutations(self, listN,):

        selectedPermutations=[]
        permutations=list(itertools.permutations(listN, len(listN)))
        #print permutations


        for i in range(0, 30000*20):#self.numberOfSubintervals*self.markFlowLength):
            randNumber=random.randrange(0,len(permutations))
            l=[]
            # for k in range(0,len(permutations[randNumber])):
            #     print permutations[randNumber][k]
            selectedPermutations.append(permutations[randNumber])


        #print len(selectedPermutations),"len selected per"
        #print selectedPermutations






        return selectedPermutations


    def getDeltaIPDs(self):
        deltaIPDs=[]
        for i in range(0,len(self.baseIntervals)):
            base=self.baseIntervals[i]
            deltaIPD=0



            for i in range(0,base.getlen()-1):
                deltaIPD+=base.get(i+1)-base.get(i)
            deltaIPDs.append(deltaIPD)
        return deltaIPDs

    def getFingerPrint(self):
        encodedFingerPrint=[]

        encd=self.readFromFile("/home/fatemeh/Dropbox/NFQ/finger.txt")
        encdoed=encd.split(" ")
        for i in range(0,len(encdoed)):
            if self.isfloat(encdoed[i]):
                encodedFingerPrint.append(int(encdoed[i]))



        '''for j in range(0,30):
            encodedFingerPrint.append(random.randrange(0,2))
            #encodedFingerPrint.append(1)
        print "Fingerprint: ",encodedFingerPrint'''


        return  encodedFingerPrint
    def isfloat(self,value):
        try:
            float(value)
            return True
        except ValueError:
            return False
    def decToBinary(self,bin):
        n=len(bin)
        res=0
        for i in range(1,n+1):
            res=res+ int(bin[i-1])*2**(n-i)
        return res
    def insertFingerPrintOnHighRates(self,markIntervalList):
        #We need this for higher rates and high jitters.(for low jitter, we at most have 1 packet in each subinterval)
        #we are just moving 50 precent of the packets
        self.delay=0
        fingerPrint=self.fingerPrint
        numberALlPack=0
        subintervalLength=self.intervalLength/self.numberOfSubintervals
        mslothLength=subintervalLength/self.numberOfSlots


        for i in range(0,len(fingerPrint)):#interval

            value=fingerPrint[i]
            rand=random.randint(0,5)
            inter=markIntervalList[i]
            numberALlPack+=inter.getlen()

            if markIntervalList[i].getlen()==0:#return []#????
                print "Zero Packet"
                continue

            numberOfInterval=math.floor(markIntervalList[i].get(0)/self.intervalLength)
            lowerBound=numberOfInterval*self.intervalLength
            upperBound=lowerBound+subintervalLength

            if value==1:
                for j in range(0,inter.getlen()):

                    lowerBound=numberOfInterval*self.intervalLength
                    upperBound=lowerBound+subintervalLength
                    currentSubinterval=0
                    while(True):

                        if (inter.elements[j]>=lowerBound and inter.elements[j]<upperBound):
                            randomJitt=random.random()
                            #print randomJitt,"ddddddddddddddddddd"
                            #print inter.elements[j]%subintervalLength, inter.elements[j],subintervalLength

                            for k in range(0,self.numberOfSlots):

                                location=int(self.permutationOne[i * self.numberOfSubintervals + currentSubinterval][rand])
                                #print type(location)
                                if inter.get(j)>lowerBound+mslothLength*k and inter.get(j)<lowerBound+mslothLength*(k+1):
                                    if location>k :# and (k==location-1 or k==location-2):
                                        temp=inter.elements[j]%(mslothLength)


                                        distFromSubInterval=inter.elements[j]%subintervalLength
                                        locationOfSelectedSlot=(location)*mslothLength
                                        portionOfDistSubint=distFromSubInterval/locationOfSelectedSlot
                                        #print portionOfDistSubint,'fffffffff'

                                        if portionOfDistSubint>1-2*self.movingThreshold:
                                            inter.elements[j]+=(location-k)*mslothLength+ mslothLength/2-temp+randomJitt

                                        break
                                    elif location<k:

                                        if currentSubinterval!=self.numberOfSubintervals-1 and self.movingThreshold>0.5:#if is added for last subinterval

                                             location2=int(self.permutationOne[i * self.numberOfSubintervals + currentSubinterval + 1][rand])

                                             distFromSubInterval=(inter.elements[j]%subintervalLength)

                                             locationOfSelectedSlot=(location+1)*mslothLength
                                             portionOfDistSubint=(distFromSubInterval-locationOfSelectedSlot)/(subintervalLength-locationOfSelectedSlot)
                                             if portionOfDistSubint>1:

                                                    print portionOfDistSubint, "Bye!",distFromSubInterval,subintervalLength,location2,location
                                             temp=inter.elements[j]%(mslothLength)
                                             if portionOfDistSubint>(1-self.movingThreshold):
                                                 inter.elements[j]+=(self.numberOfSlots-k+location2)*mslothLength+mslothLength/2-temp+randomJitt

                                             break

                            break
                        else:
                            currentSubinterval+=1
                            lowerBound=upperBound
                            upperBound+=subintervalLength

            else:
                for j in range(0,inter.getlen()):
                    randomJitt=random.random()#*self.coeficeient
                    #print randomJitt
                    lowerBound=numberOfInterval*self.intervalLength
                    upperBound=lowerBound+subintervalLength
                    currentSubinterval=0
                    while(True):

                        if (inter.elements[j]>=lowerBound and inter.elements[j]<upperBound):
                            for k in range(0,self.numberOfSlots):

                                location=int(self.permutationZero[i * self.numberOfSubintervals + currentSubinterval][rand])
                                if inter.get(j)>lowerBound+mslothLength*k and inter.get(j)<lowerBound+mslothLength*(k+1):
                                    if location>k :#and (k==location-1 or k==location-2):
                                        temp=inter.elements[j]%(mslothLength)


                                        distFromSubInterval=inter.elements[j]%subintervalLength
                                        locationOfSelectedSlot=(location)*mslothLength
                                        portionOfDistSubint=distFromSubInterval/(locationOfSelectedSlot)

                                        if portionOfDistSubint>1-2*self.movingThreshold:
                                            inter.elements[j]+=(location-k)*mslothLength+ mslothLength/2-temp+randomJitt


                                    elif location<k:


                                        if currentSubinterval!=self.numberOfSubintervals-1 and self.movingThreshold>0.5:#if is added for last subinterval

                                             location2=int(self.permutationZero[i * self.numberOfSubintervals + currentSubinterval + 1][rand])
                                             #distFromSubInterval=inter.elements[j]%((location+1)*mslothLength)#subintervalLength
                                             #print distFromSubInterval
                                             distFromSubInterval=(inter.elements[j]%subintervalLength)
                                             locationOfSelectedSlot=(location+1)*mslothLength

                                             #portionOfDistSubint=(distFromSubInterval-locationOfSelectedSlot)/locationOfSelectedSlot
                                             portionOfDistSubint=(distFromSubInterval-locationOfSelectedSlot)/(subintervalLength-locationOfSelectedSlot)
                                             temp=inter.elements[j]%(mslothLength)
                                             if portionOfDistSubint>1:
                                                print portionOfDistSubint,"Hello!"
                                             if portionOfDistSubint>(1-self.movingThreshold):
                                                 inter.elements[j]+=(self.numberOfSlots-k+location2)*mslothLength+mslothLength/2-temp+randomJitt

                                             break

                                    #break loop
                            break#???# we do not need this?? yes, we need:)

                        else:
                            currentSubinterval+=1
                            lowerBound=upperBound
                            upperBound+=subintervalLength
                markCopy=[]
        for j in range(0,len(markIntervalList)):
            inter=markIntervalList[j]
            markCopy.append([])
            for k in range(0,inter.getlen()):
                markCopy[j].append(inter.elements[k])

        rands=[]

        if mslothLength>0:
            while True:
                p=random.random()/4
                if p<float(mslothLength/2):
                    rands.append(p)
                    break
                #print "ddddddddddddd"
            for j in range(0,len(markIntervalList)):
                inter=markIntervalList[j]

                for k in range(0,inter.getlen()-1):

                    p=markCopy[j][k]
                    p2=markCopy[j][k+1]
                    r1pre=rands[len(rands)-1]
                    r2pre=random.random()/4
                    while True:
                        if p!=p2:
                             rands.append(0)
                             break
                        if r1pre<r2pre and r2pre<float(mslothLength/2):
                            inter.elements[k]+=r1pre
                            inter.elements[k+1]+=r2pre
                            rands.append(r2pre)
                            break
                        #print r1pre,r2pre,rands[0]
                        r2pre=random.random()/4

        return  markIntervalList
    def insertTwoBitAtOnce(self,markIntervalList):

        self.delay=0
        fingerPrint=self.fingerPrint
        numberALlPack=0

        subintervalLength=self.intervalLength/self.numberOfSubintervals
        mslothLength=subintervalLength/self.numberOfSlots
        #print len(fingerPrint)
        count=-1
        for i in xrange(0,len(fingerPrint),2):#interval



            value=fingerPrint[i:i+2]
            #print value
            #print i,"dddddddddddddd", value
            count+=1
            rand=random.randint(0,5)
            #print rand
            inter=markIntervalList[count]

            numberALlPack+=inter.getlen()

            if markIntervalList[count].getlen()==0:#return []#????
                continue

            numberOfInterval=math.floor(markIntervalList[count].get(0)/self.intervalLength)
            lowerBound=numberOfInterval*self.intervalLength
            upperBound=lowerBound+subintervalLength
            inserted=0

            if value==[1,1]:
                for j in range(0,inter.getlen()):

                    lowerBound=numberOfInterval*self.intervalLength
                    upperBound=lowerBound+subintervalLength
                    currentSubinterval=0
                    while(True):

                        if (inter.elements[j]>=lowerBound and inter.elements[j]<upperBound):
                            randomJitt=0#random.random()

                            for k in range(0,self.numberOfSlots):

                                location=self.permutationOne[count * self.numberOfSubintervals + currentSubinterval][rand]
                                if inter.get(j)>lowerBound+mslothLength*k and inter.get(j)<lowerBound+mslothLength*(k+1):
                                    if location>=k:
                                        temp=inter.elements[j]%(mslothLength)
                                        inter.elements[j]+=(location-k)*mslothLength+ mslothLength/2-temp+randomJitt
                                        inserted+=1

                                        break
                                    else:

                                        if currentSubinterval!=self.numberOfSubintervals-1:#if is added for last subinterval
                                             location=self.permutationOne[count * self.numberOfSubintervals + currentSubinterval + 1][rand]
                                             temp=inter.elements[j]%(mslothLength)
                                             inter.elements[j]+=(self.numberOfSlots-k+location)*mslothLength+mslothLength/2-temp+randomJitt
                                             inserted+=1

                                             break
                            break
                        else:
                            currentSubinterval+=1
                            lowerBound=upperBound
                            upperBound+=subintervalLength


            elif value==[0,0]:
                for j in range(0,inter.getlen()):
                    randomJitt=0#random.random()#*self.coeficeient
                    #print randomJitt
                    lowerBound=numberOfInterval*self.intervalLength
                    upperBound=lowerBound+subintervalLength
                    currentSubinterval=0
                    while(True):

                        if (inter.elements[j]>=lowerBound and inter.elements[j]<upperBound):
                            for k in range(0,self.numberOfSlots):

                                location=self.permutationZero[count * self.numberOfSubintervals + currentSubinterval][rand]
                                if inter.get(j)>lowerBound+mslothLength*k and inter.get(j)<lowerBound+mslothLength*(k+1):
                                    if location>=k:
                                        temp=inter.elements[j]%(mslothLength)
                                        inter.elements[j]+=(location-k)*mslothLength+mslothLength/2-temp+randomJitt
                                        inserted+=1
                                        break

                                    else:#if we are in the last interval
                                        if currentSubinterval!=self.numberOfSubintervals-1:#if is added for last subinterval

                                             location=self.permutationZero[count * self.numberOfSubintervals + currentSubinterval + 1][rand]

                                             temp=inter.elements[j]%(mslothLength)
                                             inter.elements[j]+=(self.numberOfSlots-k+location)*mslothLength-temp+mslothLength/2+randomJitt
                                             inserted+=1

                                             break
                                    #break loop
                            break#???# we do not need this?? yes, we need:)

                        else:
                            currentSubinterval+=1
                            lowerBound=upperBound
                            upperBound+=subintervalLength
            elif value==[0,1]:
                for j in range(0,inter.getlen()):
                    randomJitt=0#random.random()#*self.coeficeient
                    #print randomJitt
                    lowerBound=numberOfInterval*self.intervalLength
                    upperBound=lowerBound+subintervalLength
                    currentSubinterval=0
                    while(True):

                        if (inter.elements[j]>=lowerBound and inter.elements[j]<upperBound):
                            for k in range(0,self.numberOfSlots):

                                location=self.permutationZerOne[count * self.numberOfSubintervals + currentSubinterval][rand]
                                if inter.get(j)>lowerBound+mslothLength*k and inter.get(j)<lowerBound+mslothLength*(k+1):
                                    if location>=k:
                                        temp=inter.elements[j]%(mslothLength)
                                        inter.elements[j]+=(location-k)*mslothLength+mslothLength/2-temp+randomJitt
                                        inserted+=1


                                        break

                                    else:#if we are in the last interval
                                        if currentSubinterval!=self.numberOfSubintervals-1:#if is added for last subinterval

                                             location=self.permutationZerOne[count * self.numberOfSubintervals + currentSubinterval + 1][rand]

                                             temp=inter.elements[j]%(mslothLength)
                                             inter.elements[j]+=(self.numberOfSlots-k+location)*mslothLength-temp+mslothLength/2+randomJitt
                                             inserted+=1

                                             break
                                    #break loop
                            break#???# we do not need this?? yes, we need:)

                        else:
                            currentSubinterval+=1
                            lowerBound=upperBound
                            upperBound+=subintervalLength
            elif value==[1,0]:
                #print "sddddddddddd"
                for j in range(0,inter.getlen()):
                    randomJitt=0#random.random()#*self.coeficeient
                    #print randomJitt
                    lowerBound=numberOfInterval*self.intervalLength
                    upperBound=lowerBound+subintervalLength
                    currentSubinterval=0
                    while(True):

                        if (inter.elements[j]>=lowerBound and inter.elements[j]<upperBound):
                            for k in range(0,self.numberOfSlots):

                                location=self.permutationOneZero[count * self.numberOfSubintervals + currentSubinterval][rand]
                                if inter.get(j)>lowerBound+mslothLength*k and inter.get(j)<lowerBound+mslothLength*(k+1):
                                    if location>=k:
                                        temp=inter.elements[j]%(mslothLength)
                                        inter.elements[j]+=(location-k)*mslothLength+mslothLength/2-temp+randomJitt
                                        inserted+=1
                                        break
                                    else:#if we are in the last interval
                                        if currentSubinterval!=self.numberOfSubintervals-1:#if is added for last subinterval
                                             location=self.permutationOneZero[count * self.numberOfSubintervals + currentSubinterval + 1][rand]
                                             temp=inter.elements[j]%(mslothLength)
                                             inter.elements[j]+=(self.numberOfSlots-k+location)*mslothLength-temp+mslothLength/2+randomJitt
                                             inserted+=1
                                             break
                                    #break loop
                            break#???# we do not need this?? yes, we need:)

                        else:
                            currentSubinterval+=1
                            lowerBound=upperBound
                            upperBound+=subintervalLength
            #print inserted,value,inter.getlen()

        return  markIntervalList
    def selectRandomDelayFile(self):

        file="RandomJitters/randomJitte0.txt"
        content=self.readFromFile(file)
        delays=content.split(" ")
        noiseArray=[]

        for j in range(0,len(delays)):
            if self.isfloat(delays[j]):
                noiseArray.append(float(delays[j])*3)
        return noiseArray
    def insertFingerPrint(self,markIntervalList):
        #We need this for higher rates and high jitters.(for low jitter, we at most have 1 packet in each subinterval)
        noiseArray=self.selectRandomDelayFile()
        self.delay=0
        fingerPrint=self.fingerPrint
        numberALlPack=0

        subintervalLength=self.intervalLength/self.numberOfSubintervals
        mslothLength=subintervalLength/self.numberOfSlots

        unFingerpritnALl=[]

        for i in range(0,len(fingerPrint)):#interval
            unFingerprinted=0

            value=fingerPrint[i]
            rand=self.randSeeds[i]#random.randint(0,5)
            inter=markIntervalList[i]
            numberALlPack+=inter.getlen()

            if markIntervalList[i].getlen()==0:#return []#????
                print "dkddfdf"
                continue

            numberOfInterval=math.floor(markIntervalList[i].get(0)/self.intervalLength)
            lowerBound=numberOfInterval*self.intervalLength
            upperBound=lowerBound+subintervalLength
            count=0

            if value==1:
                for j in range(0,inter.getlen()):

                    lowerBound=numberOfInterval*self.intervalLength
                    upperBound=lowerBound+subintervalLength
                    currentSubinterval=0
                    while(True):

                        if (inter.elements[j]>=lowerBound and inter.elements[j]<upperBound):
                            randomJitt=noiseArray[count]#random.random()

                            for k in range(0,self.numberOfSlots):

                                location=int(self.permutationOne[i * self.numberOfSubintervals + currentSubinterval][rand])
                                if inter.get(j)>lowerBound+mslothLength*k and inter.get(j)<lowerBound+mslothLength*(k+1):
                                    if location>=k:
                                        temp=inter.elements[j]%(mslothLength)
                                        #print inter.elements[j],"d",type(location)
                                        inter.elements[j]+=(location-k)*mslothLength+ mslothLength/2-temp+randomJitt

                                        break
                                    else:

                                        if currentSubinterval!=self.numberOfSubintervals-1:#if is added for last subinterval
                                             location=int(self.permutationOne[i * self.numberOfSubintervals + currentSubinterval + 1][rand])
                                             temp=inter.elements[j]%(mslothLength)
                                             inter.elements[j]+=(self.numberOfSlots-k+location)*mslothLength+mslothLength/2-temp+randomJitt

                                             break
                                        else:
                                            unFingerprinted+=1
                            break
                        else:
                            currentSubinterval+=1
                            lowerBound=upperBound
                            upperBound+=subintervalLength
                    count+=1


            else:
                for j in range(0,inter.getlen()):

                    randomJitt=noiseArray[count]#random.random()#*self.coeficeient
                    lowerBound=numberOfInterval*self.intervalLength
                    upperBound=lowerBound+subintervalLength
                    currentSubinterval=0

                    while(True):

                        if (inter.elements[j]>=lowerBound and inter.elements[j]<upperBound):

                            for k in range(0,self.numberOfSlots):

                                location=int(self.permutationZero[i * self.numberOfSubintervals + currentSubinterval][rand])
                                if inter.get(j)>lowerBound+mslothLength*k and inter.get(j)<lowerBound+mslothLength*(k+1):
                                    if location>=k:
                                        temp=inter.elements[j]%(mslothLength)
                                        inter.elements[j]+=(location-k)*mslothLength+mslothLength/2-temp+randomJitt
                                        break

                                    else:#if we are in the last interval
                                        if currentSubinterval!=self.numberOfSubintervals-1:#if is added for last subinterval

                                             location=int(self.permutationZero[i * self.numberOfSubintervals + currentSubinterval + 1][rand])

                                             temp=inter.elements[j]%(mslothLength)
                                             inter.elements[j]+=(self.numberOfSlots-k+location)*mslothLength-temp+mslothLength/2+randomJitt

                                             break
                                        else:
                                            unFingerprinted+=1
                                    #break loop
                            break#???# we do not need this?? yes, we need:)

                        else:
                            currentSubinterval+=1
                            lowerBound=upperBound
                            upperBound+=subintervalLength
                    count+=1

            unFingerpritnALl.append(unFingerprinted)
        allPackets=0
        for k in range(0,len(markIntervalList)):
             allPackets+=markIntervalList[k].getlen()
             # print markIntervalList[k].getlen(),
        # print
        nonFingerprintedPercent=unFingerprinted/allPackets
        # print nonFingerprintedPercent, "None fingeprinted percent"
        # print unFingerpritnALl
        # print "Fingerpint:  "
        # print self.fingerPrint

        #self.threshold=(1-nonFingerprintedPercent)/2

        #print unFingerprinted," Unfingerprinted number of packets", nonFingerprintedPercent


        return  markIntervalList


    def insertFingerPrint_clean(self, markIntervalList):# we have a wrong break
        #print len(markIntervalList)
        self.delay=0
        fingerPrint=self.fingerPrint
        numberALlPack=0

        subintervalLength=self.intervalLength/self.numberOfSubintervals
        mslothLength=subintervalLength/self.numberOfSlots
        #print len(fingerPrint)
        for i in range(0,len(fingerPrint)):#interval
            value=fingerPrint[i]
            rand=random.randint(0,2)#self.getCentroid(self.baseIntervals[i],0)

            inter=markIntervalList[i]

            numberALlPack+=inter.getlen()
            if markIntervalList[i].getlen()==0:#return []#????
                continue

            numberOfInterval=math.floor(markIntervalList[i].get(0)/self.intervalLength)

            lowerBound=numberOfInterval*self.intervalLength
            upperBound=lowerBound+subintervalLength

            for j in range(0,inter.getlen()):

                    lowerBound=numberOfInterval*self.intervalLength
                    upperBound=lowerBound+subintervalLength
                    currentSubinterval=0

                    while(True):

                        if (inter.elements[j]>=lowerBound and inter.elements[j]<upperBound):
                            randomJitt=0
                            for k in range(0,self.numberOfSlots):
                                if value==1:
                                    location=self.permutationOne[i * self.numberOfSubintervals + currentSubinterval][rand]
                                else:
                                    location=self.permutationZero[i * self.numberOfSubintervals + currentSubinterval][rand]

                                if inter.get(j)>lowerBound+mslothLength*k and inter.get(j)<lowerBound+mslothLength*(k+1):

                                    if location>=k:
                                        temp=inter.elements[j]%(mslothLength)
                                        inter.elements[j]+=(location-k)*mslothLength+ mslothLength/2-temp+randomJitt
                                        break
                                    else:
                                        if currentSubinterval!=self.numberOfSubintervals-1:#if is added for last subinterval

                                             if value==1:
                                                location=self.permutationOne[i * self.numberOfSubintervals + currentSubinterval][rand]
                                             else:
                                                location=self.permutationZero[i * self.numberOfSubintervals + currentSubinterval][rand]

                                             temp=inter.elements[j]%(mslothLength)
                                             inter.elements[j]+=(self.numberOfSlots-k+location)*mslothLength+mslothLength/2-temp+randomJitt
                                             break
                            break

                        else:
                            currentSubinterval+=1
                            lowerBound=upperBound
                            upperBound+=subintervalLength

        return  markIntervalList
    def minusOffset(self,markIntervalList,value):
            for i in range(0,len(markIntervalList)):
                for j in range(0,markIntervalList[i].getlen()):
                    markIntervalList[i].elements[j]-=value

    def writeIntervalsToFile(self,mark,name):

        target = open(name, 'w')
        for i in range(0,self.markFlowLength):
                        inter=mark[i]
                        for j in range(0, inter.getlen()):
                            target.write(str(inter.elements[j]))
                            target.write(" ")


    def tryDifferntOffset(self,step,numberOfSteps,markIntervalList):
        extracteds=[]
        portions=[]
        offsets=[]

        for k in range(0,numberOfSteps):
            fileName="/home/fatemeh/firstChina.txt"
            self.minusOffset(markIntervalList,step*k)
            self.writeIntervalsToFile(markIntervalList,fileName)
            con=self.readFromFile(fileName)
            intervals2=self.getTlengthIntervals(con)
            markIntervalList=intervals2[0:self.markFlowLength]
            e=self.extractAllFingerprintBits(markIntervalList)
            self.minusOffset(markIntervalList,-1*step*k)
            overlapN=e[2]
            offsets.append(step*k)
            extracteds.append(e[0])
            portions.append(e[1])

        for k in range(1,numberOfSteps):
            fileName="/home/fatemeh/first1China.txt"
            self.minusOffset(markIntervalList,-1*step*k)
            offsets.append(-1*step*k)
            self.writeIntervalsToFile(markIntervalList,fileName)
            con=self.readFromFile(fileName)
            intervals2=self.getTlengthIntervals(con)
            markIntervalList=intervals2[0:self.markFlowLength]
            e=self.extractAllFingerprintBits(markIntervalList)
            self.minusOffset(markIntervalList,1*step*k)
            extracteds.append(e[0])
            portions.append(e[1])
            overlapN=e[2]

        return [extracteds,portions,overlapN,offsets]


    def extractAllFingerprintBits(self,markIntervalList):
        extracted=[]
        portions=[]
        nums=[]
        appPa=[]
        numberOfBothExtracted=0
        for i in range(0,len(markIntervalList)):
            inter=markIntervalList[i]
            e=self.extractOneFBit(inter,i)
            extracted.append(e[0])
            portions.append(e[1])
            nums.append(e[2])
            appPa.append(e[3])
            if e[4]:
                numberOfBothExtracted+=1

        return [extracted,portions,numberOfBothExtracted]

    def extractOneFBit(self, inter,i):

        fin=[]
        finNumbers=[]
        numCOnes=[]
        allP=[]

        for j in range(0,int(self.numberOfSlots)):#int(self.numberOfSlots/2)):
            e=self.extractRandom(inter, i, rand=j)

            #e=self.extractRandom2bitAtOnce(inter, i, rand=j)
            fin.append(e[0])
            finNumbers.append(e[1])
            numCOnes.append(e[2])

            allP.append(inter.getlen())

        max=0
        index=0
        for j in range(0, len(fin)):
            if finNumbers[j]>max:
                max=finNumbers[j]
                index=j
        bit=fin[index]
        # print finNumbers
        bothExtracted=False
        if 0 in fin and 1 in fin:
            bothExtracted=True
            # print "Both extracted: ", fin,finNumbers, i



        return [bit,finNumbers[index],numCOnes[index],allP[index],bothExtracted]

    def extractRandom2bitAtOnce(self, inter, i, rand):
            if inter.getlen()==0:
                return 0

            counter=0
            numberOfInterval=int(inter.get(0)/self.intervalLength)
            msLotLength=self.intervalLength/(self.numberOfSlots*self.numberOfSubintervals)
            lowerBound=self.intervalLength*numberOfInterval
            upperBound=lowerBound+self.subintervalLength
            numberOfCorrectOnes=0
            numberOfCorrectZeros=0
            currentSubinterval=0
            numberOfCorrectZerOnes=0
            numberOfCorrectOneZeros=0



            for j in range(0,inter.getlen()):
                while(True):
                        if (inter.elements[j]>=lowerBound and inter.elements[j]<upperBound):

                            counter+=1
                            location=self.permutationOne[i * self.numberOfSubintervals + currentSubinterval][rand]
                            if inter.elements[j]>=location*msLotLength+lowerBound \
                                    and inter.elements[j]<lowerBound+(location+1)*msLotLength:
                                numberOfCorrectOnes+=1

                            locSp=self.permutationZero[i * self.numberOfSubintervals + currentSubinterval][rand]



                            if inter.elements[j]>=locSp*msLotLength+lowerBound \
                                    and inter.elements[j]<lowerBound+(locSp+1)*msLotLength:
                                numberOfCorrectZeros+=1

                            location2=self.permutationOneZero[i * self.numberOfSubintervals + currentSubinterval][rand]
                            locSp2=self.permutationZerOne[i * self.numberOfSubintervals + currentSubinterval][rand]

                            if inter.elements[j]>=location2*msLotLength+lowerBound \
                                    and inter.elements[j]<lowerBound+(location2+1)*msLotLength:
                                numberOfCorrectOneZeros+=1

                            if inter.elements[j]>=locSp2*msLotLength+lowerBound \
                                    and inter.elements[j]<lowerBound+(locSp2+1)*msLotLength:
                                numberOfCorrectZerOnes+=1
                            '''lowerBound-=self.subintervalLength#o
                            upperBound-=self.subintervalLength
                            currentSubinterval-=1'''
                            break

                        else:
                            lowerBound=upperBound
                            upperBound+=self.subintervalLength#subintervalLength
                            currentSubinterval+=1
                            if currentSubinterval==self.numberOfSubintervals:#order???
                                currentSubinterval=0
                                break
                            if upperBound>self.markFlowLength*2*self.intervalLength:#???#stupid mistake
                                break


            numberAllPackets=inter.getlen()
            numberOfNulls=numberAllPackets-numberOfCorrectOnes-numberOfCorrectZeros

            difporitonOne=(2*numberOfCorrectOnes-numberAllPackets)/numberAllPackets
            difportionZero=(2*numberOfCorrectZeros-numberAllPackets)/numberAllPackets
            difportionOneZero=(2*numberOfCorrectOneZeros-numberAllPackets)/numberAllPackets
            difportionZeroOne=(2*numberOfCorrectZerOnes-numberAllPackets)/numberAllPackets

            # if difporitonOne>0 or difportionZeroOne>0 or difportionOneZero>0 or difportionZero>0:
            #         print difportionOneZero,difportionZeroOne,difporitonOne,difportionZero,i

            '''if numberOfCorrectOnes>=self.threshold*numberAllPackets:#threshold is not enough
                return [1,numberOfCorrectOnes/numberAllPackets]

            elif numberOfCorrectZeros>=self.threshold*numberAllPackets:
                 return [0,numberOfCorrectZeros/numberAllPackets]'''

            if difporitonOne>=self.threshold:
                return ['11',difporitonOne,numberOfCorrectOnes]
            elif difportionZero>=self.threshold:
                return ['00',difportionZero,numberOfCorrectZeros]
            elif difportionOneZero>=self.threshold:
                return ['10',difportionOneZero,numberOfCorrectOneZeros]
            elif difportionZeroOne>=self.threshold:
                return ['01',difportionZeroOne,numberOfCorrectZerOnes]

            else:
                if numberOfCorrectOnes>numberOfCorrectZeros:
                    correcOneOrZero=numberOfCorrectOnes

                else:
                    correcOneOrZero=numberOfCorrectZeros
                portionNull=(2*correcOneOrZero-numberAllPackets)/numberAllPackets
                return ["N",portionNull,numberOfCorrectOnes]
            #return [1,numberOfCorrectOnes/numberAllPackets,numberOfCorrectOnes]
            #print self.fingerPrint
            #if difporitonOne<0.5:
             #    print numberOfCorrectOnes,numberAllPackets
            #return [1,difporitonOne,numberOfCorrectOnes]

    def extractRandom(self, inter, i, rand):

            if inter.getlen()==0:
                #print "Inter len equal to zero"
                # print "dddddddddddddddddddddddddddddddddddddddd",i

                return ["N",0,0]

            counter=0
            #print rand
            numberOfInterval=int(inter.get(0)/self.intervalLength)
            msLotLength=self.intervalLength/(self.numberOfSlots*self.numberOfSubintervals)
            lowerBound=self.intervalLength*numberOfInterval
            upperBound=lowerBound+self.subintervalLength
            numberOfCorrectOnes=0
            numberOfCorrectZeros=0
            currentSubinterval=0
            arOfCorrectP=[]


            for j in range(0,inter.getlen()):
                while(True):
                        if (inter.elements[j]>=lowerBound and inter.elements[j]<upperBound):

                            counter+=1
                            location=int(self.permutationOne[i * self.numberOfSubintervals + currentSubinterval][rand])
                            if inter.elements[j]>=location*msLotLength+lowerBound \
                                    and inter.elements[j]<lowerBound+(location+1)*msLotLength:
                                numberOfCorrectOnes+=1

                            locSp=int(self.permutationZero[i * self.numberOfSubintervals + currentSubinterval][rand])

                            if inter.elements[j]>=locSp*msLotLength+lowerBound \
                                    and inter.elements[j]<lowerBound+(locSp+1)*msLotLength:
                                numberOfCorrectZeros+=1
                            lowerBound-=2*self.subintervalLength#o
                            upperBound-=2*self.subintervalLength
                            currentSubinterval-=2
                            break

                        else:
                            lowerBound=upperBound
                            upperBound+=self.subintervalLength#subintervalLength
                            currentSubinterval+=1
                            if currentSubinterval==self.numberOfSubintervals:#order???
                                currentSubinterval=0
                                break
                            if upperBound>self.markFlowLength*2*self.intervalLength:#???#stupid mistake
                                break


            numberAllPackets=inter.getlen()
            numberOfNulls=numberAllPackets-numberOfCorrectOnes-numberOfCorrectZeros

            difporitonOne=numberOfCorrectOnes/numberAllPackets#(2*numberOfCorrectOnes-numberAllPackets)/numberAllPackets
            difportionZero=numberOfCorrectZeros/float(numberAllPackets)#(2*numberOfCorrectZeros-numberAllPackets)/numberAllPackets
            # if difporitonOne>0  or difportionZero>0:
            #         print difportionZero,difporitonOne,i
            '''if numberOfCorrectOnes>=self.threshold*numberAllPackets:#threshold is not enough
                return [1,numberOfCorrectOnes/numberAllPackets]

            elif numberOfCorrectZeros>=self.threshold*numberAllPackets:
                 return [0,numberOfCorrectZeros/numberAllPackets]'''
            # print numberOfCorrectOnes,numberOfCorrectZeros,numberAllPackets
            #print difporitonOne,numberOfCorrectOnes,numberOfCorrectZeros,numberAllPackets
            # print self.threshold, "thrrrrrrrrrrrrrrrrsh"
            # print difportionZero,difporitonOne,numberAllPackets,"ddddddddd"
            if difporitonOne>=self.threshold and difporitonOne>difportionZero:
                #print "one",difporitonOne,numberOfCorrectOnes/float(numberAllPackets),numberOfCorrectZeros/float(numberAllPackets)
                return [1,difporitonOne,numberOfCorrectOnes]

            elif difportionZero>=self.threshold:
                #print "zero",difportionZero,numberOfCorrectOnes/float(numberAllPackets),numberOfCorrectZeros/float(numberAllPackets)
                return [0,difportionZero,numberOfCorrectZeros]

            else:
                return ['N',0,0]
                '''if numberOfCorrectOnes>numberOfCorrectZeros:
                    correcOneOrZero=numberOfCorrectOnes

                else:
                    correcOneOrZero=numberOfCorrectZeros
                portionNull=(2*correcOneOrZero-numberAllPackets)/numberAllPackets
                return ["N",portionNull,numberOfCorrectOnes]'''
            #return [1,numberOfCorrectOnes/numberAllPackets,numberOfCorrectOnes]
            #print self.fingerPrint
            #if difporitonOne<0.5:
             #    print numberOfCorrectOnes,numberAllPackets
            #return [1,difporitonOne,numberOfCorrectOnes]


    def extractFingerPrint(self, markIntervalList):

        msLotLength=self.intervalLength/(self.numberOfSlots*self.numberOfSubintervals)
        extractedFingerPrint=[]
        count=0
        allpackets=0
        counter=0
        centroid=0

        for i in range(0, len(markIntervalList)):
            inter=markIntervalList[i]
            allpackets+=inter.getlen()
            if inter.getlen()==0:
                extractedFingerPrint.append(0)
                continue

            numberOfInterval=int(inter.get(0)/self.intervalLength)

            lowerBound=self.intervalLength*numberOfInterval
            upperBound=lowerBound+self.subintervalLength
            numberOfCorrectPackets=0
            numberOfCorrectZeros=0
            currentSubinterval=0
            arOfCorrectP=[]

            for j in range(0,inter.getlen()):
                while(True):
                        if (inter.elements[j]>=lowerBound and inter.elements[j]<upperBound):

                            counter+=1
                            location=self.permutationOne[i * self.numberOfSubintervals + currentSubinterval][centroid]
                            if inter.elements[j]>=location*msLotLength+lowerBound \
                                    and inter.elements[j]<lowerBound+(location+1)*msLotLength:
                                numberOfCorrectPackets+=1

                            locSp=self.permutationZero[i * self.numberOfSubintervals + currentSubinterval][centroid]

                            if inter.elements[j]>=locSp*msLotLength+lowerBound \
                                    and inter.elements[j]<lowerBound+(locSp+1)*msLotLength:
                                numberOfCorrectZeros+=1
                            lowerBound-=self.subintervalLength#o
                            upperBound-=self.subintervalLength
                            currentSubinterval-=1
                            break

                        else:
                            lowerBound=upperBound
                            upperBound+=self.subintervalLength#subintervalLength
                            currentSubinterval+=1
                            if currentSubinterval==self.numberOfSubintervals:#order???
                                currentSubinterval=0
                                break
                            if upperBound>self.markFlowLength*2*self.intervalLength:#???#stupid mistake
                                break
                            count+=1
            numberAllPackets=inter.getlen()
            arOfCorrectP.append(numberOfCorrectPackets)

            arOfCorrectP.append(numberOfCorrectZeros)

            if numberOfCorrectPackets>=self.threshold*numberAllPackets:#threshold is not enough
                extractedFingerPrint.append(1)

            elif numberOfCorrectZeros>=self.threshold*numberAllPackets:
                 extractedFingerPrint.append(0)

            else:
                max=self.findMax(arOfCorrectP)
                if max==0 or max==1:
                    extractedFingerPrint.append(2)
                else:
                    extractedFingerPrint.append(3)# we do not know if it is zero or one
        return  extractedFingerPrint

    def findMax(self,array):
        index=0
        max=array[0]
        for i in range(0, len(array)):
            if max<array[i]:
                max=array[i]
                index=i
        return index

    def addDelayTofFlow(self,markIntervalList,delayArray):

        countOfPakcetsInInterval=0
        count=0
        for j in range(0,len(markIntervalList)):
                count+=markIntervalList[j].getlen()


        # print len(delayArray),"delay",count
        for i in range(0, len(markIntervalList)):
                    for j in range(0,markIntervalList[i].getlen()):
                        markIntervalList[i].elements[j]+=delayArray[countOfPakcetsInInterval]#+50
                        countOfPakcetsInInterval+=1


        for k in range(0,len(markIntervalList)):
            for t in range(0,markIntervalList[k].getlen()):
                for p in range(0,markIntervalList[k].getlen()-1):
                    if markIntervalList[k].elements[p]>markIntervalList[k].elements[p+1]:
                        temp=markIntervalList[k].elements[p]
                        markIntervalList[k].elements[p]=markIntervalList[k].elements[p+1]#+100
                        markIntervalList[k].elements[p+1]=temp


        #let's order the packets.
        countAll=0
        countOrder=0

        for t in range(0,len(markIntervalList)):
                countAll+=(markIntervalList[t].getlen())
                for tt in range(0,markIntervalList[t].getlen()-1):
                    if markIntervalList[t].elements[tt]>markIntervalList[t].elements[tt+1]:
                        countOrder+=1
        #print countOrder,"coutttttttttttttttttttttt"



        return delayArray
    def getNInterval(self,n):
        res=[]
        for i in range(0,self.placesOfBaseIntervals):
            if self.placesOfBaseIntervals[i]==n:
                res.append(i)
                res.append("base")
                return res
        for j in range(0,self.placesOfMrkIntervals):
            if self.placesOfMrkIntervals[j]==n:
                res.append(j)
                res.append("mark")
                return res

    def adjustIntervals(self,intervals):
        counter=[]
        count=0
        for i in range(0, len(intervals)):
            #k=place[i]
            inter=intervals[i]
            numberOfInterval=math.floor(intervals[i].get(0)/self.intervalLength)
            lowerbound=numberOfInterval*self.intervalLength
            upperbound=(numberOfInterval+1)*self.intervalLength
            for j in range(0,inter.getlen()):
                if (inter.elements[j]>=lowerbound and inter.elements[j]<upperbound):
                    pass
                else:
                    k=self.getNInterval(numberOfInterval+1)

                    count+=1
            counter.append(count)
            count=0
    def addNewPacketToInterval(self,k):
        if k[1]=="base":
            inter=self.baseIntervals[k[0]]
        else:
            inter=self.markIntervals[k[0]]

    def compare(self,dec):
        numberOfCorrectPlaces=0
        #print self.fingerPrint,"kkkkkkkkkkkkkkkkk"
        for i in range(0,len(self.fingerPrint)):
            if dec[i]==self.fingerPrint[i]:
                numberOfCorrectPlaces+=1
        return numberOfCorrectPlaces


