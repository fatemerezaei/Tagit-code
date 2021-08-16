
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
    def __init__(self, markFlowLength,nBits):
        self.markFlowLength=markFlowLength

        self.allPermuts=[]
        self.numberOfEmbededBits=nBits
        for j in range(0,int(math.pow(2,self.numberOfEmbededBits))):
            permut=self.getPermutations([0, 1, 2, 3, 4, 5])
        self.jitterCoef=2
        '''self.permutA=self.getPermutations([0, 1, 2, 3, 4, 5])#(range(self.numberOfSlots))
        self.permutB=self.getPermutations([0, 1, 2, 3, 4, 5])#self.getPermutations([0,2,4])#(range(self.numberOfSlots))
        self.permutC=self.getPermutations([0, 1, 2, 3, 4, 5])#self.getPermutationB(self.permutationOne)
        self.permutD=self.getPermutations([0, 1, 2, 3, 4, 5])
        self.permutE=self.getPermutations([0, 1, 2, 3, 4, 5])
        self.permutF=self.getPermutations([0, 1, 2, 3, 4, 5])
        self.permutG=self.getPermutations([0, 1, 2, 3, 4, 5])
        self.permutH=self.getPermutations([0, 1, 2, 3, 4, 5])


        self.permutAA=self.getPermutations([0, 1, 2, 3, 4, 5])#(range(self.numberOfSlots))
        self.permutBB=self.getPermutations([0, 1, 2, 3, 4, 5])#self.getPermutations([0,2,4])#(range(self.numberOfSlots))
        self.permutCC=self.getPermutations([0, 1, 2, 3, 4, 5])#self.getPermutationB(self.permutationOne)
        self.permutDD=self.getPermutations([0, 1, 2, 3, 4, 5])
        self.permutEE=self.getPermutations([0, 1, 2, 3, 4, 5])
        self.permutFF=self.getPermutations([0, 1, 2, 3, 4, 5])
        self.permutGG=self.getPermutations([0, 1, 2, 3, 4, 5])
        self.permutHH=self.getPermutations([0, 1, 2, 3, 4, 5])'''





        self.messages=[]#['A',"B","C","D","E","F","G","H",'AA',"BB","CC","DD","EE","FF","GG","HH"]
        for j in range(0,int(math.pow(2,self.numberOfEmbededBits))):
            self.messages.append(str(j))


        self.deltaIPDs=[]
        self.markIntervals=[]
        self.baseIntervals=[]

        self.fingerPrintLoc=[]#change in here, and
        self.fingerPrintLength=markFlowLength
        self.fingerPrint=self.getFingerPrint()[0:markFlowLength]
        #print 'Fingerptint',self.fingerPrint
        self.rands=self.getRands()
        self.threshold=0.5
        self.movingThreshold=1#What percent of packets do we move?...
    def getRands(self):
        rands=[]
        for k in range(0,self.fingerPrintLength):
            rands.append(random.randrange(0,5))
        return rands

    def getPermutationB(self,permuts):
        permutations=list(itertools.permutations([0,1,2,3,4,5], 6))
        permut2=[]
        for j in range(0,len(permuts)):
            permut2.append(permutations[random.randint(0,720)])
    def setJitterCoeficent(self):
        if self.mSlotLength>=10:
            self.jitterCoef=2.5
        elif self.mSlotLength<=5:
            self.jitterCoef=1.5
        else:
            self.jitterCoef=1


    def calcParameters(self, intervalLength, numberOfSubintervals, numberOfSlots):
        self.intervalLength=intervalLength#T
        self.numberOfSubintervals=numberOfSubintervals#r
        self.numberOfSlots=numberOfSlots#m
        self.subintervalLength=self.intervalLength/self.numberOfSubintervals
        self.mSlotLength=self.intervalLength/(self.numberOfSubintervals*self.numberOfSlots)
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

    def getTlengthIntervals(self,content):
        numbers=content.split(" ")#[:-1]


        #print len(numbers)
        intervalList=[]
        multiple=1
        #print "getTlengthIntervals: ", self.markFlowLength,self.intervalLength
        for i in range(0, self.markFlowLength*multiple):
            intervalList.append(Interval.Interval())

        upperBound=self.intervalLength
        i=0
        condition=True
        count=0

        while i< len(numbers):
	    #print(count)
            if upperBound==self.intervalLength+self.markFlowLength*multiple*self.intervalLength:
                break
            if numbers[i]=='' or numbers[i]=='\n':# this means we are in the end of our file
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
                fingerPrintLocations.append(self.permutA[count][centroid])
                count+=1
        #print(fingerPrintLocations)
        return fingerPrintLocations



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
        self.allPermuts.append(selectedPermutations)
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

        for j in range(0,30):
            encodedFingerPrint.append(self.messages[random.randrange(0,int(math.pow(2,self.numberOfEmbededBits)))])

        print "Fingerprint: ", encodedFingerPrint
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
        #print self.movingThreshold," Threshold of moving packets"
        self.delay=0
        fingerPrint=self.fingerPrint
        numberALlPack=0
        subintervalLength=self.intervalLength/self.numberOfSubintervals
        mslothLength=subintervalLength/self.numberOfSlots
        unFinger=0
        fingerP=0
        rands=[0]*len(fingerPrint)
        for k in range(0,len(rands)):
            rands[k]=random.randint(0,5)

        for i in range(0,len(fingerPrint)):#interval


            value=fingerPrint[i]
            rand=random.randrange(0,5)
            inter=markIntervalList[i]
            numberALlPack+=inter.getlen()

            if markIntervalList[i].getlen()==0:#return []#????
                continue

            numberOfInterval=math.floor(markIntervalList[i].get(0)/self.intervalLength)
            lowerBound=numberOfInterval*self.intervalLength
            upperBound=lowerBound+subintervalLength

            for e in range(0,len(self.messages)):
                if value==self.messages[e]:
                    permut=self.allPermuts[e]

            # if value==1:
            for j in range(0,inter.getlen()):

                    lowerBound=numberOfInterval*self.intervalLength
                    upperBound=lowerBound+subintervalLength
                    currentSubinterval=0
                    while(currentSubinterval!=6):
                        #print(j, 'ffffffff',currentSubinterval)

                        if (inter.elements[j]>=lowerBound and inter.elements[j]<upperBound):
                            randomJitt=random.random()*4000

                            for k in range(0,self.numberOfSlots):

                                location=permut[i * self.numberOfSubintervals + currentSubinterval][rand]
                                if inter.get(j)>lowerBound+mslothLength*k and inter.get(j)<lowerBound+mslothLength*(k+1):
                                    if location>k:# and (k==location-1 or k==location-2):
                                        temp=inter.elements[j]%(mslothLength)
                                        distFromSubInterval=inter.elements[j]%subintervalLength
                                        locationDistFromSubInterval=(location)*mslothLength
                                        portionOfDistSubint=(-distFromSubInterval+locationDistFromSubInterval)/subintervalLength
                                        # print portionOfDistSubint, "first"

                                        if portionOfDistSubint>(1-2*self.movingThreshold)/2:
                                            # print portionOfDistSubint," Fingerpitnted in first"
                                            inter.elements[j]+=(location-k)*mslothLength#+ mslothLength/2-temp+randomJitt
                                            fingerP+=1
                                        else:
                                            unFinger+=1

                                        break
                                    else:

                                        if currentSubinterval!=self.numberOfSubintervals-1:#if is added for last subinterval

                                             location2=permut[i * self.numberOfSubintervals + currentSubinterval + 1][rand]

                                             endOfSubinterval=(self.numberOfSlots)*mslothLength
                                             pktDisFromSubinterval=inter.elements[j]%subintervalLength
                                             portionFromEndOfSubinterval=pktDisFromSubinterval/float(endOfSubinterval)
                                             # print portionFromEndOfSubinterval, "second"


                                             if portionFromEndOfSubinterval<self.movingThreshold and self.movingThreshold>0.5:#math.fabs(2*self.movingThreshold-1) and self.movingThreshold>0.5:
                                                 # print portionFromEndOfSubinterval
                                                 # print "Fingerpitnted in Second"
                                                 inter.elements[j]+=(self.numberOfSlots-k+location2)*mslothLength#+mslothLength/2-temp+randomJitt
                                                 fingerP+=1
                                             else:
                                                 unFinger+=1

                                             break

                            break
                        else:
                            currentSubinterval+=1
                            lowerBound=upperBound
                            upperBound+=subintervalLength
            # print "Number of Unfingerprinted: ", unFinger, "Fingerprinted: ",fingerP

            '''else:
                for j in range(0,inter.getlen()):
                    randomJitt=0#random.random()#*self.coeficeient
                    #print randomJitt
                    lowerBound=numberOfInterval*self.intervalLength
                    upperBound=lowerBound+subintervalLength
                    currentSubinterval=0
                    while(True):

                        if (inter.elements[j]>=lowerBound and inter.elements[j]<upperBound):
                            for k in range(0,self.numberOfSlots):

                                location=self.permutB[i * self.numberOfSubintervals + currentSubinterval][rand]
                                if inter.get(j)>lowerBound+mslothLength*k and inter.get(j)<lowerBound+mslothLength*(k+1):
                                    if location>k :#and (k==location-1 or k==location-2):
                                        temp=inter.elements[j]%(mslothLength)


                                        distFromSubInterval=inter.elements[j]%subintervalLength
                                        locationDistFromSubInterval=(location)*mslothLength
                                        portionOfDistSubint=distFromSubInterval/(locationDistFromSubInterval)

                                        if portionOfDistSubint>1-2*self.movingThreshold:
                                            inter.elements[j]+=(location-k)*mslothLength+ mslothLength/2-temp+randomJitt
                                        break

                                    else:

                                        if currentSubinterval!=self.numberOfSubintervals-1:#if is added for last subinterval

                                             location2=self.permutB[i * self.numberOfSubintervals + currentSubinterval + 1][rand]
                                             #distFromSubInterval=inter.elements[j]%((location+1)*mslothLength)#subintervalLength
                                             distFromSubInterval=mslothLength*self.numberOfSubintervals-(inter.elements[j]%subintervalLength)#-((location+1)*mslothLength)
                                             #print distFromSubInterval
                                             locationDistFromSubInterval=(location+1)*mslothLength

                                             portionOfDistSubint=(distFromSubInterval-locationDistFromSubInterval)/locationDistFromSubInterval
                                             temp=inter.elements[j]%(mslothLength)
                                             #print portionOfDistSubint,"Hello!"
                                             if portionOfDistSubint>1-self.movingThreshold:
                                                 inter.elements[j]+=(self.numberOfSlots-k+location2)*mslothLength+mslothLength/2-temp+randomJitt

                                             break

                                    #break loop
                            break#???# we do not need this?? yes, we need:)

                        else:
                            currentSubinterval+=1
                            lowerBound=upperBound
                            upperBound+=subintervalLength'''
        #print fingerP,unFinger, "Unf Finger"
        #print "Fingerprinted percentage: ", fingerP/(unFinger+fingerP),"rmove: ",self.movingThreshold

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

                                location=self.permutA[count * self.numberOfSubintervals + currentSubinterval][rand]
                                if inter.get(j)>lowerBound+mslothLength*k and inter.get(j)<lowerBound+mslothLength*(k+1):
                                    if location>=k:
                                        temp=inter.elements[j]%(mslothLength)
                                        inter.elements[j]+=(location-k)*mslothLength+ mslothLength/2-temp+randomJitt
                                        inserted+=1

                                        break
                                    else:

                                        if currentSubinterval!=self.numberOfSubintervals-1:#if is added for last subinterval
                                             location=self.permutA[count * self.numberOfSubintervals + currentSubinterval + 1][rand]
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

                                location=self.permutB[count * self.numberOfSubintervals + currentSubinterval][rand]
                                if inter.get(j)>lowerBound+mslothLength*k and inter.get(j)<lowerBound+mslothLength*(k+1):
                                    if location>=k:
                                        temp=inter.elements[j]%(mslothLength)
                                        inter.elements[j]+=(location-k)*mslothLength+mslothLength/2-temp+randomJitt
                                        inserted+=1
                                        break

                                    else:#if we are in the last interval
                                        if currentSubinterval!=self.numberOfSubintervals-1:#if is added for last subinterval

                                             location=self.permutB[count * self.numberOfSubintervals + currentSubinterval + 1][rand]

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

                                location=self.permutD[count * self.numberOfSubintervals + currentSubinterval][rand]
                                if inter.get(j)>lowerBound+mslothLength*k and inter.get(j)<lowerBound+mslothLength*(k+1):
                                    if location>=k:
                                        temp=inter.elements[j]%(mslothLength)
                                        inter.elements[j]+=(location-k)*mslothLength+mslothLength/2-temp+randomJitt
                                        inserted+=1


                                        break

                                    else:#if we are in the last interval
                                        if currentSubinterval!=self.numberOfSubintervals-1:#if is added for last subinterval

                                             location=self.permutD[count * self.numberOfSubintervals + currentSubinterval + 1][rand]

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

                                location=self.permutC[count * self.numberOfSubintervals + currentSubinterval][rand]
                                if inter.get(j)>lowerBound+mslothLength*k and inter.get(j)<lowerBound+mslothLength*(k+1):
                                    if location>=k:
                                        temp=inter.elements[j]%(mslothLength)
                                        inter.elements[j]+=(location-k)*mslothLength+mslothLength/2-temp+randomJitt
                                        inserted+=1
                                        break
                                    else:#if we are in the last interval
                                        if currentSubinterval!=self.numberOfSubintervals-1:#if is added for last subinterval
                                             location=self.permutC[count * self.numberOfSubintervals + currentSubinterval + 1][rand]
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

    def insertFingerPrint(self,markIntervalList):
        #We need this for higher rates and high jitters.(for low jitter, we at most have 1 packet in each subinterval)
        noiseArray=self.selectRandomDelayFile()
        # print "Dfdfdfd"
        self.delay=0
        fingerPrint=self.fingerPrint
        numberALlPack=0

        subintervalLength=self.intervalLength/self.numberOfSubintervals
        mslothLength=subintervalLength/self.numberOfSlots
        nfignerprinted=0
        # print self.allPermuts[0][0:2], "dddfd"
        count=0
        countAll=0
        for i in range(0,len(fingerPrint)):#interval

            value=fingerPrint[i]
            rand=random.randint(0,5)
            inter=markIntervalList[i]
            numberALlPack+=inter.getlen()

            if markIntervalList[i].getlen()==0:#return []#????
                continue
            permut=[]

            for e in range(0,len(self.messages)):
                if value==self.messages[e]:
                    permut=self.allPermuts[e]

            numberOfInterval=math.floor(markIntervalList[i].get(0)/self.intervalLength)


            for j in range(0,inter.getlen()):
                    countAll+=1

                    lowerBound=numberOfInterval*self.intervalLength
                    upperBound=lowerBound+subintervalLength
                    currentSubinterval=0
                    while(True):

                        if (inter.elements[j]>=lowerBound and inter.elements[j]<upperBound):
                            randomJitt=noiseArray[count]*3000#random.random()
                            count+=1

                            for k in range(0,self.numberOfSlots):
                                location=permut[i * self.numberOfSubintervals + currentSubinterval][rand]
                                if inter.get(j)>lowerBound+mslothLength*k and inter.get(j)<lowerBound+mslothLength*(k+1):
                                    if location>=k:
                                        temp=inter.elements[j]%(mslothLength)
                                        inter.elements[j]+=(location-k)*mslothLength+ mslothLength/2-temp+randomJitt
                                        nfignerprinted+=1

                                        break
                                    else:

                                        if currentSubinterval!=self.numberOfSubintervals-1:#if is added for last subinterval
                                             location=permut[i * self.numberOfSubintervals + currentSubinterval + 1][rand]
                                             temp=inter.elements[j]%(mslothLength)
                                             # if self.numberOfSlots-k+location<=12:
                                             inter.elements[j]+=(self.numberOfSlots-k+location)*mslothLength+mslothLength/2-temp+randomJitt
                                             nfignerprinted+=1

                                             break
                            break
                        else:
                            currentSubinterval+=1
                            lowerBound=upperBound
                            upperBound+=subintervalLength



        print "Number of fingerpritned: ",nfignerprinted, "count all: ",countAll
            # for t in range(0,6):
            #
            #     print self.extractRandom(markIntervalList[i],i,rand=t),
            # print

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
                                    location=self.permutA[i * self.numberOfSubintervals + currentSubinterval][rand]
                                else:
                                    location=self.permutB[i * self.numberOfSubintervals + currentSubinterval][rand]

                                if inter.get(j)>lowerBound+mslothLength*k and inter.get(j)<lowerBound+mslothLength*(k+1):

                                    if location>=k:
                                        temp=inter.elements[j]%(mslothLength)
                                        inter.elements[j]+=(location-k)*mslothLength+ mslothLength/2-temp+randomJitt
                                        break
                                    else:
                                        if currentSubinterval!=self.numberOfSubintervals-1:#if is added for last subinterval

                                             if value==1:
                                                location=self.permutA[i * self.numberOfSubintervals + currentSubinterval][rand]
                                             else:
                                                location=self.permutB[i * self.numberOfSubintervals + currentSubinterval][rand]

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


    def tryDifferntOffset(self,step,numberOfSteps,markIntervalList,threshold):
        extracteds=[]
        portions=[]
        #for i in range()
        self.threshold=threshold

        for k in range(0,numberOfSteps):
            fileName="/home/fatemeh/ethz2ks.txt"

            self.minusOffset(markIntervalList,step*k)
            self.writeIntervalsToFile(markIntervalList,fileName)
            con=self.readFromFile(fileName)
            # print con
            intervals2=self.getTlengthIntervals(con)
            markIntervalList=intervals2[0:self.markFlowLength]

            e=self.extractAllFingerprintBits(markIntervalList)
            self.minusOffset(markIntervalList,-1*step*k)

            extracteds.append(e[0])
            portions.append(e[1])

        for k in range(0,numberOfSteps):

            fileName="/home/fatemeh/ethz1ks.txt"
            self.minusOffset(markIntervalList,-1*step*k)
            self.writeIntervalsToFile(markIntervalList,fileName)
            con=self.readFromFile(fileName)
            intervals2=self.getTlengthIntervals(con)

            markIntervalList=intervals2[0:self.markFlowLength]
            e=self.extractAllFingerprintBits(markIntervalList)
            self.minusOffset(markIntervalList,1*step*k)
            extracteds.append(e[0])
            portions.append(e[1])

        return [extracteds,portions]


    def extractAllFingerprintBits(self,markIntervalList):
        extracted=[]
        portions=[]
        nums=[]
        appPa=[]
        for i in range(0,len(markIntervalList)):
            inter=markIntervalList[i]
            e=self.extractOneFBit(inter,i)
            # print e
            extracted.append(e[0])
            portions.append(e[1])
            nums.append(e[2])
            appPa.append(e[3])

        return [extracted,portions]

    def extractOneFBit(self, inter,i):

        fin=[]
        finNumbers=[]
        numCOnes=[]
        allP=[]
        #print inter.getlen()," inter.getlen()"
        for j in range(0,int(self.numberOfSlots)):#int(self.numberOfSlots/2)):
            e=self.extractRandom(inter, i, rand=j)
            # print self.allPermuts[0][0:2], "dddjjjjjjjjjjjjjjfd"


            fin.append(e[0])
            finNumbers.append(e[1])
            numCOnes.append(e[2])
            allP.append(inter.getlen())
        index=0
        max=0

        for i in range(0,int(self.numberOfSlots)):
           if finNumbers[i]>max:
               max=finNumbers[i]
               index=i
        bit=fin[index]
        return [bit,finNumbers[index],numCOnes[index],allP[index]]


        #TODO; in the case we have all the rands
        '''e=self.extractRandom(inter, i, rand=self.rands[i])
        return [e[0],e[1],e[2],inter.getlen()]'''


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
                            location=self.permutA[i * self.numberOfSubintervals + currentSubinterval][rand]
                            if inter.elements[j]>=location*msLotLength+lowerBound \
                                    and inter.elements[j]<lowerBound+(location+1)*msLotLength:
                                numberOfCorrectOnes+=1

                            locSp=self.permutB[i * self.numberOfSubintervals + currentSubinterval][rand]



                            if inter.elements[j]>=locSp*msLotLength+lowerBound \
                                    and inter.elements[j]<lowerBound+(locSp+1)*msLotLength:
                                numberOfCorrectZeros+=1

                            location2=self.permutC[i * self.numberOfSubintervals + currentSubinterval][rand]
                            locSp2=self.permutD[i * self.numberOfSubintervals + currentSubinterval][rand]

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
    def setJitterCoefficent(self):
        # print "Ddddddddddddd"
        if self.mSlotLength>=10:
            self.jitterCoefficient=4
        elif self.mSlotLength<=5:
            self.jitterCoefficient=1.5
        else:
            self.jitterCoefficient=1

    def extractRandom(self, inter, i, rand):

            if inter.getlen()==0:
                # print "ddddddddddddddddddddddd"
                return ["N",0,0]

            counter=0
            numberOfInterval=int(inter.get(0)/self.intervalLength)
            msLotLength=self.intervalLength/(self.numberOfSlots*self.numberOfSubintervals)
            lowerBound=self.intervalLength*numberOfInterval
            upperBound=lowerBound+self.subintervalLength
            correctPlaces=[]

            for k in range(0,int(math.pow(2,self.numberOfEmbededBits))):
                correctPlaces.append(0)
            currentSubinterval=0
            for j in range(0,inter.getlen()):
                while(True):
                        if (inter.elements[j]>=lowerBound and inter.elements[j]<upperBound):
                            counter+=1
                            for p in range(0,int(math.pow(2,self.numberOfEmbededBits))):
                                location=self.allPermuts[p][i * self.numberOfSubintervals + currentSubinterval][rand]
                                if inter.elements[j]>=location*msLotLength+lowerBound \
                                        and inter.elements[j]<lowerBound+(location+1)*msLotLength:
                                    correctPlaces[p]+=1

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
            maxIndex=self.getMax(correctPlaces)
            # print correctPlaces[maxIndex],numberAllPackets
            if correctPlaces[maxIndex]>self.threshold*numberAllPackets:
                return [self.messages[maxIndex],correctPlaces[maxIndex]/numberAllPackets,0]
            else:
                return ["N",0,0]

    def getMax(self,array):
        max=0
        index=0
        for i in range(0,len(array)):
            if array[i]>max:
                max=array[i]
                index=i
        return index

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
                            location=self.permutA[i * self.numberOfSubintervals + currentSubinterval][centroid]
                            if inter.elements[j]>=location*msLotLength+lowerBound \
                                    and inter.elements[j]<lowerBound+(location+1)*msLotLength:
                                numberOfCorrectPackets+=1

                            locSp=self.permutB[i * self.numberOfSubintervals + currentSubinterval][centroid]

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
    def selectRandomDelayFile(self):

        file="RandomJitters/randomJitte0.txt"
        content=self.readFromFile(file)
        delays=content.split(" ")
        noiseArray=[]

        for j in range(0,len(delays)):
            if self.isfloat(delays[j]):
                noiseArray.append(float(delays[j])*2)
        return noiseArray


    def addDelayTofFlow(self,markIntervalList,delayArray):

        countOfPakcetsInInterval=0
        # print len(delayArray), "Lenndd"
        # print delayArray

        for i in range(0, len(markIntervalList)):
                    for j in range(0,markIntervalList[i].getlen()):
                        #print("HI", countOfPakcetsInInterval, i, j,len(markIntervalList), len(delayArray))#('HI', 100, 20, 4,30,100)
                        if countOfPakcetsInInterval == 100: break
                        markIntervalList[i].elements[j]+=delayArray[countOfPakcetsInInterval]
                        countOfPakcetsInInterval+=1

        allPackets=[]
        for k in range(0,len(markIntervalList)):
            for t in range(0,markIntervalList[k].getlen()):
                for p in range(0,markIntervalList[k].getlen()-1):
                    if markIntervalList[k].elements[p]>markIntervalList[k].elements[p+1]:
                        temp=markIntervalList[k].elements[p]
                        markIntervalList[k].elements[p]=markIntervalList[k].elements[p+1]
                        markIntervalList[k].elements[p+1]=temp


        #let's order the packets.
        countAll=0
        countOrder=0

        for t in range(0,len(markIntervalList)):
                countAll+=(markIntervalList[t].getlen())
                for tt in range(0,markIntervalList[t].getlen()-1):
                    if markIntervalList[t].elements[tt]>markIntervalList[t].elements[tt+1]:
                        countOrder+=1
        # print countOrder,"Number of disordered packet"


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
    def setpMove(self,p_move):
        self.movingThreshold=p_move
        self.threshold=p_move/float(2)
    def addNewPacketToInterval(self,k):
        if k[1]=="base":
            inter=self.baseIntervals[k[0]]
        else:
            inter=self.markIntervals[k[0]]

    def compare(self,dec):
        numberOfCorrectPlaces=0
        for i in range(0,len(self.fingerPrint)):
            if dec[i]==self.fingerPrint[i]:
                numberOfCorrectPlaces+=1
        return numberOfCorrectPlaces


