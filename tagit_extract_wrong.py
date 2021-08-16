import nf2
import dpkt
from scapy.all import *
import os

permutZero = []
input = nf2.getTheParameters()
markFlowLength = 5
fingerprint = input[1][:markFlowLength]
print("My Fingerprint: ", fingerprint)
permutations = input[0]
# print("permutations: ", permutations[:5])
threshold = 0.2
baseIntervalList = []
markIntervalList = []
# system parameters
intervalLength = 2160
numberOfSlots = 6
subintervalLength = 120  # intervalLength / float(numberofSubintervals)
numberofSubintervals = intervalLength / subintervalLength  # 20*2*2

mslotLength = intervalLength / float(numberofSubintervals * numberOfSlots)
print(mslotLength, subintervalLength)

improvement = 0


def minusMeanDealy(mark, mean):
    for i in range(0, len(mark)):
        inte = mark[i]
        for j in range(0, len(inte)):
            inte[j] -= mean


def write_intervals_to_files(mark, name):
    placeM = []  # markIntervals
    for i in range(0, markFlowLength):
        placeM.append(i)
    target = open(name, 'w')

    count = -1
    while True:
        found = 0

        if count == 37:
            target.close()
            break
        if found == 0:
            for i in range(0, len(placeM)):
                if placeM[i] == count:
                    inter = mark[i]
                    # print mark[i],i
                    for j in range(0, len(inter)):
                        target.write(str(inter[j]))
                        target.write("#")
                    break
        count += 1


def try_different_offsets(offset, desI, markIntervalList):
    # print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
    fileName2 = "first"
    # print(markIntervalList)
    minusMeanDealy(markIntervalList, offset)
    # print('fffffffffffffff',markIntervalList)

    fileName2 += str(desI) + "rec" + ".txt"
    write_intervals_to_files(markIntervalList, fileName2)

    con = read_from_file(fileName2)
    # print("kkkkkkkkkkkk", con)

    intervals2 = get_T_length_intervals(con)
    markIntervalList = intervals2[0:markFlowLength]
    print(len(markIntervalList),"DD")
    extracted = extract_finger(markIntervalList)  # error
    # print(markIntervalList)
    return extracted


def read_from_file(path):
    content = ""
    c = ""
    with open(path, 'r') as content_file:
        content = content_file.read()
        # print(content)
        c = content.split("#")
    for i in range(0, len(c)):
        if isfloat(c[i]):
            c[i] = float(c[i])
            # print c[i]
        else:
            c[i] = 0
            # print c[i],";"
    return c


def get_T_length_intervals(content):
    # print(content)
    numbers = content

    intervalList = []
    for i in range(0, markFlowLength):
        intervalList.append([])

    upperBound = intervalLength
    i = 0
    condition = True
    count = 0
    while condition:
        # print numbers[i]
        if upperBound == intervalLength + markFlowLength * intervalLength:
            break
        # print numbers[i],i

        if i >= len(numbers) or not isfloat(numbers[i]):  # this means we are in the end of our file
            break

        if i < len(numbers) and float(numbers[i]) < upperBound:
            intervalList[count].append(float(numbers[i]))  # ????///
            i += 1
            if i == len(numbers):
                break
        else:
            upperBound += intervalLength
            count += 1
    # print "intervals lIst"
    # print intervalList

    return intervalList


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def random_extract(inter, center, i):
    # print inter
    count = 0
    counter = 0
    # print inter,"inter"
    msLotLength = intervalLength / float(numberOfSlots * numberofSubintervals)
    centroid = center
    allpackets = len(inter)
    if len(inter) < 2:
        return ["Zero", 0]

    numberOfInterval = int(inter[0] / intervalLength)
    lowerBound = intervalLength * numberOfInterval
    upperBound = lowerBound + subintervalLength  # subinterval
    numberOfCorrectOnes = 0
    numberOfCorrectZeros = 0
    currentSubinterval = 0
    nu = 0
    # print msLotLength,subintervalLength,numberofSubintervals,lowerBound,upperBound
    for j in range(0, len(inter)):
        nu += 1
        while (True):  # ????currentsubinter=0?
            if (inter[j] >= lowerBound and inter[j] < upperBound):
                counter += 1
                index = int(i * numberofSubintervals + currentSubinterval)
                # print(permutations[0])
                print(index, centroid, len(permutations), len(permutations[0]))

                location = int(permutations[index][centroid])
                # print(location,"ll",type(location))
                # print(type(inter[j]), type(location), type(msLotLength), type(lowerBound))
                if inter[j] >= location * msLotLength + lowerBound \
                        and inter[j] < lowerBound + (location + 1) * msLotLength:
                    numberOfCorrectOnes += 1

                locSp = location
                # print locSp, "location for zero"
                if location < 3:
                    locSp += 2
                else:
                    locSp -= 2
                if inter[j] >= locSp * msLotLength + lowerBound \
                        and inter[j] < lowerBound + (locSp + 1) * msLotLength:
                    numberOfCorrectZeros += 1
                lowerBound -= subintervalLength  # o
                upperBound -= subintervalLength
                currentSubinterval -= 1  # ??

                break
            else:
                # print(currentSubinterval, "No packet in this subinterval")
                lowerBound = upperBound
                upperBound += subintervalLength  # subintervalLength
                currentSubinterval += 1
                if currentSubinterval == numberofSubintervals:  # order???
                    currentSubinterval = 0
                    break
                if upperBound > markFlowLength * intervalLength + 1000:  # ???#stupid mistake
                    break
                count += 1

    numberAllPackets = len(inter)
    # print nu,"Sdsddd",numberAllPackets

    # I should check if the intersection of these four if's are not zero...
    if numberOfCorrectOnes >= threshold * numberAllPackets:  # threshold is not enough
        # print numberOfCorrectOnes,numberOfCorrectZeros,numberAllPackets
        return [1, numberOfCorrectOnes]
    elif numberOfCorrectZeros >= threshold * numberAllPackets:
        # print numberOfCorrectOnes,numberOfCorrectZeros,numberAllPackets
        return [0, numberOfCorrectZeros]
    else:
        # print numberOfCorrectOnes,numberOfCorrectZeros,numberAllPackets
        return ["None", 0]


def extracRandFingerprintNewM(inter, center, i):
    count = 0
    counter = 0
    # print inter,"inter"
    msLotLength = intervalLength / (numberOfSlots * numberofSubintervals)
    centroid = center
    allpackets = len(inter)
    if len(inter) == 0:
        return "Zero"

    numberOfInterval = int(inter[0] / intervalLength)
    lowerBound = intervalLength * numberOfInterval
    upperBound = lowerBound + subintervalLength  # subinterval
    numberOfCorrectOnes = 0
    numberOfCorrectZeros = 0
    currentSubinterval = 0
    numberOfNull = 0
    # print len(inter),i," h",type(inter[0])
    # print len(inter), "lengt"
    for j in range(0, len(inter)):
        # print inter[j],"j"
        while (True):  # ????currentsubinter=0?
            if (inter[j] >= lowerBound and inter[j] < upperBound):
                counter += 1

                location = permutations[i * numberofSubintervals + currentSubinterval][centroid]
                # print(location,"ll",type(location))
                locSp = permutZero[i * numberofSubintervals + currentSubinterval][centroid]
                if inter[j] >= location * msLotLength + lowerBound \
                        and inter[j] < lowerBound + (location + 1) * msLotLength:
                    numberOfCorrectOnes += 1

                elif inter[j] >= locSp * msLotLength + lowerBound \
                        and inter[j] < lowerBound + (locSp + 1) * msLotLength:
                    numberOfCorrectZeros += 1
                else:
                    numberOfNull += 1
                lowerBound -= subintervalLength  # o
                upperBound -= subintervalLength
                currentSubinterval -= 1  # ??

                break
            else:
                # print(currentSubinterval, "No packet in this subinterval")
                lowerBound = upperBound
                upperBound += subintervalLength  # subintervalLength
                currentSubinterval += 1
                if currentSubinterval == numberofSubintervals:  # order???
                    currentSubinterval = 0
                    break
                if upperBound > markFlowLength * 2 * intervalLength:  # ???#stupid mistake
                    break
                count += 1

    numberAllPackets = len(inter)
    # print numberAllPackets
    # print(inter.getlen())

    # I should check if the intersection of these four if's are not zero...
    if numberOfCorrectOnes > threshold * numberAllPackets:  # threshold is not enough
        # print numberAllPackets
        # print(numberOfCorrectOnes, "One",numberAllPackets,"Index: ",location,center),i
        # print numberOfCorrectOnes,numberAllPackets
        return [1, numberOfCorrectOnes]
    elif numberOfCorrectZeros > threshold * numberAllPackets:
        return [0, numberOfCorrectZeros]
    else:
        # print numberOfCorrectOnes,numberOfCorrectZeros,numberAllPackets
        return ["Null", 0]


def extract_one_bit(inter, index):  # (self,inter,center,i):
    finger = []
    # print index
    corr = []
    for i in range(0, 5):  # numberOfSlots???
        finCor = random_extract(inter, i, index)  # this can have newM
        finger.append(finCor[0])
        corr.append(finCor[1])
    max = 0
    pind = 0
    for i in range(0, len(finger)):

        if corr[i] >= max:
            max = corr[i]
            pind = i

    # print index,finger,corr,len(inter)

    if max < 0.2 * len(inter):
        return "None"
    return finger[pind]


def extract_finger(markIntervalList):
    # fingerLoc=self.fingerPrintLoc#threshold check
    # we have to check it with baseinterval, center,....
    extractedFingerPrint = []
    count = 0
    for i in range(0, len(markIntervalList)):  # fingerPrintLength
        inter = markIntervalList[i]
        if len(inter) == 0:
            count += 1
        l = extract_one_bit(inter, i)
        extractedFingerPrint.append(l)
    # print(extractedFingerPrint, 'Exxxxxxxxxxxxxxxxx', count)
    return [extractedFingerPrint, count]


def findMax(array):
    index = 0
    max = array[0]
    for i in range(0, len(array)):
        if max < array[i]:
            max = array[i]
            index = i
    return index


def calcNumberOfNuls(extracted):
    numOfNull = 0
    if extracted != None:
        for l in range(0, len(extracted)):
            if extracted[l] == 2 or extracted[l] == "None" or extracted[l] == 3:
                numOfNull += 1
    # print numOfNull, "numberOFNull"
    return numOfNull


def addDelay(mark, amount):
    minusMeanDealy(mark, -1 * amount)


def tryIntervalOffsetInterval(inter, index):
    extractedBit = []
    for i in range(0, int(mslotLength)):
        # print i/2.0
        for j in range(0, len(inter)):
            inter[j] -= (i)
            f = extract_one_bit(inter, index)
            extractedBit.append(f)
    for i in range(0, int(mslotLength)):
        for j in range(0, len(inter)):
            inter[j] += (i)
            f = extract_one_bit(inter, index)
            extractedBit.append(f)
    numOfZero = 0
    numberOfOne = 0
    for i in range(0, len(extractedBit)):
        if extractedBit[i] == 0:
            numOfZero += 1
        elif extractedBit[i] == 1:
            numberOfOne += 1
    # print "number Of zero: ", numOfZero
    # print "number of One: ", numberOfOne
    if numberOfOne > numOfZero:
        return 1
    if numOfZero > numberOfOne:
        return 0


def tryInternalOffset(markList, extr):
    for i in range(0, len(markList)):
        if extr[i] == 4:
            inter = markList[i]
            k = tryIntervalOffsetInterval(inter, i)
            extr[i] = k
            # k=extractOneBit(inter,i)

    return extr


def get_extracted_fingerprint(desI, step, numberOfSteps, markIntervalList, improvement):
    #
    numOfPackets = 0
    for i in range(0, len(markIntervalList)):
        numOfPackets += len(markIntervalList[i])
    # print("Number Of Packets:", numOfPackets)

    numberOfNoneFingerprinted = 0
    numberOfFingerprinted = 0
    mean = 0  # TODO think: why mean should be zero?
    offsets = []
    extractedFingers = []
    numberOfNulls = []
    numberOfEmptyIntervals = []
    for k in range(0, numberOfSteps):
        # print "hey First"

        newMean = mean - k * step
        offsets.append(newMean)
        e = try_different_offsets(newMean, desI, markIntervalList)

        addDelay(markIntervalList, -k * step)
        extractedFingers.append(e[0])
        numberOfEmptyIntervals.append(e[1])
        numberOfNull = calcNumberOfNuls(e[0])
        numberOfNulls.append(numberOfNull)

    min = markFlowLength
    subtractValue = mean
    selectedFingerprints = []
    selectedOffsets = []

    for p in range(0, len(extractedFingers)):
        if numberOfNulls[p] <= min:
            min = numberOfNulls[p]
            subtractValue = offsets[p]

    slectedNumberOfEmpties = []
    for p in range(0, len(extractedFingers)):
        if numberOfNulls[p] == min:
            selectedFingerprints.append(extractedFingers[p])
            selectedOffsets.append(offsets[p])
            slectedNumberOfEmpties.append(numberOfEmptyIntervals[p])

    # TODO
    number_of_zeros = [0 for _ in range(markFlowLength)]
    number_of_ones = [0 for _ in range(markFlowLength)]
    extracted = [0 for _ in range(markFlowLength)]

    # print len(selectedFingerprints),"selected Fingerprints",slectedNumberOfEmpties[0]
    for j in range(0, len(selectedFingerprints)):
        for k in range(0, markFlowLength):
            if selectedFingerprints[j][k] == 0:
                number_of_zeros[k] += 1
            elif selectedFingerprints[j][k] == 1:
                number_of_ones[k] += 1

    for j in range(0, markFlowLength):
        # print numberOfOnes[j],numberOfZeros[j],j,len(selectedFingerprints)
        if number_of_zeros[j] >= 0.2 * len(selectedFingerprints):

            extracted[j] = 0
        elif number_of_ones[j] >= 0.2 * len(selectedFingerprints):
            extracted[j] = 1
        else:
            extracted[j] = 4

    nullNum = 0
    for j in range(0, len(extracted)):
        if extracted[j] == 4:
            nullNum += 1

    try_different_offsets(subtractValue, desI, markIntervalList)
    # for r in range(0,markFlowLength):
    #     print markIntervalList[r], r ,len(markIntervalList[r])

    numOfPackets = 0
    for i in range(0, len(markIntervalList)):
        numOfPackets += len(markIntervalList[i])
    print("Number Of Packets:", numOfPackets)

    if nullNum >= markFlowLength / 2:
        numberOfNoneFingerprinted += 1
        return extracted
        # it finishes here...
    else:
        numberOfFingerprinted += 1
    # TODO there should be a change
    for i in range(0, markFlowLength):
        if number_of_zeros[i] > number_of_ones[i]:
            extracted[i] = 0
        elif number_of_zeros[i] <= number_of_ones[i] and number_of_ones[i] != 0:
            extracted[i] = 1
        else:
            extracted[i] = 4

    a = compare(fingerprint, extracted)

    extracted = tryInternalOffset(markIntervalList, extracted)
    print(extracted, 'extracted fingerprint ffffffff')
    b = compare(fingerprint, extracted)
    improvement += b - a
    # print b-a, "improment"

    return extracted


def compare(fingerprint, ext):
    numberOfCorrectPlaces = 0

    for i in range(0, markFlowLength):
        # print(decodedFingerPrint[i],self.finger[i])
        if ext[i] == fingerprint[i]:
            numberOfCorrectPlaces += 1

    return numberOfCorrectPlaces


def read_pcap_data(pcap_file):
    bitcoin_traffic = open(pcap_file, "rb")
    pcap = dpkt.pcap.Reader(bitcoin_traffic)
    all_flows = []
    flow = []
    count = 0
    counter = 0
    prev_time, first = 0, 0
    for ts, pkt in pcap:
        try:
            if count == 0:
                prev_time = ts
                first = ts

            count += 1
            if ts - prev_time > 10:
                all_flows.append(flow)
                print("Counter: ", counter, len(flow))
                flow = []
                count = 1
                counter += 1
                if counter == 3:
                    break
            flow.append((ts - first) * 1000)
            prev_time = ts

        except:
            pass
        if len(flow) != 0:
            all_flows.append(flow)
    # print(all_flows)
    return all_flows


def extractMFlow(fileName):
    myreader = PcapReader(os.path.join(os.path.dirname(os.path.realpath(__file__)), fileName))
    flow = []
    first = 0
    count = 0
    all_flows = []
    counter = 0
    # tar=open("/home/fatemeh/timings/purdue/"+name+"/file"+str(counter)+".txt",'w')
    for p in myreader:
        pkt = p.payload

        if isinstance(pkt.payload.payload, scapy.packet.Raw):
            number = str(p.payload.payload.payload)
            if count == 0:
                first = p.time
            # TODO I should write something for retransmission
            flow.append((p.time - first) * 1000)
            # tar.write(str((p.time-first)*1000)+" ")
            count += 1
            if "e nd" in number or "end" in number:
                counter += 1
                # tar.close()
                # tar=open("/home/fatemeh/timings/purdue/"+name+"/file"+str(counter)+".txt",'w')
                all_flows.append(flow)
                flow = []

    if len(flow) != 0:
        f = flow[0]
        for i in range(0, len(flow)):
            flow[i] -= f
        all_flows.append(flow)
    return all_flows


def divide_pcap_to_flows(timing):
    ipds_all, ipds = [], []
    # I am not sure if I need to count the retransmission packets which are in middle of flows or not.
    i = 1
    ipds.append(timing[0] * 1000)
    while i < len(timing):

        if timing[i] - timing[i - 1] > 10:
            ipds_all.append(ipds)
            ipds = []
        ipds.append(timing[i] * 1000)

        i += 1

    return ipds_all


def read_pcap_file(pcap_file):
    bitcoin_traffic = open(pcap_file, "rb")
    pcap = dpkt.pcap.Reader(bitcoin_traffic)
    all_flows = []
    flow = []
    for ts, pkt in pcap:
        try:
            flow.append(ts)
        except:
            pass

    return flow


def Main(resultFinger, file_name):
    # rec4,7,8,9:3*2000 rec5,6: 4*2000
    timings = read_pcap_file(file_name)  # this gives us array of flows
    target = open("/home/fatemeh/MyProjects/Fingerprint/0_tagit/ext_result/ext.txt", 'w')
    flows = divide_pcap_to_flows(timings)

    print("Number of flows: ", len(flows), len(flows[0]))
    # print(all_flows)

    # target=open("/home/fatemeh/pur"+name+".txt",'w')

    # print len(allTimings)," :NumberOf the flows"
    improvement = 0
    for i in range(0, 10):
        flow = flows[i]
        # print(f[:14],"FFFFFFF")
        print("Flow Number: ", i)
        # we should have this line for real data with jitter
        first = flow[0]  # I am not sure about this part
        # print f[0],content
        # print("first: ", first, flow)
        for j in range(0, len(flow)):
            flow[j] -= first
        print(flow)

        intrvals = get_T_length_intervals(flow)
        print('# of intervals: ', len(intrvals))
        markIntervalList = intrvals  # [0:markFlowLength]

        count = 0
        for j in range(0, len(flow)):
            if flow[j] - flow[j - 1] > 1000:
                count += 1

        # print("Number Of packets that have 1 sec or more distance: ", count)

        ext = get_extracted_fingerprint(0, 1/5.0, 50, markIntervalList, improvement)
        for k in range(0, len(ext)):
            target.write(str(ext[k]) + " ")
        target.write("\n")
        print(ext, 'extracted fingerprint')
        print(ext, "Number of finn:", compare(fingerprint, ext))

        resultFinger[compare(fingerprint, ext)] += 1
    target.close()
    return resultFinger


resultFinger = []
for i in range(0, 10):
    resultFinger.append(0)

# re=Main(resultFinger,"/home/fatemeh/nfq/purdue/rec20E1.pcap","20E1")
re = Main(resultFinger, "/home/fatemeh/MyProjects/Fingerprint/0_tagit/pcaps/client.pcap")
