#!/usr/bin/python
# need root privileges
import struct
import Interval
import sys

sys.path.append('python')
sys.path.append('build/python')
# import nfqueue
sys.path.append('dpkt-1.6')
from scapy.all import *


def getNumbers(array):
    result = []
    for i in range(0, len(array) - 1):
        result.append(int(float(array[i])))
    return result


def getPermuations(perm):
    result = []

    for i in range(0, len(perm) - 1):
        temp = perm[i]
        permTemp = []
        permTemp.append(int(temp[1]))
        permTemp.append(int(temp[4]))
        permTemp.append(int(temp[7]))
        # permTemp.append(int(temp[10]))
        # permTemp.append(int(temp[13]))

        result.append(permTemp)
    return result


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def readFromFile(fileName):
    content = ""
    with open(fileName, 'r') as content_file:
        content = content_file.read()
    values = content.split(" ")
    # print len(values)

    return values


def readIntFromFile(fileName):
    content = ""
    with open(fileName, 'r') as content_file:
        content = content_file.read()
    values = content.split(" ")
    print(len(values[0]), "le", values)
    numbers = []
    for i in range(0, len(values)):
        if isfloat(values[0]):
            numbers.append(int(float(values[i])))
    # print numbers,"d"
    '''allFingers=[]
    for k in range(0,30):
         l=numbers[k*4:(k+1)*4]
        val=0
        for p in range(0,4):
            val+=l[p]*math.pow(2,3-p)

        #print l
        allFingers.append(val)'''

    # return allFingers
    return numbers


# 0 0 0 1 1 1 1 1 0 0 1 1 1 1 1 1 1 0 0 1 1 0 0 0 1 1 1 1 1 0
def getTheParameters():
    output = []
    perms = []
    fingerprint = readIntFromFile("/home/fatemeh/Documents/PycharmProjects/TagIt/NFQ/FingerPrintConv.txt")
    # fingerprint=readIntFromFile("/home/fatemeh/Dropbox/NFQ/fingerprintReed")
    for i in range(0, 32):
        perm = readFromFile("/home/fatemeh/Documents/PycharmProjects/TagIt/NFQ/permutations/perm" + str(i) + ".txt")
        perms.append(perm)
    # permutzero=getPermuations(permutations)

    output.append(perms)

    print(fingerprint, "fingerprint", len(fingerprint))

    output.append(fingerprint)

    # output.append(permut)
    # print len(permut),"len"
    return output


def printArray(array):
    for i in range(0, len(array)):
        print(array[i])
