import nf
from scapy.all import *
import os#ssh umass_pet@planetlab3.inf.ethz.ch
import numpy as np
import matplotlib.pyplot as plt
#import commpy.channelcoding.convcode as cc
#import plot
#import scikit-commpy
input=nf.getTheParameters()
fingerprint=input[1]
# markIntervals=input[1]
# baseIntervals=input[2]
#permutations=input[3]
permutations=input[0]

#print permutations
threshold=0.5
baseIntervalList=[]
markIntervalList=[]
#system parameters
intervalLength=2160#1800
numberofSubintervals=18#30#1200#20*2*2
numberOfSlots=6
subintervalLength=intervalLength/float(numberofSubintervals)
mslotLength=float(intervalLength/float(numberofSubintervals*numberOfSlots))
print mslotLength,subintervalLength
markFlowLength=30
improvement=0
messages=[]
for k in range(0,2):
    messages.append(k)
#print subintervalLength,mslotLength

generator_matrix = np.array([[07, 05,03]])#cchanging to 1/4 and changing the number of memory..> I have to look
        #at these alternatives
        #print("dddddddddddddddd")
        #generator_matrix = np.array([[03, 00, 02], [07, 04, 06]])
M = np.array([2])
        #self.trellis = cc.Trellis(self.M, self.generator_matrix)
        #print(self.generator_matrix.shape," shape")
coeficeient=5
def minusMeanDealy(mark,mean):


        for i in range(0,len(mark)):
            inte=mark[i]
            for j in range(0,len(inte)):
                inte[j]-=mean

def writeIntervalsToFile(mark,name):

        target = open(name, 'w')
        for i in range(0,markFlowLength):
                        inter=mark[i]
                        for j in range(0, len(inter)):
                            target.write(str(inter[j]))
                            target.write(" ")

def tryDiffOffsets(offset,desI,markIntervalList):

            fileName2="first"
            minusMeanDealy(markIntervalList,offset)
            fileName2+=str(desI)+"rec"+".txt"
            writeIntervalsToFile(markIntervalList,fileName2)

            con=readFromFile(fileName2," ")
            intervals2=getTlengthIntervals(con)
            markIntervalList=intervals2[0:markFlowLength]
            extracted=extractFinger(markIntervalList)#error

            return extracted

def readFromFile(path,delimiter):
    content=""
    c=""
    with open(path, 'r') as content_file:
             content = content_file.read()
             #print content
             c=content.split(delimiter)
    '''for i in range(0,len(c)):
        if isfloat(c[i]):
            c[i]=float(c[i])
            #print c[i]
        else:
            c[i]=0'''

    return  c

def getTlengthIntervals(content):
        numbers=content

        intervalList=[]
        for i in range(0, markFlowLength):
            intervalList.append([])

        upperBound=intervalLength
        i=0
        condition=True
        count=0
        while condition:
            #print numbers[i]
            if upperBound==intervalLength+markFlowLength*intervalLength:
                break
            #print numbers[i],i

            if i>=len(numbers) or not isfloat(numbers[i]):# this means we are in the end of our file
                break

            if i<len(numbers) and float(numbers[i])<upperBound:
                intervalList[count].append(float(numbers[i]))#????///
                i+=1
                if i==len(numbers):
                    break
            else:
                upperBound+=intervalLength
                count+=1
        #print "intervals lIst"
       # print intervalList

        return intervalList

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def getMarkBaseExtraction(interval):
        markIntervalList=[]
        for j in range(0,len(markIntervals)):
            markIntervalList.append(interval[int(markIntervals[j])])
        baseMark=[]
        baseMark.append(baseIntervalList)
        baseMark.append(markIntervalList)
        return baseMark

def randomExtract(inter, center, i):
            #print inter
            count=0
            counter=0
            #print inter,"inter"
            msLotLength=intervalLength/float(numberOfSlots*numberofSubintervals)
            #print mslotLength
            centroid=center
            allpackets=len(inter)
            if len(inter)<2:
                return ["Zero",0]

            numberOfInterval=int(inter[0]/intervalLength)
            lowerBound=intervalLength*numberOfInterval
            upperBound=lowerBound+subintervalLength#subinterval
            numberOfCorrects=[]

            for k in range(0,2):
                numberOfCorrects.append(0)
            currentSubinterval=0
            nu=0
            #print len(inter),"l;lk"
            #print msLotLength,subintervalLength,numberofSubintervals,lowerBound,upperBound
            for j in range(0,len(inter)):
                nu+=1
                while(True):#????currentsubinter=0?
                        if (inter[j]>=lowerBound and inter[j]<upperBound):
                            counter+=1

                            #print permutations[0][0:10]
                            #print len(permutations[0])
#
                            for k in range(0,2):
                                location=int(permutations[k][i*numberofSubintervals+currentSubinterval][centroid])
                            #print(location,"ll",type(location))
                                if inter[j]>=location*msLotLength+lowerBound \
                                    and inter[j]<lowerBound+(location+1)*msLotLength:
                                    numberOfCorrects[k]+=1

                            # locationZer=int(permutZero[i*numberofSubintervals+currentSubinterval][centroid])
                            #
                            # if inter[j]>=locationZer*msLotLength+lowerBound \
                            #         and inter[j]<lowerBound+(locationZer+1)*msLotLength:
                            #     numberOfCorrectZeros+=1

                            lowerBound-=subintervalLength#o
                            upperBound-=subintervalLength
                            currentSubinterval-=1#??

                            break
                        else:
                            #print(currentSubinterval, "No packet in this subinterval")
                            lowerBound=upperBound
                            upperBound+=subintervalLength#subintervalLength
                            currentSubinterval+=1
                            if currentSubinterval==numberofSubintervals:#order???
                                currentSubinterval=0
                                break
                            if upperBound>markFlowLength*intervalLength+1000:#???#stupid mistake
                                break
                            count+=1

            numberAllPackets=len(inter)
            #print nu,"Sdsddd",numberAllPackets

            # I should check if the intersection of these four if's are not zero...
            maxIndex=getMax(numberOfCorrects)
            if numberOfCorrects[maxIndex]>threshold*numberAllPackets:
                #print messages[maxIndex]
                return [messages[maxIndex],numberOfCorrects[maxIndex],0]
            else:
                #print "n"
                return ["N",0,0]
def getMax(array):
        max=0
        index=0
        for i in range(0,len(array)):
            if array[i]>max:
                max=array[i]
                index=i
        return index
def extracRandFingerprintNewM(inter,center,i):

            count=0
            counter=0
            #print inter,"inter"
            msLotLength=intervalLength/(numberOfSlots*numberofSubintervals)
            centroid=center
            allpackets=len(inter)
            if len(inter)==0:
                return "Zero"

            numberOfInterval=int(inter[0]/intervalLength)
            lowerBound=intervalLength*numberOfInterval
            upperBound=lowerBound+subintervalLength#subinterval
            numberOfCorrectOnes=0
            numberOfCorrectZeros=0
            currentSubinterval=0
            numberOfNull=0
            #print len(inter),i," h",type(inter[0])
            #print len(inter), "lengt"
            for j in range(0,len(inter)):
                #print inter[j],"j"
                while(True):#????currentsubinter=0?
                        if (inter[j]>=lowerBound and inter[j]<upperBound):
                            counter+=1

                            location=permutations[i*numberofSubintervals+currentSubinterval][centroid]
                            #print(location,"ll",type(location))
                            locSp=permutZero[i*numberofSubintervals+currentSubinterval][centroid]
                            if inter[j]>=location*msLotLength+lowerBound \
                                    and inter[j]<lowerBound+(location+1)*msLotLength:
                                numberOfCorrectOnes+=1

                            elif inter[j]>=locSp*msLotLength+lowerBound \
                                    and inter[j]<lowerBound+(locSp+1)*msLotLength:
                                numberOfCorrectZeros+=1
                            else:
                                numberOfNull+=1
                            lowerBound-=subintervalLength#o
                            upperBound-=subintervalLength
                            currentSubinterval-=1#??

                            break
                        else:
                            #print(currentSubinterval, "No packet in this subinterval")
                            lowerBound=upperBound
                            upperBound+=subintervalLength#subintervalLength
                            currentSubinterval+=1
                            if currentSubinterval==numberofSubintervals:#order???
                                currentSubinterval=0
                                break
                            if upperBound>markFlowLength*2*intervalLength:#???#stupid mistake
                                break
                            count+=1

            numberAllPackets=len(inter)
            #print numberAllPackets
            #print(inter.getlen())


            # I should check if the intersection of these four if's are not zero...
            if numberOfCorrectOnes>threshold*numberAllPackets:#threshold is not enough
                #print numberAllPackets
                #print(numberOfCorrectOnes, "One",numberAllPackets,"Index: ",location,center),i
                #print numberOfCorrectOnes,numberAllPackets
                return [1,numberOfCorrectOnes]
            elif numberOfCorrectZeros>threshold*numberAllPackets:
                 return [0,numberOfCorrectZeros]
            else:
                #print numberOfCorrectOnes,numberOfCorrectZeros,numberAllPackets
                return ["Null",0]



def extractOneBit(inter,index):#(self,inter,center,i):
        finger=[]
        #print index
        corr=[]
        for i in range(0,numberOfSlots):
            finCor=randomExtract(inter, i, index)#this can have newM
            finger.append(finCor[0])
            corr.append(finCor[1])
        max=0

        #print pind,len(finger)
        bit="N"
        for i in range(0,len(messages)):
            if messages[i] in finger:
                bit=messages[i]
       # print bit,

        return bit #finger[pind]

def extractFinger(markIntervalList):
        #fingerLoc=self.fingerPrintLoc#threshold check
        #we have to check it with baseinterval, center,....
        extractedFingerPrint=[]
        count=0
        for i in range(0, len(markIntervalList)):#fingerPrintLength
            inter=markIntervalList[i]
            if len(inter)==0:
                count+=1
            l=extractOneBit(inter,i)
            extractedFingerPrint.append(l)
        return [extractedFingerPrint,count]

def findMax(array):
        index=0
        max=array[0]
        for i in range(0, len(array)):
            if max<array[i]:
                max=array[i]
                index=i
        return index

def numberOfExtraction(extracted):

            numberOfExtraction=0
            if extracted!=None:
                for l in range(0,len(extracted)):
                    if extracted[l] in messages:
                        numberOfExtraction+=1
            #print numOfNull, "numberOFNull"
            return numberOfExtraction
def addDelay(mark,amount):
        minusMeanDealy(mark,-1*amount)
def tryIntervalOffsetInterval(inter,index):
    extractedBit=[]
    steps=15#int(mslotLength*4*3)/0.2
    for i in range(0,steps):
        #print i/2.0
        for j in range(0,len(inter)):
            inter[j]-=(i*0.2)
            f=extractOneBit(inter,index)
            extractedBit.append(f)
            inter[j]+=(i*0.2)
    for i in range(0,steps):
        for j in range(0,len(inter)):
            inter[j]+=(i*0.2)
            f=extractOneBit(inter,index)
            extractedBit.append(f)
            inter[j]-=(i*0.2)
    numOfZero=0
    numberOfOne=0
    for i in range(0,len(extractedBit)):
        if extractedBit[i]==0:
            numOfZero+=1
        elif extractedBit[i]==1:
            numberOfOne+=1
    #print "number Of zero: ", numOfZero
    #print "number of One: ", numberOfOne
    if numberOfOne>numOfZero:
            return 1
    if numOfZero>numberOfOne:
            return 0




def tryInternalOffset(markList,extr):
    for i in range(0,len(markList)):
        if extr[i]==4:
            inter=markList[i]
            k=tryIntervalOffsetInterval(inter,i)
            extr[i]=k
            #k=extractOneBit(inter,i)

    return extr
def getExtractedFingerprint(desI,step,numberOfSteps,markIntervalList,improvement):
#
            numOfPackets=0
            emptyInterval=0
            for i in range(0,len(markIntervalList)):
                if len(markIntervalList[i])==0:
                    emptyInterval+=1

                numOfPackets+=len(markIntervalList[i])
            print "Number Of Packets: ", numOfPackets,"N empty intervals: ",emptyInterval


            numberOfNoneFingerprinted=0
            numberOfFingerprinted=0
            mean=0#TODO think: why mean should be zero?
            offsets=[]
            extractedFingers=[]
            numberOfNulls=[]
            numberOfEmptyIntervals=[]

            for k in range(0, numberOfSteps):

                newMean=mean-k*step
                offsets.append(newMean)
                e=tryDiffOffsets(newMean,desI,markIntervalList)
                addDelay(markIntervalList,-k*step)
                extractedFingers.append(e[0])
                numberOfEmptyIntervals.append(e[1])
                numberOfExtr=numberOfExtraction(e[0])
                numberOfNulls.append(numberOfExtr)

            max=0
            subtractValue=mean
            selectedFingerprints=[]
            selectedOffsets=[]
            index=0

            for p in range(0,len(extractedFingers)):
                if numberOfNulls[p]>=max:
                    max=numberOfNulls[p]
                    subtractValue=offsets[p]

            slectedNumberOfEmpties=[]
            print max ,"minnnnnnnnnnnnnn"
            '''if max>7:
                    y=[]
                    x=[]
                    for l in range(0,len(offsets)):
                         if l%60!=0:
                             continue
                         tmp=0
                         for h in range(0,len(extractedFingers[l])):
                            if extractedFingers[l][h]==1 or extractedFingers[l][h]==0:
                                tmp+=1
                    y.append(tmp)
                    x.append(offsets[l])
               # print tmp
                    plt.plot(x,y)
                    plt.ylim(0,30)
                    plt.xlabel("Offset (ms)")
                    plt.ylabel("Extraction bits")
                    plt.show()'''

            for p in range(0,len(extractedFingers)):
                if numberOfNulls[p]==max:
                    selectedFingerprints.append(extractedFingers[p])
                    index=p
                    selectedOffsets.append(offsets[p])
                    slectedNumberOfEmpties.append(numberOfEmptyIntervals[p])


            print extractedFingers[index]
            # for pl in range(0,len(selectedFingerprints)):
            #     print selectedFingerprints[pl]

            extracted=extractedFingers[index]
            print "Number of selected offsets: ", len(selectedOffsets),subtractValue
            #print selectedOffsets,"ddddddddddddddddddd"

            '''numberOfZeros=[]
            numberOfOnes=[]
            extracted=[]
            for i in range(0,markFlowLength):
                numberOfOnes.append(0)
                numberOfZeros.append(0)
                extracted.append(0)

            for j in range(0,len(selectedFingerprints)):
                for k in range(0, markFlowLength):
                    if selectedFingerprints[j][k]==0 :
                        numberOfZeros[k]+=1
                    elif selectedFingerprints[j][k]==1 :
                        numberOfOnes[k]+=1


            for j in range(0,markFlowLength):
                #print numberOfOnes[j],numberOfZeros[j],j,len(selectedFingerprints)
                if numberOfZeros[j]>=0.9*len(selectedFingerprints):

                    extracted[j]=0
                elif numberOfOnes[j]>=0.9*len(selectedFingerprints):
                    extracted[j]=1
                else:
                    extracted[j]=4

            nullNum=0
            for j in range(0,len(extracted)):
                if extracted[j]==4:
                    nullNum+=1

            tryDiffOffsets(subtractValue,desI,markIntervalList)

            numOfPackets=0

            for i in range(0,len(markIntervalList)):
                numOfPackets+=len(markIntervalList[i])
            print "Number Of Packets:", numOfPackets

            if nullNum>=markFlowLength/2:
                numberOfNoneFingerprinted+=1
                return extracted
            else:
                numberOfFingerprinted+=1
            #TODO there should be a change
            for i in range(0,markFlowLength):
                    if numberOfZeros[i]>numberOfOnes[i]:
                        extracted[i]=0
                    elif numberOfZeros[i]<=numberOfOnes[i] and numberOfOnes[i]!=0:
                        extracted[i]=1
                    else:
                        extracted[i]=4'''

            #a=compare(fingerprint,extracted)
            #extracted=tryInternalOffset(markIntervalList,extracted)
            #b=compare(fingerprint,extracted)
            #improvement+=b-a

            return [extracted,emptyInterval]

def getNumberOfDetection(array):
    pass

def decodeFingerprint(fingerprint):

        tb_depth = coeficeient*(M.sum() + 1)
        arra=np.zeros(markFlowLength)
        for i in range(0,len(fingerprint)):
            #np.append(arra,i)
            arra[i]=fingerprint[i]
        trellis = cc.Trellis(M, generator_matrix)
        decoded_bits = cc.viterbi_decode(arra.astype(float), trellis, tb_depth)
#       print(decoded_bits)

        return decoded_bits
def compare(fingerprint,ext):
        numberOfCorrectPlaces=0
        #print fingerprint,"fingerprint"
        #print fingerprint
        #print len(fingerprint),len(ext),"erwddddddddd"

        for i in range(0,markFlowLength):
            #print(decodedFingerPrint[i],self.finger[i])
            if ext[i]==fingerprint[i]:
                numberOfCorrectPlaces+=1


        return numberOfCorrectPlaces
def extractMFlow(fileName,name):

        myreader = scapy.utils.PcapReader(os.path.join(os.path.dirname(os.path.realpath(__file__)), fileName))
        allTimings=[]
        first=0
        count=0
        flows=[]
        counter=0
        previousTime=0
        #tar=open("/home/fatemeh/nfq/timings/ethz/"+name+"/files"+str(counter)+".txt",'w')
        tar= open("/home/fatemeh/"+name+"/filesR200v"+str(counter)+".txt","w")
        for p in myreader:
            pkt = p.payload


            if isinstance(pkt.payload.payload,scapy.packet.Raw):
                        number=str(p.payload.payload.payload)
                        if count==0:
                            first=p.time
                            previousTime=p.time
                            #print p.show()
                            #print first,"dfdfd"
                            #print "kllllll"
                        #TODO I should write something for retransmission
                        allTimings.append((p.time-first)*1000)

                        #print str((p.time-first)*1000)
                        tar.write(str((p.time-first)*1000)+" ")
                        count+=1
                        if "end" in number or (p.time-previousTime)*1000>8000:
                            counter+=1
                            tar.close()
                            #tar=open("/home/fatemeh/nfq/timings/ethz/"+name+"/files"+str(counter)+".txt",'w')
                            tar= open("/home/fatemeh/"+name+"/filesR200v"+str(counter)+".txt","w")
                            flows.append(allTimings)
                            # if counter==101:
                            #     break
                            allTimings=[]
                        previousTime=p.time
                        #print p.time-first

        for i in range(0,len(allTimings)):
            if allTimings[i]==0:
                print i, "Packet lost"

        if len(allTimings)!=0:
            f=allTimings[0]
            print "heeeeeeeeeeeeeeeeee",len(allTimings)
            for i in range(0,len(allTimings)):
                 allTimings[i]-=f
            flows.append(allTimings)
        #print allTimings,"d"
        print len(flows),"len flows"
        return flows
def compareResultANdFingerprint():
    badFlows=[]
    allFingers=readFromFile('/home/fatemeh/Dropbox/codes/ethz19202.3R100.txt',"\n")
    print allFingers[0],"sdfd"

    finger=readFromFile("/home/fatemeh/Dropbox/NFQ/FingerPrintConv2.3.txt"," ")#ethz1920rate23R100.pcap
    extrN=[]
    #print finger
    print len(finger),"ddddddddddd"
    for k in range(0,len(allFingers)):
        fing=allFingers[k]
        #print fing
        fingArray=fing



        equ=0
        if len(fingArray)>20:
            for p in range(0,len(finger)):
            #print finger[p],fingArray[p],"lkkkkk"
                if finger[p]==fingArray[p]:
                    equ+=1

        if equ>=20:
            extrN.append(equ)
            badFlows.append(k)
    sum=0
    for k in range(0,len(extrN)):
        sum+=(extrN[k]/float(30))
    print extrN
    sum/=len(extrN)
    print "extr",sum

    #print badFlows
    return badFlows

def Main(resultFinger,name,badFlows):

    # this gives us array of flows
    #target=open("/home/fatemeh/ethz19202.3R100"+".txt",'w')
    target=open("/home/fatemeh/ethz216013R10r"+".txt",'w')
    #target=open("/home/fatemeh/ucla200210v4"+".txt",'w')
    #allTimings=extractMFlow("/home/fatemeh/tcp10UCLA0.5v2.pcap","ucla")
    #allTimings=extractMFlow("/home/fatemeh/ethz1920rate23.pcap","ethz")
    #allTimings=extractMFlow("/home/fatemeh/ethz1920rate23R100.pcap","ethz")
    allTimings=extractMFlow("/home/fatemeh/ethz216013rate10.pcap","ethz")
    #allTimings=extractMFlow("/home/fatemeh/fingerAllr10.pcap","ethz")
    improvement=0
    #print len(allTimings)
    decoded=[]

    for i in range(0,10+1):
        decoded.append(0)

    for i in range(0,len(allTimings)):


        #f=content
        f=allTimings[i]

        first=f[0]#I am not sure about this part
        for j in range(0,len(f)):
                 f[j]-=first

        if i in badFlows or i>=0:

            intrvals=getTlengthIntervals(f)
            markIntervalList=intrvals[0:markFlowLength]
            count=0
            for j in range(1,len(f)):
                if f[j]-f[j-1]>1000:
                    count+=1
            print "Flow Number: ", i

            nsteps=100
            stepLength=4

            if i in [17,31,39]:
                 nsteps=700
                 stepLength=1
                 #break
            '''else:
                continue'''



            ext,nEmp=getExtractedFingerprint(0,stepLength,nsteps,markIntervalList,improvement)
            if nEmp>0:
                print nEmp," Number of empty intervals"
                continue

            for k in range(0,len(ext)):
                target.write(str(ext[k])+" ")
            #print ext, "extracted"
            #decoded=decodeFingerprint(ext)
            target.write("M")
            target.write("\n")

            extraN=0
            for i in range(0,len(ext)):
                if ext[i] in messages:
                    extraN+=1
            resultFinger[extraN]+=1
            #$print ext
            #print fingerprint
            print len(ext),len(fingerprint),"m"
            print ext,"Number of extraction:", extraN,"Number of detection:", compare(fingerprint,ext)

            #resultFinger[compare(fingerprint,ext)]+=1
    target.close()
    return resultFinger
def getFlowTimings(fileName,name):
    allTimings=extractMFlow(fileName,name)

resultFinger=[]
array2=[]
for i in range(0,markFlowLength+1):
        resultFinger.append(0)
        array2.append(i)

improvement=0
#First get the timings
#extractMFlow("/home/fatemeh/nfq/nodes/ethz/newP/recN.pcap","newP")
re=Main(resultFinger,"ethz",[92,93])#TODO this is the last one

#badFlows=compareResultANdFingerprint()
#Main(resultFinger,"ucla",[29, 38, 67, 115, 118, 125, 129, 133, 137, 138])
#This is for false positive
#re=Main(resultFinger,"/home/fatemeh/jitterRates/ethz/rec10.pcap","newP")
[88,87,79,77,74,75,42,38,35,33,27,24,20,17]
