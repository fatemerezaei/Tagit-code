def read_ground_truth(interval_length):
    path = '/home/fatemeh/MyProjects/Fingerprint/0_tagit/ipds/10-25/'
    number_of_bits_sent = []

    for i in range(500):
        try:
            # print("Flow: ", i)
            flow = readFromFile(path + str(i) + '.txt', " ")
            times = []
            t = 0
            num_packet_in_interval = [0] * 20

            for j in range(100):
                times.append(t)
                t += float(flow[j])
            for time in times:
                num_packet_in_interval[int(time / float(interval_length))] += 1
            whole_rate = 0
            non_empty_intervals = 0
            for k in range(len(num_packet_in_interval)):
                if num_packet_in_interval[k] != 0:
                    whole_rate += num_packet_in_interval[k]
                    non_empty_intervals += 1
            # print(whole_rate, non_empty_intervals)
            # print(num_packet_in_interval,non_empty_intervals)

            whole_rate /= float(non_empty_intervals)
            # print(whole_rate, non_empty_intervals)
            number_of_bits_sent.append(non_empty_intervals)
        except:
            pass

    return number_of_bits_sent


def compute_duration_ground_truth(interval_length):
    path = '/home/fatemeh/MyProjects/Fingerprint/0_tagit/ipds/10-25/'
    num_of_intervals = []
    for i in range(500):
        try:
            # print("Flow: ", i)
            duration = 0
            flow = readFromFile(path + str(i) + '.txt', " ")
            # print(len(flow), 'EDDDDDDDDDDDDDD')
            for f in range(100):
                duration += float(flow[f])
            num_of_intervals.append(int(duration / interval_length))

            # print(len(flow), duration, int(duration/2160))
        except:
            pass
    return num_of_intervals


import random


def generate_fingerprint(length):
    finger = []
    for _ in range(length):
        finger.append(random.randint(0, 1))

    return finger


def write_array_to_file(array, path, delimiter):
    target = open(path, 'w')
    for k in range(0, len(array)):
        target.write(str(array[k]) + delimiter)
    target.write("\n")


def build_fingerprint_dataset():
    path = '/home/fatemeh/MyProjects/Fingerprint/NFQ/fings/1_'

    for i in range(300):
        finger = generate_fingerprint(length=30)
        write_array_to_file(finger, path + str(i) + ".txt", " ")


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def convert_stringArrays_to_floatArray(array):
    intArray = []

    for k in array:
        if isfloat(k):
            intArray.append(int(k))
    return intArray


def compute_exxt_result():
    fingerprint = [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0]
    ext_server = readFromFile("/home/fatemeh/MyProjects/Fingerprint/0_tagit/ext_result/2160_10_all_fing.txt", "\n")
    interval_length = 2160
    ground_truth = read_ground_truth(interval_length=interval_length)
    num_of_intervals = compute_duration_ground_truth(interval_length=interval_length)
    n_of_all_bits = n_lost_bits = ext_rate = average_bits_sent = num_ext_fing = 0
    N = len(ext_server)
    for i in range(N - 1):
        fingerprint = convert_stringArrays_to_floatArray(
            readFromFile('/home/fatemeh/MyProjects/Fingerprint/NFQ/fings/' + str(i+1) + '.txt', ' '))

        try:

            n_of_intervals = num_of_intervals[i]  # int(ground_truth[i])#
            n_of_all_bits += n_of_intervals  # num_of_intervals[i]  # int(ground_truth[i])  # to compute bit_rate_error
            ext = ext_server[i].split(" ")[:-1]
            num_ext_bit = 0
            # print(len(ext),n_of_intervals)
            print(fingerprint)
            print(ext)
            print("#############################")
            for j in range(n_of_intervals):
                if ext[j] != 'N' and int(ext[j]) == fingerprint[j]:
                    num_ext_bit += 1
            if n_of_intervals > num_ext_bit:
                n_lost_bits += (n_of_intervals - num_ext_bit)
            if num_ext_bit == n_of_intervals:
                ext_rate += 1

                average_bits_sent += n_of_intervals
            num_ext_fing += 1
        #  print(ext, num_ext_bit, ground_truth[i], n_of_intervals, 'i:  ', i)

        except:
            pass
    print("average bits sent: ", average_bits_sent / float(num_ext_fing))
    ext_rate /= float(N - 1)
    bit_rate_error = n_lost_bits / n_of_all_bits

    print(ext_rate, bit_rate_error, 'num of flows:', N)


def compute_exxt_result_all():
    fingerprint = [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0]
    files = ['2160_10.txt', '1620_10.txt', '1080_5.txt', '1080_10.txt']  # , '2160_20.txt',
    n_of_all_bits = 0
    n_lost_bits = 0
    ext_rate = 0
    average_bits_sent = 0
    N = 0
    e = 0
    for f in files:
        ext_server = readFromFile("/home/fatemeh/MyProjects/Fingerprint/0_tagit/ext_result/" + f, "\n")
        ground_truth = read_ground_truth()
        num_of_intervals = compute_duration_ground_truth()
        # print(ground_truth)

        N += len(ext_server)

        for i in range(N - 1):
            try:
                n_of_all_bits += int(ground_truth[i])  # to compute bit_rate_error
                ext = ext_server[i].split(" ")
                b = 0
                n_of_intervals = num_of_intervals[i]  # 100 // ground_truth[i] + 1

                for j in range(len(ext) - 1):
                    if j < len(fingerprint):
                        if ext[j] != 'N' and int(ext[j]) == fingerprint[j]:
                            b += 1
                if n_of_intervals > b:
                    n_lost_bits += (n_of_intervals - b)
                if b >= n_of_intervals:
                    ext_rate += 1
                    e += 1
                    average_bits_sent += n_of_intervals
                # print(ext, n_of_intervals, b, ground_truth[i])
            except:
                pass
    print("average bits sent: ", average_bits_sent / float(e))
    ext_rate /= float(N)
    bit_rate_error = n_lost_bits / (n_of_all_bits * 5)

    print(ext_rate, bit_rate_error, N)


def readFromFile(path, delimiter):
    with open(path, 'r') as content_file:
        content = content_file.read()
        # print content
        c = content.split(delimiter)

    return c


# build_fingerprint_dataset()
# compute_duration_ground_truth()

compute_exxt_result()
