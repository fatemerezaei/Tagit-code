from __future__ import division

#import socks

import matplotlib.pyplot as plt
plt.rcParams['xtick.labelsize'] = 40
plt.rcParams['ytick.labelsize'] =40
import FingerprintEthz2bit as FIBIR
#from plotPackage import plot,plotJit
from plotPackage import probability2 as FN_prob
from plotPackage import plot as plot2
import random
from plotPackage import probability as FN_p

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
        # print len(array), "delay length"
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

    def divideDelayToFiles(self, numberOffiles, path, nodeName, rate, numberofPacketInFile):
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
            dels=[]
            delay=140
            for i in range(0,numberofPacketInFile):
                delay+=float(selectedJitter[i])

                file.write(str(delay)+" ")
                dels.append(delay)
            file.close()
            # for k in range(1,len(dels)):
            #     if dels[k]-dels[k-1]:
            #         print "neg"



    def getNumbeOfExtractedBits(self,array):
        extN=0
        for j in range(0,len(array)):
            if array[j]=='0' or array[j]=='1':# or array[j]=='2' or array[j]=='3':
                extN+=1
        return extN
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
        print "FUnction Selcet Random Delay"
        for j in range(0,len(delays)):
            if self.isfloat(delays[j]):
                if delays[j]<0:
                    print delays[j], "Delay Negative"
                delayArray.append(float(delays[j]))
        mean=self.calcMean(delayArray)
        # print delayArray
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
        for p in range(0,len(timings1)):
            for k in range(0,len(timings1)-1):
                if timings1[k+1]<timings1[k]:
                    temp=timings1[k]
                    timings1[k]=timings1[k+1]
                    timings1[k+1]=temp
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
                numberOfExtr.append(self.getNumbeOfExtractedBits(extracteds2[p]))


            index=0
            max=0
            for j in range(0,len(numberOfExtr)):
                if numberOfExtr[j]>max:
                    max=numberOfExtr[j]
                    index=j

            extracted=extracteds2[index]
            portion=portions[index]

            #plt.plot(arrayX,portion,"*-")

            # p=plotJit.ploty()
            # p.plotDIfference(portion,name="Fingerprinted")
            #print extracted, "STD:", stdDelay,"Mean: ", mean,"Index:",i, \
            print "index: ",i , "Number Of detect:",fibir.compare(extracted),"Number of extra: ",self.getNumbeOfExtractedBits(extracted)
            print "Number of Flow: ",i
            print "finger",fibir.fingerPrint
            numberOfExtracteds[fibir.compare(extracted)]+=1

            #print extracted

        return [numberOfExtracteds]

    def clientForTryingDifferentEXTThreshold(self,fibir,slotLength,rate,node,numberOfSimul,rands,fing,lnt):
        extResultDiffThresholds=[]


        extChoices=[]
        for k in range(0,2*int(fibir.movingThreshold*10)+1):
            extChoices.append(1/float(6)+0.05*k)
        for k in range(0,len(extChoices)):
            extResultDiffThresholds.append([0]*fibir.fingerPrintLength)

        print "Number of trying threshold for extraction:  ", len(extChoices)

        for i in range(0,numberOfSimul):

            fileName="/home/fatemeh/allPackets/Fingerprint/files/rates/"+str(rate)+"/timing"+str(i)+".txt"

            content=fibir.readFromFile(fileName)
            delayArray=self.selectRandomDelayFile(rate=rate,node=node,rand=rands[i])
            mean=self.calcMean(delayArray)
            stdDelay=self.calcStandardDeviation(delayArray,mean)
            print "STD of delay:   ",stdDelay, "delay Mean:  ",mean
            slotLen=self.decideSlotValue(std=stdDelay)#*10
            roundSlotLength=slotLength#20#self.getRoundSlotLength(slotLen)

            numOfSubintervals=10
            interLength=self.getIntervalLength(numOfSubintervals, numberofSlot=6, slotLength=roundSlotLength)

            numOfSubintervals=self.getNumberOfSubintervals(intervalLength=interLength,numberofSlot=6,slotLength=roundSlotLength)
            fibir.calcParameters(intervalLength=interLength,numberOfSubintervals=numOfSubintervals,numberOfSlots=6)

            intervalList=fibir.getTlengthIntervals(content)
            markIntervalList=intervalList#[0:fingerprintlength]#sw.getMarkAndBaseIntervals(intervalList)

            fibir.setJitterCoefficent()#this sould be accodring to slot length

            nPKTS=0
            for k in range(0,len(markIntervalList)):
                nPKTS+=markIntervalList[k].getlen()
            print "Number of all packets:  ",nPKTS,len(markIntervalList)

            if fing:
                markIntervalList=fibir.insertFingerPrintOnHighRates(markIntervalList)#fibir.insertFingerPrint(markIntervalList)

            fibir.addDelayTofFlow(markIntervalList, delayArray)

            for k in range(0,6):#len(extChoices)):
                extResultDiffThresholds[k][self.tryDifferentExtractionThreshold(extChoices[k],markIntervalList,fibir,int(math.fabs(mean)))]+=1
                # print "h",k
        # for k in range(0,len(extChoices)):
        #     print extResultDiffThresholds[k],"Extraction Threshold:  ",extChoices[k], "Moving Threshold: ", fibir.movingThreshold
        #     sum=0
        stds=[]
        exts=[]
        for k in range(0,6):#len(extChoices)):
            std,ext=self.plotFrDiffExtrThrshld(extResultDiffThresholds[k],numberOfSimul)
            exts.append(ext)
            stds.append(std)
        plt.errorbar(extChoices[0:6],exts,lw=4,yerr=stds, fmt=lnt)
        # plt.legend(lengend,fontsize=36)







    def plotFrDiffExtrThrshld(self,extr,numberOfSimul):

        sum=0
        std=0

        for k in range(0,len(extr)):
                    sum+=extr[k]*k
        sum/=float((len(extr)-1)*numberOfSimul)
        for k in range(0,len(extr)):
                std+=math.pow(((k/float(len(extr)-1))-sum),2)*extr[k]
                    #print std,"llllllllllllllll",extr[k],sum,float(k/float(len(extr)-1)),math.pow(((float(k/float(len(extr)-1))-sum)),2)*extr[k],math.pow(((float(k/float(len(extr)-1))-sum)),2)
        std/=float(numberOfSimul)
        std=float(math.sqrt(std))

        return std,sum
        #


    def tryDifferentExtractionThreshold(self,extThreshold,markIntervalList,fibir,mean):
            extractedPortion=fibir.tryDifferntOffset(1,(mean+10), markIntervalList,extThreshold)

            extractedF=extractedPortion[0]


            numberOfDetection=[]
            numberOfExtr=[]
            for p in range(0,len(extractedF)):
                numberOfDetection.append(fibir.compare(extractedF[p]))
                numberOfExtr.append(self.getNumbeOfExtractedBits(extractedF[p]))


            index=0
            max=0
            for j in range(0,len(numberOfDetection)):
                if numberOfExtr[j]>max:
                    max=numberOfExtr[j]
                    index=j

            extracted=extractedF[index]

            return  fibir.compare(extracted)

    def client(self, fibir,slotLength,rate,node,numberOfSimul,rands):

        arrayX=[]
        ipds1=[]
        ipds2=[]
        for j in range(0,30):
            arrayX.append(j)

        ArrayOFNumbers=[]
        numberOfExtracteds=[]
        for i in range(0,31):
            ArrayOFNumbers.append(i)
            numberOfExtracteds.append(0)

        for i in range(0,numberOfSimul):

            fileName="/home/fatemeh/allPackets/Fingerprint/files/rates/"+str(rate)+"/timings"+str(i)+".txt"

            content=fibir.readFromFile(fileName)
            delayArray=self.selectRandomDelayFile(rate=rate,node=node,rand=rands[i])
            mean=self.calcMean(delayArray)
            stdDelay=self.calcStandardDeviation(delayArray,mean)
            print "STD of delay:   ",stdDelay
            slotLen=self.decideSlotValue(std=stdDelay)#*10


            roundSlotLength=slotLength#20#self.getRoundSlotLength(slotLen)

            numOfSubintervals=5
            interLength=self.getIntervalLength(numOfSubintervals, numberofSlot=6, slotLength=roundSlotLength)


            # numOfSubintervals=self.getNumberOfSubintervals(intervalLength=interLength,numberofSlot=6,slotLength=roundSlotLength)
            fibir.calcParameters(intervalLength=interLength,numberOfSubintervals=numOfSubintervals,numberOfSlots=6)

            intervalList=fibir.getTlengthIntervals(content)
            markIntervalList=intervalList#[0:fingerprintlength]#sw.getMarkAndBaseIntervals(intervalList)

            fibir.setJitterCoefficent()#this sould be accodring to slot length

            nPKTS=0
            for k in range(0,len(markIntervalList)):
                nPKTS+=markIntervalList[k].getlen()
            print "Number of all packets:  ",nPKTS,len(markIntervalList),len(delayArray)



            # IPD1=self.getIPDFromMIList(markIntervalList)
            # ipds1.append(IPD1)
            fibir.movingThreshold=1
            fibir.threshold=0.5
            markIntervalList=fibir.insertFingerPrintOnHighRates(markIntervalList)
            fibir.addDelayTofFlow(markIntervalList, delayArray)

            IPD2=self.getIPDFromMIList(markIntervalList)
            ipds2.append(IPD2)
            print "fibir.addDelayTofFlow(markIntervalList, delayArray)      ", fibir.fingerPrint

            extractedPortion=fibir.tryDifferntOffset(1,int(math.fabs(mean))+20, markIntervalList,fibir.movingThreshold/2)
            # extractedPortion=fibir.tryDifferntOffset(1,200, markIntervalList,fibir.movingThreshold/2)
            # extractedPortion=fibir.tryDifferntOffset(1,1, markIntervalList,fibir.movingThreshold/2)



            portions=extractedPortion[1]
            extracteds=extractedPortion[0]
            extracteds2=extracteds


            numberOfDetection=[]
            numberOfExtr=[]
            for p in range(0,len(extracteds2)):
                numberOfDetection.append(fibir.compare(extracteds2[p]))
                numberOfExtr.append(self.getNumbeOfExtractedBits(extracteds2[p]))


            index=0
            max=0
            for j in range(0,len(numberOfExtr)):
                if numberOfExtr[j]>max:
                    max=numberOfExtr[j]
                    index=j

            extracted=extracteds2[index]


            print "index: ",i , "Number Of detect:",fibir.compare(extracted),"Number of extra: ",self.getNumbeOfExtractedBits(extracted), "mean: ",mean
            numberOfExtracteds[fibir.compare(extracted)]+=1

        return [ipds1,ipds2,numberOfExtracteds]

    def plotFigure(self,plt):
        plt.xlabel("i's interval")
        #plt.ylabel("Fraction of packets in selected slots")
        plt.ylabel("Portion of difference between selected and non-selected slots")
        plt.ylim(-1,1)
        plt.title("Result on unfingerprinted flow")
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
    def addDelayToTimings(self,delay,timings):
        print len(delay),len(timings), " delay Timings"
        timingL=[]
        for k in range(0,len(timings)):
            timingL.append(0)
            timingL[k]=delay[k]+float(timings[k])
            # timings[k]+=delay[k]
        return timingL
    def nextTime(self,rateParameter):
            return -math.log(1.0 - random.random()) / rateParameter
    def BuildCUmulativeFlowsMixed(self,node):

        allIPDs=[]#first item is rate 10, second one 11, third one 12
        npksts=1000
        allTimings=[]
        beg=0
        delay=self.selectRandomDelayFile(rate=10,node=node,rand=random.randrange(0,100))
        for k in range(0,npksts*3):
            r=random.randrange(0,3)
            if r==0:
                allIPDs.append(self.nextTime(0.01))
            elif r==1:
                allIPDs.append(self.nextTime(0.011))
            elif r==2:
                allIPDs.append(self.nextTime(0.012))
        for i in range(0,len(allIPDs)):
            # print allIPDs[i]
            allTimings.append(beg)
            beg+=allIPDs[i]
        count=0
        allTimings[0]+=delay[0]
        for k in range(1,len(allTimings)):
            if delay[k]<0:
                print delay[k]
            else:

                allTimings[k]+=delay[k]
                if allTimings[k-1]>allTimings[k]:
                    temp=allTimings[k]
                    allTimings[k]=allTimings[k-1]
                    allTimings[k-1]=temp
                    count+=1
        for k in range(0,len(allTimings)):
            for p in range(0,len(allTimings)-1):
                if allTimings[p]>allTimings[p+1]:
                    temp=allTimings[p]
                    allTimings[p]=allTimings[p+1]
                    allTimings[p+1]=temp

        print "Hey:  ",count
        fileO=open("/home/fatemeh/allPackets/Fingerprint/ksR/cumulativeFlow.txt","w")

        allIPD2=[]
        for k in range(1,len(allTimings)):

            if allTimings[k]-allTimings[k-1]>0:
                allIPD2.append(allTimings[k]-allTimings[k-1])
            else:
                print "kddddddddddddd",k,allTimings[k-1],allTimings[k]
        print len(allIPD2)," IPD2"
        for k in range(0,len(allIPD2)):
            fileO.write(str(allIPD2[k])+" ")
        fileO.close()



    def buildCumulativeFlowsDifRates(self,nodeName):
        #TODO get some timing with different rates and add jitter. :)
        fileO=open("/home/fatemeh/allPackets/Fingerprint/ksR/cumulativeFlow.txt","w")
        rates=[10,15,20,12]
        count=0
        flowLenght=1000
        for i in range(0,5):
            for k in range(0,len(rates)):

                delay=self.selectRandomDelayFile(rate=10,node=nodeName,rand=random.randrange(0,200))
                fileName="/home/fatemeh/allPackets/Fingerprint/files/rates/"+str(rates[k])+"/timing"+str(i)+".txt"
                timings=self.readFromFile(fileName)
                timings=timings.split(" ")[0:15000]
                newTimings=self.addDelayToTimings(delay,timings)
                for p in range(1,len(newTimings)):
                    if newTimings[p]-newTimings[p-1]>0:
                        fileO.write(str(newTimings[p]-newTimings[p-1])+" ")



                count+=1
        fileO.close()


    def MainCumulativeTest(self):
        pass

    def MainKSTest(self):

        FIB=FIBIR.FIBIR(markFlowLength=30,nBits=1)
        allslotLength=[10]#1,5,10,20,30,40,50,60]#[1,2,5,10,20]
        numberOFPackets=[]
        randsContent=self.readFromFile('rands.txt')#self.getRandomNumber(100)
        randArray=randsContent.split(" ")
        rands=[]
        nSim=100
        for k in range(0,len(randArray)-1):
            rands.append(int(randArray[k]))

        slot='Slot length='
        lineType=['*-',"s-","o-","^-",'*--',"s--","o--","^--"]
        lengend=[slot+'1ms',slot+'5ms',slot+'10ms',slot+'20ms',slot+'30ms',slot+'40ms',slot+'50ms',slot+'60ms']
        ksResults=[]
        for j in range(1,10):
            numberOFPackets.append(j*50)
        for i in range(0,len(allslotLength)):
            IPD1,IPD2,extr=self.client(fibir=FIB,slotLength=allslotLength[i],rate='10',node="ETHZ",numberOfSimul=nSim,rands=rands)
            # per=
            # for k in range(0,nSim):
            #     per+=FIB.unFingeprintedPercent[k]
            # per/=float(100)
            # print "Unfingerprinted percent: ",per
            self.writeAllIPDsToFiles(IPD1,IPD2,allslotLength[i])
            print extr, "extttt"
            nMore=0

            sum=0
            for k in range(0,len(extr)):
                    nMore+=1

                    sum+=extr[k]*k
            sum/=float((len(extr)-1)*nSim)
            print "extraction Rate: ", sum#, nMore
            # print len(IPD1),len(IPD2)
            '''ksResults.append([])
            for j in range(0,9):
                ks=ks_2samp(IPD1[j*50:(j+1)*50], IPD2[j*50:(j+1)*50])
                ksResults[i].append(ks[0])

        for i in range(0,len(allslotLength)):
            #
            plt.plot(numberOFPackets,ksResults[i],lineType[i],lw='2' )

        plt.legend(lengend,fontsize=36)


        plt.ylabel('K-S test difference',fontsize=36)
        plt.ylim(0,1)
        plt.xlabel('Number of packets (n)',fontsize=36)
        plt.show()'''

    def getIntervalLength(self, numberOfSubintervals, numberofSlot, slotLength):
        intervalLength=slotLength*6*numberOfSubintervals
        # numberOfSubintervals=int(intervalLength/(numberofSlot*slotLength)+0.000000001)
        # print numberOfSubintervals, "number of subintervals",intervalLength,numberofSlot,slotLength,intervalLength/(numberofSlot*slotLength)
        return intervalLength
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
    def MainExtrSlot(self):


        FIB=FIBIR.FIBIR(markFlowLength=30,nBits=2)
        randsContent=self.readFromFile('rands.txt')#self.getRandomNumber(100)
        randArray=randsContent.split(" ")
        rands=[]
        for k in range(0,len(randArray)-1):
            rands.append(int(randArray[k]))
        rands=[]


        numberOfSimu=200
        for k in range(0,numberOfSimu):
            rands.append(k)
        allslotLength=[5,10,15,25,30,40]#[0.1,0.2,0.4,0.5,0.8,1]##[20,30,40,50,80,100]#[15]#5,10,20,25,30,40,50]#,60,80,100,120,140,160,180,200]
        #allslotLength=[10,20,30,40,50,60,70,80,90]#T=2*1800?
        rates=[10]#,100,200]#,100,200]#,100,200]#,100,200]#,100,200]
        landa="Rate="
        lineType=["*-","s-",'o-']
        lengend=[landa+'10pkt/sec',landa+'100pkt/sec',landa+'200pkt/sec']


        for j in range(0,len(rates)):

            extRates=[]
            stds=[]
            std=0
            for i in range(0,len(allslotLength)):

                print i,j, allslotLength[i], len(rates)
                IPD1,IPD2,extr=self.client(fibir=FIB,slotLength=allslotLength[i],rate=rates[j],node="ETHZ",numberOfSimul=numberOfSimu,rands=rands)


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



            plt.errorbar(allslotLength,extRates,lw=4,yerr=stds, fmt=lineType[j])
            #plt.plot(allslotLength,extRates,lineType[j],lw='2')

        fn=FN_p.porbability()

        fn.plotFN("s-",10,plt)

        plt.legend(lengend,fontsize=45,loc=4)
        plt.legend(["Simulation","Analysis"],fontsize=45,loc=4)

        plt.ylabel('Extraction rate',fontsize=45)
        plt.ylim(0,1.01)
        #yticks=np.
        # plt.yticks(np.arange(0,1.01,0.1))
        plt.xlabel('Slot length (ms)',fontsize=45)
        plt.show()

        # plt.legend(lengend,fontsize=45,loc=4)
        # #plt.title('Extraction rate according to the slot length for Amherst-ETHZ',fontsize=45)
        # plt.ylabel('Extraction rate',fontsize=45)
        # plt.ylim(0,1.1)
        # #yticks=np.
        # plt.yticks(np.arange(0,1.1,0.1))
        # plt.xlabel('Slot length (ms)',fontsize=45)
        # plt.show()

    def Main(self):
        FIB=FIBIR.FIBIR(markFlowLength=30)
        self.client(fibir=FIB,slotLength=20,rate=10,node="ETHZ")


    def ks_pMove(self):
        FIB=FIBIR.FIBIR(markFlowLength=30,nBits=1)
        moves=[0.2,0.4,0.6,0.8,1]
        rates=[10,100,200]#,100,200]
        landa="Rate="
        randsContent=self.readFromFile('rands.txt')#self.getRandomNumber(100)
        randArray=randsContent.split(" ")
        rands=[]
        nSimul=100

        for k in range(0,len(randArray)-1):
            rands.append(int(randArray[k]))
        lineType=["*-","s-","o-"]#,"t-"]
        lengend=[landa+'10pkt/sec',landa+'100pkt/sec',landa+'200pkt/sec']
        ksResults=[]

        for j in range(0,len(rates)):
            ksResults=[]
            kss=[]
            stds=[]
            for i in range(0,len(moves)):
                FIB.setpMove(moves[i])
                IPD1,IPD2,extr=self.client(fibir=FIB,slotLength=8,rate=rates[j],node="ETHZ",numberOfSimul=nSimul,rands=rands)
                print len(IPD1), IPD2
                # ks=ks_2samp(IPD1, IPD2)
                # ksResults.append(ks[0])
                # print ks[0],"ks"
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
                # print std,"dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"
                # print std,"STTTTTTTTTTTTTTD"
                #print std,'stddddd'
                stds.append(std)


            plt.errorbar(moves,ksResults,lw='4',yerr=stds, fmt=lineType[j])
        plt.legend(lengend,fontsize=36,loc=2)
        plt.xlabel("$R_{move}$",fontsize=36)
        plt.ylabel("ks statistic",fontsize=36)
        plt.ylim(0,1)
        plt.yticks(np.arange(0,1.1,0.1))
        #plt.title("KS difference according to different R_move",fontsize=36)
        plt.show()



    def extractionRate_pMove(self):
        FIB=FIBIR.FIBIR(markFlowLength=30)
        moves=[0.2,0.4,0.6,0.8,1]
        realMove=[]
        for j in range(0,len(moves)):
             realMove.append(float(moves[j]/2))

        numberOfSimu=100
        rates=[10]#,100,200]#,200]
        landa="Rate="
        lineType=["*-","s-","o-"]
        lengend=[landa+'10pkt/sec',landa+'100pkt/sec',landa+'200pkt/sec']

        for j in range(0,len(rates)):
            extRates=[]
            stds=[]
            for i in range(0,len(moves)):
                FIB.setpMove(moves[i])
                IPD1,IPD2,extr=self.client(fibir=FIB,slotLength=8,rate=rates[j],node="ETHZ",numberOfSimul=numberOfSimu)
                sum=0
                std=0
                for t in range(0,len(extr)):
                    sum+=extr[t]*t
                sum/=float(len(extr)*numberOfSimu)

                for k in range(0,len(extr)):
                    std+=math.pow(((k/float(len(extr)-1))-sum),2)*extr[k]
                std/=float(numberOfSimu)
                std=float(math.sqrt(std))
                stds.append(std)
                extRates.append(sum)
            plt.errorbar(realMove,extRates,lw='2',yerr=stds, fmt=lineType[j])

        plt.legend(lengend,fontsize=36)
        plt.xlabel("R_move",fontsize=36)
        plt.ylabel("Extraction Rate",fontsize=36)
        plt.title("Extraction Rate for different R_move",fontsize=36)
        plt.ylim(0,1)
        plt.show()



    def barGraph(self,numberOfPackets):
        N = 200
        menMeans = numberOfPackets[0:N]#[20, 35, 30, 35, 27]
        #menStd = (1, 1, 1, 1, 1)
        ind = np.arange(N)  # the x locations for the groups
        width = 1       # the width of the bars
        fig, ax = plt.subplots()
        #fig.ylim(0,5)
        rects1 = ax.bar(ind, menMeans, width, color='b',edgecolor='b')
        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()


        autolabel(rects1)
        plt.yticks(np.arange(0,10,1))

        plt.ylim(0,10)
        #plt.show()
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
    def writeAllIPDsToFiles(self, IPD1, IPD2, slotL):#i is equal to slotLength

        for j in range(0,len(IPD1)):


            fileForKSResult="/home/fatemeh/allPackets/Fingerprint/ksR/after"+str(j)+"DrmoveF08D"
            fileForKSResult+= str(slotL) + ".txt"


            fileO=open(fileForKSResult,"w")
            ipd2=IPD2[j]
            # print ipd2[0:1],ipd1[0:1]
            negatives=[]
            cou=0
            for k in range(0,len(ipd2)):
                if ipd2[k]>0:

                    fileO.write(str(ipd2[k])+" ")
                else:
                    negatives.append(k)
                    cou+=1
            fileO.close()
            # print "Number of disordered in Reciever Side: ",cou
            fileForKSResult="/home/fatemeh/allPackets/Fingerprint/ksR/"+"before"+str(j)+"DrmoveF08D"
            fileForKSResult+= str(slotL) + ".txt"

            fileO=open(fileForKSResult,"w")
            ipd1=IPD1[j]

            cou=0
            for k in range(0,len(ipd1)):
                if ipd1[k]>0 and k not in negatives:
                    # print "SDdsdsdsdsdsdsd"
                    fileO.write(str(ipd1[k])+" ")
                else:
                    cou+=1
                    # print "FERESHTEEEEEEEEEEEEEEEEEEEEE"
            # print "Number of Disordered in sender Packets: ", cou
            fileO.close()

            '''lenn=50
            avgIPD1=np.sum(ipd1[0:lenn])
            # print avgIPD1/lenn, "Avg IPD 1",avgIPD1
            avgIPD2=np.sum(ipd2[0:lenn])
            # print avgIPD2/lenn, "Avg IPD 2",avgIPD2
            base=80
            step=10
            # print ipd1[base:base+step]
            # print ipd2[base:base+step]

            stdIPD1=self.calcStandardDeviation(ipd1[0:lenn],avgIPD1/lenn)
            stdIPD2=self.calcStandardDeviation(ipd2[0:lenn],avgIPD2/lenn)
            print stdIPD1,stdIPD2, "STDDD"'''


    def MainEXTThrshldTst(self):
        FIB=FIBIR.FIBIR(markFlowLength=30,nBits=1)
        randsContent=self.readFromFile('rands.txt')
        randArray=randsContent.split(" ")
        rands=[]
        for k in range(0,len(randArray)-1):
            rands.append(int(randArray[k]))

        self.clientForTryingDifferentEXTThreshold(fibir=FIB,slotLength=10,rate=10,node="ETHZ",numberOfSimul=20,rands=rands,fing=False,lnt="*-")
        self.clientForTryingDifferentEXTThreshold(fibir=FIB,slotLength=10,rate=10,node="ETHZ",numberOfSimul=20,rands=rands,fing=True,lnt="s-")

        plt.legend(["None-Fingerprinted","Fingerprinted"],fontsize=36)
        plt.ylabel('Extraction Rate',fontsize=36)
        plt.ylim(0,1)
        plt.xlabel('Different extraction Threshold ($R_{move}=$)'+str(FIB.movingThreshold),fontsize=36)
        plt.show()
    def combineDiffFlowRates(self):

        FIB=FIBIR.FIBIR(markFlowLength=30,nBits=1)
        slotL=12
        rates=[10,14]
        nSim=1

        randsContent=self.readFromFile('rands.txt')#self.getRandomNumber(100)
        randArray=randsContent.split(" ")
        rands=[]
        for k in range(0,len(randArray)-1):
            rands.append(int(randArray[k]))

        for k in range(0,len(rates)):
            IPD1,IPD2,ext=self.client(fibir=FIB,slotLength=slotL,rate=str(rates[k]),node="china",numberOfSimul=nSim,rands=rands)
            self.writeAllIPDsToFiles(IPD1,IPD2,slotL,rates[k])

        afterIPDs=[]
        beforeIPDS=[]
        for i in range(0,len(rates)):
            for k in range(0,nSim):

                fileForKSResult="/home/fatemeh/allPackets/Fingerprint/ksR/after"+str(k)+"D"
                fileForKSResult+=str(slotL)+"rate"+str(rates[i])+".txt"

                con=FIB.readFromFile(fileForKSResult)
                x =con.split(" ")[:-1]
                y=[]
                for j in range(0,len(x)):
                    y.append(float(x[j]))

                afterIPDs+=y
        for i in range(0,len(rates)):
            for k in range(0,nSim):

                fileForKSResult="/home/fatemeh/allPackets/Fingerprint/ksR/before"+str(k)+"D"
                fileForKSResult+=str(slotL)+"rate"+str(rates[i])+".txt"

                con=FIB.readFromFile(fileForKSResult)
                x =con.split(" ")[:-1]
                y=[]
                for j in range(0,len(x)):
                    y.append(float(x[j]))

                beforeIPDS+=y
        print len(beforeIPDS)," # Of Packets"  ,len(afterIPDs)

        self.writeCombinedRatesToFiles(beforeIPDS,afterIPDs,'a','b')

    def writeCombinedRatesToFiles(self,ipd1,ipd2,i,rate):#i is equal to slotLength

            fileForKSResult="/home/fatemeh/allPackets/Fingerprint/ksR/after"+"D"
            fileForKSResult+=str(i)+"rate"+str(rate)+".txt"


            fileO=open(fileForKSResult,"w")
            negatives=[]
            cou=0
            for k in range(0,len(ipd2)):
                if ipd2[k]>0:
                    fileO.write(str(ipd2[k])+" ")
                else:
                    negatives.append(k)
                    cou+=1
            fileO.close()
            print "Number of disordered in Receiver Side: ",cou

            fileForKSResult="/home/fatemeh/allPackets/Fingerprint/ksR/"+"before"+"D"
            fileForKSResult+=str(i)+"rate"+str(rate)+".txt"

            fileO=open(fileForKSResult,"w")
            cou=0
            for k in range(0,len(ipd1)):
                if ipd1[k]>0 and k not in negatives:
                    fileO.write(str(ipd1[k])+" ")
                else:
                    cou+=1
            print "Number of Disordered in sender Packets: ", cou
            fileO.close()


import itertools
#Overhead is for permutation functions

tes=tesFIBIR()
# tes.divideDelayToFiles(1000, "/home/fatemeh/allPackets/china/jitter/10/all.txt", "china", "10", numberofPacketInFile=800 )

#tes.devideJitterToFiles(1000,"/home/fatemeh/allPackets/ETHZ/jitter/200/all.txt","ETHZ","200",numberofPacketInFile=10000*5)
# tes.MainKSTest()
tes.MainExtrSlot()
extr=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 3, 7, 14, 20, 29, 18, 5]# 8 and r=15
extr=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 5, 10, 17, 17, 18, 17, 8, 1]#10
# extr=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 2, 1, 0, 1, 4, 12, 15, 15, 13, 17, 6, 6, 0, 0]#8 slot length
# extr=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 9, 23, 23, 22, 12, 3]#12
# extr=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 9, 14, 22, 15, 20, 12, 4]#6
#extr=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 12, 20, 41, 22] 10 with 15 as r
sum=0
for k in range(0,len(extr)):
        sum+=extr[k]*k
sum/=float((len(extr)-1)*98)
print sum
# tes.combineDiffFlowRates()
# tes.MainEXTThrshldTst()
# tes.MainExtrSlot()
# tes.BuildCUmulativeFlowsMixed('ETHZ')
# tes.buildCumulativeFlowsDifRates("china")
# tes.MainKSTest()
#delayArray=tes.selectRandomDelayFile(rate=100,node='irland')
#tes.devideJitterToFiles(400)
#tes.Main()
# tes.ks_pMove()
#print "hey youuuuuuuuuuuuu"
# tes.extractionRate_pMove()
#tes.divideIPDs("files/rates/input10.txt",600,rate=10)
'''perm1=tes.finPermutations()
perm2=tes.finPermutations()
numberOfSimil=0
for i in range(0,len(perm2)):
    for j in range(0,1):
        if perm1[i][j]==perm2[i][j]:
            numberOfSimil+=1
print numberOfSimil

'''
#tes=tesFIBIR()
#(self,numberOffiles,path,nodeName,rate,numberofPacketInFile)
#tes.devideJitterToFiles(1000,"/home/fatemeh/allPackets/"+"irland"+"/jitter/"+"10"+"/all.txt","irland","10",800)
#tes.Main()
#tes.barGraph()
#TODO work on K_S Test


