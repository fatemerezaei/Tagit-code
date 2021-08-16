from __future__ import division

#import socks

import matplotlib.pyplot as plt
plt.rcParams['xtick.labelsize'] = 40
plt.rcParams['ytick.labelsize']=40
import FingerprintIrland4bit as FIBIR
#from plotPackage import plot,plotJit
from plotPackage import probability2 as FN_prob
#from plotPackage import plot as plot2
import random
#import ExtractFIBIR.ExtractFingerNBEthz
import numpy as np
from scipy import stats
from scipy.stats import ks_2samp
import math
import datetime

fingerprintlength=30

class tesFIBIR:
    def __init__(self):
        #print("d")
        self.mean=0
        # print "hsdddddddddd"

        self.sd=0
        #self.nodes='Swit_Japan'
        #self.nodes='pol_Zeal'

        self.stepSize=3
        self.numberOfSteps=120
        #self.nodes='oregon_rut'
        self.nodes="japan_ethz"
        #self.nodes="temp"
        #self.nodes="rutgers-purdue"#rutgers-purdue
        self.numberOfFingerprinted=0
        self.numberOfNoneFingerprinted=0

    def plotSDM(self):

            extractRate=[]# detecRate
            nOfSD=[]# n of SD

            par=[1000,500,400]
            sd=[1,2,2.5]
            sw=FIBIR.FIBIR(36, 2000, 1000, 5)


            for i in range(0,len(par)):
                #sw=swirl.swirl(36,2880,par[i],3)
                sw.calcParameters(2000,par[i],5)
                #print(sw.numberOfSubintervals,sw.subintervalLength)
                ext=self.detectionRate(par[i],sw)
                correct=0
                all=0
                for j in range(0,len(ext)):
                    all+=ext[j]
                all=all*36# number of all intervals
                #print(all)
                for j in range(0,len(ext)):
                    correct+=j*(ext[j])

                extRate=correct/all
                print(extRate)
                extractRate.append(extRate)
                #print(len(sd))
                #print(i, len(sd))
                nOfSD.append(sd[i])


            # fig = plt.figure()
            # fig.suptitle('Extraction Rate according to slot length for Poland-Newzealand nodes', fontsize=15)
            # plt.plot(nOfSD, extractRate)
            # plt.ylabel("Extraction Rate")
            # plt.xlabel("Slot length/SD")
            # plt.savefig("poll8.eps")
            # plt.show()
    def plotExtractionRateOneInterval(self):
        ext=self.detectionRate(20)
        #we should change the T interval length each time...
        correct=0
        all=0
        for i in range(0,len(ext)):
            all+=ext[i]
        all=all*36# number of all intervals
        for i in range(0,len(ext)):
            correct+=i*(ext[i])
        extRate=correct/all
        print(extRate)#0.93



    def calcMeanDealy(self,des,sw):
        meanAll=0
        meanA=[]
        sdA=[]
        sdAll=0
        meanSD=[]

        for i in range(0,len(des)):
            jitterName=self.nodes+"/jitter"
            desI=des[i]
            jitterName+=str(desI)+".txt"
            contentJitter=sw.readFromFile(jitterName)
            cc=contentJitter.split(" ")
            sdMe=self.calcDelay(cc)
            self.mean=sdMe[0]
            self.sd=sdMe[1]
            meanA.append(self.mean)
            sdA.append(self.sd)
            sdAll+=self.sd
            #print(self.sd)
            meanAll+=sdMe[0]

        meanAll/=len(des)
        sdAll/=len(des)
        print(self.sd, "sd All")
        self.mean=meanAll
        print(meanAll,"meanAll")
        meanSD.append(meanA)
        meanSD.append(sdA)
        return  meanSD

    def calcIPD(self,markIntervalList,sw):
            firstmarks=[]

            for j in range(0,len(sw.markIntervals)):
                for k in range(0,sw.markIntervals[j].getlen()):
                    firstmarks.append(sw.markIntervals[j].elements[k])
            IPD1=[]
            for j in range(0,len(firstmarks)-1):
                IPD1.append(firstmarks[j+1]-firstmarks[j])


    def saveDeltaIPD(self,deltaIPDOut,deltaIPDIn):
        for i in range(0,len(deltaIPDIn)):
            deltaIPDOut.append(deltaIPDIn[i])


    def detectionRate(self,sw):#
        numberOfCorrectP=[]

        ext=[]
        for j in range(0,37):
            ext.append(0)

        array=[]
        print(sw.fingerPrintLength,"fingrprintlength")
        for i in range(0, sw.fingerPrintLength+1):
            numberOfCorrectP.append(0)

            array.append(i)

        numberOfPacketChange=[]
        c=0
        sdmean=0
        des=[]
        for i in range(0,25):
             des.append(i)
        #des=self.extractDesiredInputs(80,120)

        centroidChange=[]
        for i in range(0,32):
            centroidChange.append(0)

        for i in range(0,180):  #
            numberOfPacketChange.append(0)

        mr=self.calcMeanDealy(des)

        print(mr[1], "SD")
        #print(mr)
        print(mr[0], "mean")
        #print("wer")
        #mr=self.calcDelay(des)
        #print(mr)
        #99.99 for pol, 87 for swit
        #self.mean=134#99, 99.5, 100
        fingerprinted=0
        nonFingerprinted=0
        for i in range(0,1):


            fileName='inputS/input'
            fileName2='inputS/input'
            jitterName=self.nodes+"/jitter"

            desI=des[i]
            #print("SD: ",mr[1][i], "delay: ", mr[0][i])
            fileName+=str(desI)+".txt"
            jitterName+=str(desI)+".txt"
            fileName2+=str(desI)+"rec.txt"
            #print("kd")
            content=sw.readFromFile(fileName)
            intervalList=sw.getTlengthIntervals(content)
            markIntervalList=sw.getMarkAndBaseIntervals(intervalList)
            markIntervalList=sw.insertFingerPrint(markIntervalList)
            self.writeIntervalsToFile(sw.baseIntervals,sw.markIntervals,fileName2)


            sw.addDelay(markIntervalList,sw.baseIntervals,jitterName)

            extracted=self.getExtractedFingerprint(desI,fileName2,self.stepSize,self.numberOfSteps)

            numberOfNull=0
            for j in range(0,len(extracted)):
                if extracted[j]==4:
                    numberOfNull+=1
            if numberOfNull>18:#this shows the number of extracted bits in unfigerprinted flow
                ext[sw.compare(extracted)]+=1
                continue

            decoded=sw.decodeFingerPrint(extracted)
            numberOfCorrectP[sw.compareTwoFingerPrint(decoded)]+=1
            ext[sw.compare(extracted)]+=1

        print(self.numberOfFingerprinted, " :Number of Fingerprinted")
        print(self.numberOfNoneFingerprinted, " :Number of Nonefingerprinted")


        n=[]
        for e in range(0,fingerprintlength+1):
            n.append(ext[e])
        print(n)
        # p= plot.plot(n, array, 36+1)
        # p.plotFigure()

        n=[]
        for i in range(0,sw.fingerPrintLength+1):
            n.append(numberOfCorrectP[i])
        #
        # p= plot.plot(n, array, sw.fingerPrintLength+1)
        # p.hist()


        return numberOfCorrectP

    def getExtractedFingerprint(self,desI,fileName2,step,numberOfSteps,sw):


            offsets=[]
            extractedFingers=[]
            numberOfNulls=[]

            for k in range(0, numberOfSteps):
                newMean=self.mean-k*step
                offsets.append(newMean)
                e=self.tryDiffOffsets(fileName2,newMean,desI)
                self.addDelay(sw.baseIntervals,sw.markIntervals,self.mean-k*step)
                extractedFingers.append(e)
                numberOfNull=self.calcNumberOfNuls(e)
                numberOfNulls.append(numberOfNull)

            for k in range(1,numberOfSteps):
                newMean=self.mean+k*step
                offsets.append(newMean)
                e=self.tryDiffOffsets(fileName2,newMean,desI)
                self.addDelay(sw.baseIntervals,sw.markIntervals,self.mean+k*step)
                extractedFingers.append(e)
                numberOfNull=self.calcNumberOfNuls(e)
                numberOfNulls.append(numberOfNull)


            min=36
            subtractValue=self.mean
            selectedFingerprints=[]
            selectedOffsets=[]


            for p in range(0,len(extractedFingers)):

                if numberOfNulls[p]<min:
                    min=numberOfNulls[p]
                    subtractValue=offsets[p]
            #Now we find the extracted bits that have the same number of NULLs

            for p in range(0,len(extractedFingers)):
                if numberOfNulls[p]==min:
                    selectedFingerprints.append(extractedFingers[p])
                    selectedOffsets.append(offsets[p])

            #Now we should just find the best extracted fingerprint
            numberOfZeros=[]
            numberOfOnes=[]
            numberOfTwos=[]
            numberOfThrees=[]
            extracted=[]
            for i in range(0,36):
                numberOfOnes.append(0)
                numberOfZeros.append(0)
                extracted.append(0)
                numberOfTwos.append(0)
                numberOfThrees.append(0)

            for j in range(0,len(selectedFingerprints)):
                for k in range(0, 36):
                    if selectedFingerprints[j][k]==0 :
                        numberOfZeros[k]+=1
                    elif selectedFingerprints[j][k]==1 :
                        numberOfOnes[k]+=1
                    elif selectedFingerprints[j][k]==2:
                        numberOfTwos[k]+=1
                    elif selectedFingerprints[j][k]==3:
                        numberOfThrees[k]+=1

            for j in range(0,36):
                if numberOfZeros[j]>=0.5*len(selectedFingerprints):
                    extracted[j]=0
                elif numberOfOnes[j]>=0.5*len(selectedFingerprints):
                    extracted[j]=1
                else:
                    extracted[j]=4
            nullNum=0
            for j in range(0,len(extracted)):
                if extracted[j]==4:
                    nullNum+=1

            self.tryDiffOffsets(fileName2,subtractValue,desI)

            if nullNum>=18:
                self.numberOfNoneFingerprinted+=1
                return extracted

            else:
                self.numberOfFingerprinted+=1
                for i in range(0,36):
                    if numberOfZeros[i]+numberOfThrees[i]>numberOfOnes[i]+numberOfTwos[i]:
                        extracted[i]=0
                    else:
                        extracted[i]=1
                #print(extracted, " Extracted")#delay , offset

                return extracted


            #following line would change base and mark intervals...

            #self.minusMeanDealy(sw.baseIntervals,sw.markIntervals,self.mean)

            #extracted=extractedFingers[minIndex]

    def calcNumberOfNuls(self,extracted):

            numOfNull=0
            for l in range(0,36):
                 if extracted[l]==2:
                     numOfNull+=1
                     #extracted[l]=1

                 if extracted[l]==3:
                     numOfNull+=1
                     #extracted[l]=0
            return numOfNull


    def tryDiffOffsets(self,fileName2,offset,desI,sw):

            self.minusMeanDealy(sw.baseIntervals,sw.markIntervals,offset)
            fileName2+=str(desI)+"rec"+".txt"
            self.writeIntervalsToFile(sw.baseIntervals,sw.markIntervals,fileName2)
            content2=sw.readFromFile(fileName2)
            intervals2=sw.getTlengthIntervals(content2)
            markIntervalList=sw.getMarkBaseExtraction(intervals2)
            extracted=sw.extractFingerPrint(markIntervalList)#error

            return extracted

    def compareToArray(self,array1,array2):#odd thing
        print(len(array1),len(array2))
        for i in range(0,len(array1)):
             print(array1[i]-array2[i], array1[i], i)
    def addDelay(self,base,mark,amount):
        self.minusMeanDealy(base,mark,-1*amount)

    def minusMeanDealy(self,base,mark,mean):
        for i in range(0,len(base)):
            inte=base[i]
            for j in range(0,inte.getlen()):
                inte.elements[j]-=mean
        for i in range(0,len(mark)):
            inte=mark[i]
            for j in range(0,inte.getlen()):
                inte.elements[j]-=mean
    def writeMark(self,mark,name):
        #print mark[0:30]

        target = open(name, 'w')
        count=-1
        all=0

        for i in range(0,fingerprintlength):

                        inter=mark[i]
                        all+=inter.getlen()

                        for j in range(0, inter.getlen()):
                            #print inter.elements[j]
                            target.write(str(inter.elements[j]))
                            target.write(" ")

        target.close()
        return



    def writeIntervalsToFile(self,base,mark,name,sw):

        placeB=sw.placesOfBaseIntervals
        placeM=sw.placesOfMrkIntervals

        target = open(name, 'w')

        count=-1
        while True:
            found=0
            count+=1
            if count==72:
                target.close()
                break
            for i in range(0,len(placeB)):
                if placeB[i]==count:
                    inter=base[i]
                    found=1
                    for j in range(0, inter.getlen()):
                        target.write(str(inter.elements[j]))
                        target.write("#")
                    break
            if found==0:
                for i in range(0,len(placeM)):
                    if placeM[i]==count:
                        inter=mark[i]
                        for j in range(0, inter.getlen()):
                            target.write(str(inter.elements[j]))
                            target.write("#")
                        break


    def readFromFile(self,path):
         with open(path, 'r') as content_file:
             content = content_file.read()
             return  content

    def extractDesiredInputs(self,limit1,limit2):
        desired=[]

        jitterName="../../WiresahrkParsing/jitterFiles/"+self.nodes+"/jitter"
        average=0

        for i in range(0,100):

            jitterName+=str(i)+".txt"
            contentJitter=self.readFromFile(jitterName)
            cc=contentJitter.split(" ")
            sdMe=self.calcDelay(cc)
            sd=sdMe[1]
            if sd<limit2 and sd>limit1:
                desired.append(i)
                average+=sd

            jitterName="../../WiresahrkParsing/jitterFiles/"+self.nodes+"/jitter"
        #print(average/len(desired), "average")
        return desired

    def calcDelay(self,array):
        delay=[]
        sum=100
        for i in range(0,len(array)-1):
            sum+=float(array[i])
            delay.append(sum)
        mean=self.calcMean(delay)
        sd=self.calcStandardDeviation(delay,mean)
        #print("mean:   ", mean, "SD:    ",sd)
        ar=[]
        ar.append(mean)
        ar.append(sd)
        return ar



    def calcMean(self,array):
        mean=0
        #print(len(array))
        #print(array)
        for i in range(0,len(array)-1):
            mean+=float(array[i])
            #print (mean,array[i])
        mean/=len(array)
        #print(mean)

        return mean
    def calcStandardDeviation(self, array, mean):
        variance=0
        for i in range(0,len(array)-1):
            #variance+=(array[i]-mean)*(array[i]-mean)
            variance+=math.pow(float(array[i])-mean,2)
        variance/=(len(array)-1)
        variance=math.sqrt(variance)
        return variance

    def DelayDiffM(self):
        #20,1000,10,3
        #we will run this for m in range(2,10)
        numberOfSlots=[]
        delayPerM=[]


        for i in range(2,10):
            sw=FIBIR.FIBIR(20, 1000, 10, i)#m is equal to i

            fileName='../inputs/input'
            jitterName="../inputs/inputJitter"


            totalDelay=0
            numberOfPackets=0
            fileName+='3'+".txt"
            jitterName+='3'+".txt"
            intervalList=sw.insertFingerPrint(fileName)
            sw.addJitterToFlow(intervalList,jitterName)
            detected=sw.extractFingerPrint(intervalList)
            for k in range(0,len(intervalList)):
                inter=intervalList[k]
                numberOfPackets+=inter.getlen()

            totalDelay=sw.getDelay()
            delayPerPacket=float(totalDelay/numberOfPackets)
            delayPerM.append(delayPerPacket)
            numberOfSlots.append(i)
            #print(delayPerPacket, "average Delay by fingerPrinting in 1000 flow per packet")

        print(len(numberOfSlots),len(delayPerM))
        p= plot.plot(9, [], sw.markFlowLength)
        p.graphFunction(numberOfSlots,delayPerM)
    def selectDelayRandomly(self, pathToJitter):
        jitterPath=pathToJitter
        delayArray=[]
        jitterContent=self.readFromFile(jitterPath)
        jitters=jitterContent.split(" ")

        randomNumber=random.randrange(0,(770-1)*800)
        selectedJitter=jitters[randomNumber:randomNumber+800]
        delay=0

        for i in range(0,800):
            delay+=float(selectedJitter[i])
            delayArray.append(delay)
        return delayArray

    def devideJitterToFiles(self,numberOffiles,path,nodeName,rate,numberofPacketInFile):
        #path="/home/fatemeh/china2.txt"#"/home/fatemeh/FIBIR/node_timings/ethz/no-finger/jitterAll.txt"#china2 Irland2

        delayArray=[]
        jittercontent=self.readFromFile(path)
        jitters=jittercontent.split("#")
        print len(jitters)
        for i in range(0,numberOffiles):
            delayFiles="/home/fatemeh/allPackets/"+nodeName+"/jitter/"+rate+"/file"+str(i)+".txt"
            file=open(delayFiles,'w')
            #print i,"ii"
            randomNumber=random.randrange(0,(len(jitters)-numberofPacketInFile))
            #print randomNumber
            selectedJitter=jitters[randomNumber:randomNumber+numberofPacketInFile]
            #print len(selectedJitter)
            delay=0
            for i in range(0,numberofPacketInFile):
                delay+=float(selectedJitter[i])
                file.write(str(delay)+" ")
            file.close()



    def getNumbeOfExtractedBits(self,array,fibir):
        extN=0
        for j in range(0,len(array)):
            if array[j] in fibir.messages:
                extN+=1
        return extN
    def getRandomNumber(self,count):
        rands=[]
        for i in range(0,count):
            rand=random.randrange(0,300)
            rands.append(rand)

        target=open("rands.txt",'w')
        for j in range(0,len(rands)):
            target.write(str(rands[j])+" ")
        target.close()
        return rands
        return rands

    def selectRandomDelayFile(self,rate,node,rand):
        #rand=random.randrange(0,300)
        #rand=225
#
        file="/home/fatemeh/allPackets/"+node+"/jitter/"+str(rate)+"/file"+str(rand)+".txt"
        #file="/home/fatemeh/Dropbox/Link to FIBIR/jitters/"+node+"/"+str(rate)+"/file"+str(rand)+".txt"

        #print "File Number: ", rand

        content=self.readFromFile(file)
        delays=content.split(" ")
        delayArray=[]
        #print delays

        for j in range(0,len(delays)):
            if self.isfloat(delays[j]):
                delayArray.append(float(delays[j]))
        print delayArray[0:10]
        mean=self.calcMean(delayArray)
        sd=self.calcStandardDeviation(delayArray,mean)
        print sd, "sd delay"
        return delayArray
    def getTLengthIntForMultFLowAttack(self,array,steps,upperlimit):
        numbers=array
        print len(numbers)
        intervalList=[]
        for i in range(0, upperlimit):
            intervalList.append([])
        upperBound=steps
        i=0
        count=0
        while True:
            if upperBound==upperlimit or i>=len(numbers):
                break
            if float(numbers[i])<upperBound:
                intervalList[count].append(float(numbers[i]))
                #print "ddddddddddddddddddddddddddddd",i,float(numbers[i])
                i+=1
            else:
                upperBound+=steps
                count+=1
        # for k in range(0,len(intervalList)):
        #      if len(intervalList[k])!=0:
        #          print len(intervalList[k]),k

        return intervalList
    def getIPDFromMIList(self,markintervalList):

        timings1=[]
        for i in range(0,len(markintervalList)):
            inter=markintervalList[i]
            for j in range(0,inter.getlen()):
                timings1.append(inter.elements[j])
        IPD=[]
        for k in range(0,len(timings1)-1):
            IPD.append(timings1[k+1]-timings1[k])

        return IPD

    def clientRealTime(self,fibir,slotLength):#This is for extraction of realtime
        arrayX=[]
        IPD1=[]
        IPD2=[]
        for j in range(0,30):
            arrayX.append(j)
        numberOfPckts=[]
        xAxis=[]
        steps=10
        upperLimit=30*200#this give 1 ms
        #upperLimit/=10#this give 10 ms
        for p in range(0,upperLimit):#each 0.2 ms
            numberOfPckts.append(0)
            xAxis.append(steps*p)
        ksResult=0
        ArrayOFNumbers=[]
        numberOfExtracteds=[]
        for i in range(0,31):
            ArrayOFNumbers.append(i)
            numberOfExtracteds.append(0)

        for i in range(0,1):

            fileName="/home/fatemeh/files"+str(i)+".txt"
            #fileName="files/rates/100/input"+str(i)+".txt"

            content=fibir.readFromFile(fileName)

            fibir.calcParameters(intervalLength=2000,numberOfSubintervals=20,numberOfSlots=5)

            intervalList=fibir.getTlengthIntervals(content)
            markIntervalList=intervalList[0:fingerprintlength]#sw.getMarkAndBaseIntervals(intervalList)




            #extracted=fibir.extractAllFingerprintBits(markIntervalList)
            extractedPortion=fibir.tryDifferntOffset(0.01, 100, markIntervalList)
            portions=extractedPortion[1]
            extracteds=extractedPortion[0]
            extractReal=[]

            extracteds2=extracteds
            print extracteds2

            numberOfDetection=[]
            numberOfExtr=[]
            for p in range(0,len(extracteds2)):
                numberOfDetection.append(fibir.compare(extracteds2[p]))
                numberOfExtr.append(self.getNumbeOfExtractedBits(extracteds2[p],fibir))


            index=0
            max=0
            for j in range(0,len(numberOfDetection)):
                if numberOfDetection[j]>max:
                    max=numberOfDetection[j]
                    index=j

            extracted=extracteds2[index]
            portion=portions[index]

            #plt.plot(arrayX,portion,"*-")

            # p=plotJit.ploty()
            # p.plotDIfference(portion,name="Fingerprinted")
            #print extracted, "STD:", stdDelay,"Mean: ", mean,"Index:",i, \
            print "index: ",i , "Number Of detect:",fibir.compare(extracted),"Number of extra: ",self.getNumbeOfExtractedBits(extracted,fibir)
            print "Number of Flow: ",i
            print "finger",fibir.fingerPrint
            numberOfExtracteds[fibir.compare(extracted)]+=1

            #print extracted

        return [numberOfExtracteds]


    def  client(self, fibir,slotLength,rate,node,numberOfSimul,rands):
        path=open("/home/fatemeh/Dropbox/codes/simIrland.txt",'w')
        pathLog=open("/home/fatemeh/Dropbox/Link to FIBIR/Fingerprint/logs/logIrland.txt",'w')
        arrayX=[]
        #print slotLength,"ssssssssssssslot"
        IPD1=[]
        IPD2=[]
        for j in range(0,30):
            arrayX.append(j)
        numberOfPckts=[]
        portionBargraph=[]
        portionBargraphX=[]
        for k in range(0,100):
            portionBargraph.append(0)
            portionBargraphX.append(0.01*k)
        xAxis=[]
        steps=10

        ipds1=[]
        ipds2=[]
        upperLimit=30*200#this give 1 ms
        for p in range(0,upperLimit):#each 0.2 ms
            numberOfPckts.append(0)
            xAxis.append(steps*p)
        ArrayOFNumbers=[]
        numberOfExtracteds=[]
        for i in range(0,31):
            ArrayOFNumbers.append(i)
            numberOfExtracteds.append(0)

        for i in range(0,numberOfSimul):

            fileName="files/inputs/lam10input"+str(i)+".txt"
            fileName="/home/fatemeh/allPackets/Fingerprint/files/rates/"+str(rate)+"/timing"+str(i)+".txt"

            content=fibir.readFromFile(fileName)
            #delayArray=self.selectDelayRandomly("/home/fatemeh/Irland2.txt")#("/home/fatemeh/FIBIR/node_timings/ethz/no-finger/jitterAll.txt")# overhead of reading a big file every time..

            delayArray=self.selectRandomDelayFile(rate=rate,node=node,rand=rands[i])
            print rands[i],"rand",len(delayArray)


            mean=self.calcMean(delayArray)
            stdDelay=self.calcStandardDeviation(delayArray,mean)
            #print "SD OF DELAY: ", stdDelay, "MEAN:  ",mean
            slotLen=self.decideSlotValue(std=stdDelay)#*10
            print mean,stdDelay,"mean sd"


            '''if slotLen>0.3:
                continue'''
            #TODO: Now calc slot Length

            roundSlotLength=slotLength#20#self.getRoundSlotLength(slotLen)


            interLength=1800
            '''if rate!=10:
                interLength=180'''


            numOfSubintervals=self.getNumberOfSubintervals(intervalLength=interLength,numberofSlot=6,slotLength=roundSlotLength)
            fibir.calcParameters(intervalLength=interLength,numberOfSubintervals=numOfSubintervals,numberOfSlots=6)

            intervalList=fibir.getTlengthIntervals(content)
            markIntervalList=intervalList[0:fingerprintlength]#sw.getMarkAndBaseIntervals(intervalList)
            IPD1=self.getIPDFromMIList(markIntervalList)
            ipds1.append(IPD1)
            #fibir.setJitterCoefficent()#this sould be accodring to slot length
            #markIntervalList=fibir.insertFingerPrintOnHighRates(markIntervalList)


            markIntervalList=fibir.insertFingerPrint(markIntervalList)
            countOrder=0
            countAll=0


            IPD2=self.getIPDFromMIList(markIntervalList)
            ipds2.append(IPD2)

            fibir.addDelayTofFlow(markIntervalList, delayArray)

            for t in range(0,len(markIntervalList)):
                countAll+=markIntervalList[t].getlen()
                for tt in range(0,markIntervalList[t].getlen()-1):
                    if markIntervalList[t].elements[tt]>markIntervalList[t].elements[tt+1]:
                        countOrder+=1
            # print countOrder,"countOrder",countAll


            #extracted=fibir.extractAllFingerprintBits(markIntervalList)0.02 200 iralnd

            numberOfSt=int(math.fabs(mean*2/fibir.mSlotLength))+1
            print numberOfSt,"fffffffffffffff",mean
            # print float(fibir.mSlotLength/2),"dddddddddddddd",numberOfSt
            # extractedPortion=fibir.tryDifferntOffset(0.5,210, markIntervalList)
            extractedPortion=fibir.tryDifferntOffset(float(fibir.mSlotLength/4),4*(int(math.fabs(numberOfSt))+1), markIntervalList)
            portions=extractedPortion[1]
            extracteds=extractedPortion[0]

            nPkts=0
            for k in range(0,len(markIntervalList)):
                nPkts+=markIntervalList[k].getlen()
            print nPkts,"nuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuumber of Pktssssssssssssssssssssssss","Rate:  ",rate

            # offsets=extractedPortion[2]
            extractReal=[]
            pathLog.write("rand: "+ str(rands[i])+" index: "+str(i))
            extracteds2=extracteds


            numberOfDetection=[]
            numberOfExtr=[]
            for p in range(0,len(extracteds2)):
                numberOfDetection.append(fibir.compare(extracteds2[p]))
                numberOfExtr.append(self.getNumbeOfExtractedBits(extracteds2[p],fibir))


            index=0
            max=0
            for j in range(0,len(numberOfExtr)):
                if numberOfExtr[j]>max:
                    max=numberOfExtr[j]
                    index=j

            extracted=extracteds2[index]
            portion=portions[index]


            packets=[]
            for u in range(0,len(markIntervalList)):
                for e in range(0,markIntervalList[u].getlen()):
                    packets.append(markIntervalList[u].elements[e])

            for r in range(0,len(portion)):
                for rr in range(0,len(portionBargraph)):
                    #print rr*0.05,(rr+1)*0.05,portion[rr]
                    if portion[r]>=rr*0.01 and portion[r]<(rr+1)*0.01:
                        portionBargraph[rr]+=1



            #plt.plot(arrayX,portion,"*-")
            #plt.plot(arrayX,portion,"*-")

            #p=plotJit.ploty()
            # p.plotDIfference(portion,name="Fingerprinted")
            #print extracted, "STD:", stdDelay,"Mean: ", mean,"Index:",i, \
            print "index: ",i , "Number Of detect:",fibir.compare(extracted),"Number of extra: ",self.getNumbeOfExtractedBits(extracted,fibir), "mean: ",mean,"sd:",stdDelay
            #print "Number of Flow: ",i
            pathLog.write(" Number of detection: "+str(fibir.compare(extracted))+" Slot length: "+str(slotLength)+"\n")
            numberOfExtracteds[fibir.compare(extracted)]+=1

            print "Extracted Fingerprint: ",extracted
            # for j in range(0,len(extracted)):
            #     pathLog.write(str(extracted[j])+" ")
            #pathLog.write(" STD: "+ str(stdDelay)+" Mean: "+ str(mean)+" Index: "+str(i)+ " Number Of Ext: "+str(fibir.compare(extracted))+"\n")
            for j in range(0,len(extracted)):
                path.write(str(extracted[j])+" ")
            path.write("\n")
        #self.barGraph(numberOfPckts)

        #plt.plot(portionBargraphX,portionBargraph)
        #plt.show()
        #self.barGraph(portionBargraph)
        #pl=plot2.plot(numberOfExtracteds,ArrayOFNumbers,31)
        #self.plotFigure(plt)

        path.close()
        pathLog.close()
        return [ipds1,ipds2,numberOfExtracteds]
    def plotFigure(self,plt):
        plt.xlabel("i's interval")
        #plt.ylabel("Fraction of packets in selected slots")
        plt.ylabel("Fraction of packets in selected slots")
        plt.ylim(0,1)
        plt.yticks(np.arange(0,1.1,0.1))
        plt.title("Result on 100 Fingerprinted flow")
        plt.show()


    def isfloat(self,value):
        #print value,"D("
        try:
            float(value)
            return True
        except ValueError:
            return False
    def writeFile2(self,fileName,array):
        #print array

        target=open(fileName,"w")
        #print array
        for i in range(0,len(array)):
            #print array[i]
            if self.isfloat(array[i]):
                target.write(str(math.fabs(array[i]))+"#")
            else:
                print array[i],"sd"
        target.close()
    def writeFile(self,fileName,array):

        target=open(fileName,"w")
        for i in range(0,len(array)):
                target.write(str(array[i])+"#")
        target.close()

    def saveSystemParameters(self, fibir):
        fingerprint=fibir.fingerPrint
        permutations=fibir.permutationOne
        #print petryDiffOffsetsrmutations
        fingrprint=fibir.fingerPrint
        print len(fingerprint)
        # baseLocFileName="base.txt"
        # markLocFileName="mark.txt"
        permutationsFileNmae="files/param_2/permutations"+".txt"
        fingerprintName="files/param_2/fingerprintFCode.txt"
        # self.writeFile(baseLocFileName,baseLoc)
        # self.writeFile(markLocFileName,markLoc)
        self.writeFile(permutationsFileNmae,permutations)
        self.writeFile(fingerprintName,fingerprint)

    def Kolmogrov_Smirov(self,dist1,dist2):
        test_stat=ks_2samp(dist1,dist2)
        print test_stat, "Kolmogorov test result:"
        return test_stat([0])
    def decideSlotValue(self,std):

        prob=FN_prob.porbability()
        slotLength=prob.decideSlotLengthAccodringToFN(sd=std)
        #print "Decided Slot Length:",slotLength
        return slotLength
    def getRoundSlotLength(self,slotLength):
        return slotLength
    def getNumberOfSubintervals(self,intervalLength,numberofSlot,slotLength):
        numberOfSubintervals=int(intervalLength/(numberofSlot*slotLength)+0.000000001)
        print numberOfSubintervals, "number of subintervals",intervalLength,numberofSlot,slotLength,intervalLength/(numberofSlot*slotLength)
        return numberOfSubintervals
    def MainKSTest(self):

        FIB=FIBIR.FIBIR(markFlowLength=30,nBits=4)
        allslotLength=[1,5,10,20,30,40,50,60]#[1,2,5,10,20]
        numberOFPackets=[]
        randsContent=self.readFromFile('rands.txt')#self.getRandomNumber(100)
        randArray=randsContent.split(" ")
        rands=[]
        for k in range(0,len(randArray)-1):
            rands.append(int(randArray[k]))
        nSimul=10

        slot='Slot length='
        lineType=['*-',"s-","o-","^-",'*--',"s--","o--","^--"]
        lengend=[slot+'1ms',slot+'5ms',slot+'10ms',slot+'20ms',slot+'30ms',slot+'40ms',slot+'50ms',slot+'60ms']
        ksResults=[]
        for j in range(1,10):
            numberOFPackets.append(j*50)
        for i in range(0,len(allslotLength)):
            IPD1,IPD2,ext=self.client(fibir=FIB,slotLength=allslotLength[i],rate='10',node="ETHZ",numberOfSimul=nSimul,rands=rands)
            print len(IPD1),len(IPD2)
            ksResults.append([])
            for p in range(0,nSimul):
                sum=0
                for j in range(0,9):
                    ks=ks_2samp(IPD1[p][j*50:(j+1)*50], IPD2[p][j*50:(j+1)*50])
                    sum+=ks[0]
                ksResults[i].append(sum/nSimul)

        for i in range(0,len(allslotLength)):
            #
            plt.plot(numberOFPackets,ksResults[i],lineType[i],lw='2' )

        plt.legend(lengend,fontsize=36)


        plt.ylabel('K-S test difference',fontsize=36)
        plt.ylim(0,1)
        plt.xlabel('Number of packets (n)',fontsize=36)
        plt.show()
    def MainExtrSlot(self):


        FIB=FIBIR.FIBIR(markFlowLength=30,nBits=5)
        randsContent=self.readFromFile('rands.txt')#self.getRandomNumber(100)
        randArray=randsContent.split(" ")
        rands=[]
        for k in range(0,len(randArray)-1):
            rands.append(int(randArray[k]))

        numberOfSimu=5
        allslotLength=[10,20]#[0.1,0.2,0.3,0.4,0.5,1]#,1,2]#,5,10,20]
        #allslotLength=[5,10,15,20,25,30,35,40,50]#,60,80,100,120,140,160,180,200]
        #allslotLength=[10,20,30,40,50,60,70,80,90]#T=2*1800?
        rates=[10]#,100,200]#,100,200]#,100,200]#,100,200]
        landa="Rate="
        lineType=["*-","s-",'o-']
        lengend=[landa+'10pkt/sec',landa+'100pkt/sec',landa+'200pkt/sec']


        #slot='slot length='
        #lengend=[slot+'1ms',slot+'2ms',slot+'5ms',slot+'10ms',slot+'20ms']
        for j in range(0,len(rates)):

            extRates=[]
            stds=[]
            std=0
            for i in range(0,len(allslotLength)):
                print float(allslotLength[i]/2),"half of slot"
                #print i,j, len(allslotLength), len(rates)
                IPD1,IPD2,extr=self.client(fibir=FIB,slotLength=allslotLength[i],rate=rates[j],node="irland",numberOfSimul=numberOfSimu,rands=rands)


                sum=0

                for k in range(0,len(extr)):
                    sum+=extr[k]*k
                sum/=float((len(extr)-1)*numberOfSimu)
                extRates.append(sum)
                #print sum,"lksuuuuuuuuum"
                for k in range(0,len(extr)):
                    std+=math.pow(((k/float(len(extr)-1))-sum),2)*extr[k]
                    #print std,"llllllllllllllll",extr[k],sum,float(k/float(len(extr)-1)),math.pow(((float(k/float(len(extr)-1))-sum)),2)*extr[k],math.pow(((float(k/float(len(extr)-1))-sum)),2)
                std/=float(numberOfSimu)
                std=float(math.sqrt(std))
                #print std,'stddddd'
                stds.append(std)


            #plt.plot(allslotLength,extRates,lineType[j],lw='2')
            plt.errorbar(allslotLength,extRates,lw='4',yerr=stds, fmt=lineType[j])

        plt.legend(lengend,fontsize=45,loc=4)
        #plt.title('Extraction rate according to the slot length for Amherst-Irland',fontsize=45)
        plt.ylabel('Extraction rate',fontsize=45)
        plt.ylim(0,1)
        #yticks=np.
        plt.yticks(np.arange(0,1.1,0.1))
        plt.xlabel('Slot length (ms)',fontsize=45)
        plt.show()

    def Main(self):
        randsContent=self.readFromFile('rands.txt')#self.getRandomNumber(100)
        randArray=randsContent.split(" ")
        rands=[]
        for k in range(0,len(randArray)):
            rands.append(int(randArray[k]))
        print "len rands",len(rands),rands[len(rands)-1]
        FIB=FIBIR.FIBIR(markFlowLength=30,nBits=4)#(self, fibir,slotLength,rate,node,numberOfSimul,rands):
        self.client(fibir=FIB,slotLength=5,rate=10,node="irland",numberOfSimul=100,rands=rands)


    def ks_pMove(self):
        FIB=FIBIR.FIBIR(markFlowLength=30,nBits=4)
        moves=[0.2,0.4,0.6,0.8,1]
        rates=[10,100,200]
        nSimul=10
        landa="Rate="
        lineType=["*-","s-","o-"]#,"t-"]
        lengend=[landa+'10pkt/sec',landa+'100pkt/sec',landa+'200pkt/sec']

        randsContent=self.readFromFile('rands.txt')#self.getRandomNumber(100)
        randArray=randsContent.split(" ")
        rands=[]

        for k in range(0,len(randArray)-1):
            rands.append(int(randArray[k]))

        for j in range(0,len(rates)):
            ksResults=[]
            stds=[]

            for i in range(0,len(moves)):
                FIB.setpMove(moves[i])
                kss=[]
                IPD1,IPD2,extr=self.client(fibir=FIB,slotLength=0.5,rate=rates[j],node="irland",numberOfSimul=nSimul,rands=rands)
                sum=0
                std=0
                for r in range(0, nSimul):

                    ks=ks_2samp(IPD1[r], IPD2[r])
                    sum+=ks[0]
                    kss.append(ks[0])
                    print ks[0],sum
                sum/=nSimul


                ksResults.append(sum)
                for k in range(0,nSimul):
                    std+=math.pow((kss[k]-sum),2)#*ksResults[k]
                    #print math.pow(((k/float(len(kss)-1))-sum),2),"powr two"

                    #print std,"llllllllllllllll",extr[k],sum,float(k/float(len(extr)-1)),math.pow(((float(k/float(len(extr)-1))-sum)),2)*extr[k],math.pow(((float(k/float(len(extr)-1))-sum)),2)
                std/=float(nSimul)
                std=float(math.sqrt(std))
                print std,"STTTTTTTTTTTTTTD"
                #print std,'stddddd'
                stds.append(std)

            #plt.plot(moves,ksResults,lineType[j],lw='4')
            plt.errorbar(moves,ksResults,lw='4',yerr=stds, fmt=lineType[j])
        plt.legend(lengend,fontsize=36,loc=2)
        plt.xlabel("R_move",fontsize=36)
        plt.ylabel("KS Difference",fontsize=36)
        plt.ylim(0,1)
        plt.yticks(np.arange(0,1.1,0.1))
        plt.title("KS difference according to different R_move",fontsize=36)
        plt.show()



    def extractionRate_pMove(self):
        FIB=FIBIR.FIBIR(markFlowLength=30,nBits=4)
        moves=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
        realMove=[]
        for j in range(0,len(moves)):
             realMove.append(float(moves[j]/2))

        numberOfSimu=100
        rates=[10,100,200]#,200]
        landa="Rate="
        lineType=["*-","s-","o-"]
        lengend=[landa+'10pkt/sec',landa+'100pkt/sec',landa+'200pkt/sec']
        randsContent=self.readFromFile('rands.txt')#self.getRandomNumber(100)
        randArray=randsContent.split(" ")
        rands=[]
        for k in range(0,len(randArray)):
            rands.append(int(randArray[k]))
        for j in range(0,len(rates)):
            extRates=[]
            stds=[]


            for i in range(0,len(moves)):
                FIB.setpMove(moves[i])
                IPD1,IPD2,extr=self.client(fibir=FIB,slotLength=0.5,rate=rates[j],node="irland",numberOfSimul=numberOfSimu,rands=rands)
                sum=0
                std=0
                for t in range(0,len(extr)):
                    sum+=extr[t]*t
                sum/=float(len(extr)*numberOfSimu)

                for k in range(0,len(extr)):
                    std+=math.pow(((k/float(len(extr)-1))-sum),2)*extr[k]
                    #print std,"llllllllllllllll",extr[k],sum,float(k/float(len(extr)-1)),math.pow(((float(k/float(len(extr)-1))-sum)),2)*extr[k],math.pow(((float(k/float(len(extr)-1))-sum)),2)
                std/=float(numberOfSimu)
                std=float(math.sqrt(std))
                #print std,'stddddd'
                stds.append(std)
                extRates.append(sum)



            plt.errorbar(moves,extRates,lw='4',yerr=stds, fmt=lineType[j])




            #plt.plot(moves,extRates,lineType[j],lw='2')#
        plt.legend(lengend,fontsize=36,loc=2)
        plt.xlabel("R_move",fontsize=36)
        plt.ylabel("Extraction Rate",fontsize=36)
        plt.title("Extraction Rate for different R_move",fontsize=36)
        plt.yticks(np.arange(0,1.1,0.1))
        plt.ylim(0,1)
        plt.show()



    def barGraph(self,numberOfPackets):
        print numberOfPackets,"numer"
        N = len(numberOfPackets)
        menMeans = numberOfPackets[0:N]#[20, 35, 30, 35, 27]
        print len(menMeans),"lllllllllllllllllllll"
        #menStd = (1, 1, 1, 1, 1)
        ind = np.arange(N)  # the x locations for the groups
        width = 0.5      # the width of the bars
        fig, ax = plt.subplots()
        #fig.ylim(0,5)
        rects1 = ax.bar(ind, numberOfPackets, width, color='black',edgecolor='black')

# add some text for labels, title and axes ticks
        #ax.set_ylabel('Scores')

#ax.ylim(0,100)
        #ax.set_title('Hist')
        #ax.set_xticks(ind + width)
        #ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))

        def autolabel(rects):
    # attach some text labels
            for rect in rects:
                height = rect.get_height()
                # ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                #         '%d' % int(height),
                #         ha='center', va='bottom')

        autolabel(rects1)
        #plt.yticks(np.arange(0,1.1,0.1))
        plt.xticks(np.arange(0,101,10))
        #plt.title("Cumulative extraction rate for intervals over 100 fingerprinted flow (30*100 interval)",fontsize=36)
        plt.xlabel("Extraction rate",fontsize=36)
        plt.ylabel("Number of intervals",fontsize=36)
        plt.xlim(0,100)


        plt.ylim(0,200)
        plt.show()
    def finPermutations(self):
        selectedPermutations=[]
        permutations=list(itertools.permutations([0,1,2,3,4,5], 6))
        #print permutations


        for i in range(0, 30000*20):#self.numberOfSubintervals*self.markFlowLength):
            randNumber=random.randrange(0,len(permutations))
            selectedPermutations.append(permutations[randNumber])
        print selectedPermutations[0:10]
        return selectedPermutations
    def divideIPDs(self,path,numberOfPktsPerFile,rate):
        allIPDs=self.readFromFile(path)
        allIPDs=allIPDs.split(" ")


        for i in range(0,100):
            target=open("files/rates/"+str(rate)+"/timings"+str(i)+".txt","w")
            rand=random.randrange(0,len(allIPDs)-numberOfPktsPerFile)
            ipds=allIPDs[rand:rand+numberOfPktsPerFile]
            timings=[]
            initialTime=0
            timings.append(initialTime)
            for j in range(0,len(ipds)):
                initialTime+=float(ipds[j])
                timings.append(initialTime)
            for j in range(0,len(timings)):
                target.write(str(timings[j])+" ")
            target.close()


import itertools
#Overhead is for permutation functions
# 10682
tes=tesFIBIR()
# tes.devideJitterToFiles(1000,"/home/fatemeh/allPackets/irland/jitter/10/all.txt","irland","10",numberofPacketInFile=8000)
# tes.MainKSTest()
tes.MainExtrSlot()


#delayArray=tes.selectRandomDelayFile(rate=["N",correctPlaces[maxIndex]/numberAllPackets,0]100,node='irland')
#tes.devideJitterToFiles(400)
#tes.Main()
#tes.ks_pMove()
#print "hey youuuuuuuuuuuuu"
#tes.extractionRate_pMove()
#tes.divideIPDs("files/rates/input10.txt",600,rate=10)

#tes=tesFIBIR()
#(self,numberOffiles,path,nodeName,rate,numberofPacketInFile)
#tes.devideJitterToFiles(1000,"/home/fatemeh/allPackets/"+"irland"+"/jitter/"+"10"+"/all.txt","irland","10",800)
#tes.Main()
#tes.barGraph()
#TODO work on K_S Test


