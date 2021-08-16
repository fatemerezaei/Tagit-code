import numpy as np
import math
import matplotlib.pyplot as plt
from math import erf
from scipy.special import comb
from decimal import Decimal
plt.rcParams['xtick.labelsize'] = 40
plt.rcParams['ytick.labelsize'] =40
class porbability:
    def combinatior(self,x,y):
        #result+=self.combinatior(x,i)*math.pow(p,i)*math.pow(1-p,x-i)
        return comb(x, y, exact=False)
        result=1

        # for i in range(1,x+1):
        #     result*=i
        #
        # for i in range(1,x-y+1):
        #     result/=i
        # for j in range(1,y+1):
        #     result/=j

    def calcBernouli(self,p,x,y):
        result=0
        for i in range(y,x+1):
            result+=self.combinatior(x,i)*math.pow(p,i)*math.pow(1-p,x-i)
        return result
    def calcAllBernouli(self):
        array=[]
        array2=[]
        for i in range(1,20):
            pr=erf(i*0.2/math.sqrt(2))
            print(pr,i*0.2/math.sqrt(2))
            probalility=self.calcBernouli(pr,20,10)
            array.append(probalility)#probability of staying in the slot by adding delay
            array2.append(i*0.2*2)
        arrays=[]
        arrays.append(array)
        arrays.append(array2)
        return arrays

    def plotBernoulie(self):
        # arrays=self.calcAllBernouli()
        rates=[10]#,100]#,20,40]#100,200]#,100,200]#,100,200]
        landa="Rate="
        plt.figure(figsize=(5,5))
        lineType=["*-","s-",'o-']
        # lengend=[landa+'10pkt/sec',landa+'100pkt/sec',landa+'200pkt/sec']
        for k in range(0,len(rates)):
                arrays=self.calcFNCompletedFunction(1.2,rates[k])
                array2=arrays[1]
                array=arrays[0]
                plt.plot(array2, array,lineType[k],lw=4)

        plt.ylabel('Extraction rate (analysis)',fontsize=45)
        # plt.legend(lengend,fontsize=45,loc=4)
        plt.xlabel("Slot length (ms)",fontsize=45)
        plt.ylim(0,1.01)
        plt.show()
        return array,array2
    def plotFN(self,lineType,rate,pl):
                #stds=[0.25]#0.083,0.4,0.11,0.16,0.98,0.08,0.08,0.84,0.16]
                # stds=[20.241,23.091,28.13,20.6378,21.46615,25.3110,25.3193,24.769]
                # stds=[8]
                stds=[21]
                arr=[0,0,0,0,0,0]
                arrays=[]
                for k in range(0,len(stds)):
                    arrays=self.calcFNCompletedFunction(stds[k],rate)
                    print len(arrays[0]),len(arr)



                    for p in range(0,len(arrays[0])):
                        arr[p]+=arrays[0][p]

                for p in range(0,len(arr)):
                    arr[p]/=len(stds)
                array2=arrays[1]
                array=arrays[0]
                # pl.plot(array2, array,lineType,lw=4)

                plt.errorbar(array2,arr,lw=4,yerr=[0,0,0,0,0,0], fmt=lineType)


        #
    def calcBionomial(self, p, x, y):
        result=0
        for i in range(y,x+1):
            result+=self.combinatior(x,i)*math.pow(p,i)*math.pow(1-p,x-i)
        return result
    def phi(self,x):
        'Cumulative distribution function for the standard normal distribution'
        return (1.0 + erf(x / math.sqrt(2.0))) / 2.0
    def calcFNCompletedFunction(self,sd,rate):


        infin=8*rate
        # array2=[5,10,20,30,40,50]
        array2=[0.1,0.2,0.4,0.5,0.8,1]
        array2=[20,30,40,50,80,100]

        # array2=[20,30,40,50,80,100]
        # array2=[5,10,15,25,30,40]
        array=[0,0,0,0,0,0]
        nOfSlots=6
        numberOfSubIntervals=10


        # array2=[5,10,20,25,30,50,60,100,200,300]
        # array=[0,0,0,0,0,0,0,0,0,0]

        #
        # array2=[0.03,0.06,0.5,1,1.5,2,3,4,5]
        # array=[0,0,0,0,0,0,0,0,0]
        for j in range(1,infin):
            # prob=self.poissonProb(landa=intervalLength/100,k=j)#landa should be 18 since interval length was 1.8 sec
            for i in range(0,len(array)):
                coef=1#rate/10
                # print "ddddd"
                # lGu=numberOfSubIntervals*array2[i]*nOfSlots/100*coef
                prob=self.poissonProb(landa=(numberOfSubIntervals*array2[i]*nOfSlots/100)*coef,k=j)
                # prob=self.poissonProb(landa=24,k=j)
                # print 5*array2[i]*6/100, "kkkkkkkkkkkkkkkk"
                #print prob
               # print lGu, j
                step=array2[i]/float(sd)
                step/=2
                # pr1=erf(step*sd/(math.sqrt(2)*sd))#-erf(-1*step*sd/(math.sqrt(2)*sd))#we suppose packets are in the middle of interval

                pr=Decimal(self.phi(step)-self.phi(-1*step))
                # print pr,"kkkkkkkkkkkkkkkkkk"

                # pr-=0.42*array2[i]*6/intervalLength
                pr_flip=0#.15#(1-pr)*prob*self.FindFalsePostiveInterval(6)
                # print 0.42*array2[i]*6/intervalLength,pr
                #print pr,"Dddddddddd"

                if j%2==0:
                      probalility=Decimal(self.calcBionomial(pr, j, j / 2))
                else:
                    probalility=Decimal(self.calcBionomial(pr, j, j / 2 + 1))
                # probalility-=0.42*(sltL*6)/1800
                #print probalility*prob,"d"

                array[i]+=prob*probalility-pr_flip#probability of staying in the slot by adding delay

        print array
        return [array,array2]


    def FindFalsePostiveInterval(self, M):
        threshold=0.5

        result=0
        ininit=40

        for i in range(0,ininit):
            prob=self.poissonProb(landa=24,k=i)
            result+=prob*self.calcBionmialCDF(1/float(6),n=i,m=int(i*threshold))
        result*=M
        print result, "result"

        return result
    def drawFalsePositve(self):
        pass


    def calcBionmialCDF(self,p,n,m):
        result=0
        for i in range(0,m+1):
            result+=self.combinatior(n,i)*math.pow(p,i)*math.pow(1-p,n-i)

            result+=comb()
        return 1-result
    def poissonProb(self,landa,k):
        temp=Decimal(1)
        print landa,k
        temp*=Decimal(math.pow(landa,k))
        # for i in range(0,k):
        #      temp*=landa
        temp/=Decimal(math.pow((math.e),landa))
        # for k in range(0,landa):
        #     temp/=math.e

        temp/=Decimal(math.factorial(k))
        #
        # for i in range(1,k+1):
        #      temp/=i
        return temp


    def falseNegativeForFlow(self,a1,a2,nFlows):
        a1F=[]
        # plt.figure((5,5))
        for k in range(0,len(a1)):
            p=self.calcBionomial(a1[k], nFlows, nFlows/2)
            a1F.append(p)
        plt.ylabel('Extraction rate (analysis)',fontsize=45)
        # plt.legend(lengend,fontsize=45,loc=4)
        plt.plot(a2,a1F,'*-',lw=3)
        plt.xlabel("Slot length",fontsize=45)
        plt.ylim(0,1.01)
        plt.show()



p=porbability()
# a1,a2=p.plotBernoulie()
# print a1

# print math.factorial(300)
# print Decimal(math.factorial(2000))
# print comb(800, 414, exact=False)
# print a2
# p.falseNegativeForFlow(a1,a2,30)
#v=p.calcBernouli(0.76,20,10)
#print(v)
points=[0.25,0.5,0.75,1,1.25,1.5,1.75,2]
# print p.phi(2)-p.phi(-2)
# for k in points:
#     print p.phi(k)-p.phi(-1*k)
#re=p.calcBionmialCDF(1/float(6),20,10)
#bits that we insert?
#This is false postive
# for k in range(1,5):
#     re=p.FindFalsePostiveInterval(2*6*k)
    # print p.FindFalsePostiveFlow(re,30,15), "Flase Postive flow"
