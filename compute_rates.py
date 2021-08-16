import socket
import time


def read_from_file(file_path):
    with open(file_path, 'r') as content_file:
        content = content_file.read()
    return content


def read_all_files(address):
    all_ipds = []
    for f in range(1000):
        numbers = read_from_file(address + str(f) + ".txt").split(" ")
        all_ipds.append(numbers[:-1])
    return all_ipds


def write_array_to_file(array, path, delimiter):
    target = open(path, 'w')
    for k in range(0, len(array)):
        target.write(str(array[k]) + delimiter)
    target.close()


path = '/home/fatemeh/MyProjects/Fingerprint/0_tagit/ipds/10-25/'
all_flows = read_all_files(address='/home/fatemeh/MyProjects/Fingerprint/Key_length/1024/test_ipds/')
# rate_per_sec = [0] * 500
rate_10 = 0
for i in range(500):
    times = []
    t = 0
    rate_per_sec = [0] * 40

    for j in range(100):
        times.append(t)
        t += float(all_flows[i][j])
    for time in times:
        # print(int(time))
        rate_per_sec[int(time / float(1000))] += 1
    whole_rate = 0
    p = 0
    for k in range(len(rate_per_sec)):
        if rate_per_sec[k] != 0:
            whole_rate += rate_per_sec[k]
            p += 1
    whole_rate /= float(p)
    if 5 < whole_rate < 25:
        write_array_to_file(all_flows[i], path + str(i) + ".txt", delimiter=" ")
        rate_10 += 1

    print(' flow i', i, "  Rate for flow: ", whole_rate, "Number of seconds:", p)
    # print(rate_per_sec)
print("Number of rate 10 flows:", rate_10)
def read_folder():
    import os
    path = '/home/fatemeh/MyProjects/Fingerprint/0_tagit/ipds/10-25/'
    files = os.listdir(path)
    numbers = []
    for f in files:
        numbers.append(int(f[:-4]))
    sorted_numbers = sorted(numbers)
    print(sorted_numbers)
read_folder()
