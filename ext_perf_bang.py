import numpy as np
from keras.layers import Activation, Dropout, Dense, Input
from keras.layers import Conv1D, MaxPooling1D

from keras.layers.normalization import BatchNormalization
from keras.layers import Flatten
from keras.regularizers import l2
from keras.models import Model


def read_from_file(path):
    with open(path, 'r') as content_file:
        content = content_file.read()
        return content


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def convert_string_arrays_to_float_array(array):
    intArray = []

    for k in array:
        if isfloat(k):
            intArray.append(float(k))
    return intArray


def compute_extract_rate(keys, true_keys):
    correct = 0
    for i in range(len(keys)):

        if np.argmax(keys[i]) == np.argmax(true_keys[i]):
            correct += 1
    return correct / float(len(keys))


def compute_bit_rate_error(ext_keys, true_keys, n_bits):
    n_ext = 0
    for i in range(len(ext_keys)):
        ext = bin(np.argmax(ext_keys[i]))[2:].zfill(n_bits)
        true_k = bin(np.argmax(true_keys[i]))[2:].zfill(n_bits)
        b_er = 0  # bit error for each test_key
        try:
            for j in range(len(ext)):
                if ext[j] != true_k[j]:
                    b_er += 1
        except:
            print(j, "DDDDDDDDDDDDDDDDDD", ext)
        n_ext += b_er

    # bit_er = n_ext / (n_bits * len(ext_keys))
    # print('Bite rate error: ', bit_er, 'Bit rate ext rate: ', 1 - bit_er)
    return n_ext


def get_decoder(key_length, sample_size, layer, reg):
    Input_ipd = Input(shape=(sample_size, 1), name='input_dec_r')

    conv1 = Conv1D(filters=50, kernel_size=10, kernel_regularizer=l2(reg), padding='same', name='conv1')(Input_ipd)
    conv_b1 = BatchNormalization(name='conv_b1')(conv1)
    conv_r1 = Activation('relu', name='conv_r1')(conv_b1)
    conv_d1 = Dropout(0.3, name='conv_d1')(conv_r1)
    conv_m1 = MaxPooling1D(pool_size=1, name="conv_m1")(conv_d1)

    conv2 = Conv1D(filters=10, kernel_size=10, kernel_regularizer=l2(reg), padding='same', name='conv2')(conv_m1)
    conv_b2 = BatchNormalization(name='conv_b2')(conv2)
    conv_r2 = Activation('relu', name='conv_r2')(conv_b2)
    conv_d2 = Dropout(0.3, name='conv_d2')(conv_r2)
    conv_m2 = MaxPooling1D(pool_size=1, name="conv_m2")(conv_d2)

    flat2 = Flatten(name="flat2")(conv_m2)

    dense_1 = Dense(layer, kernel_regularizer=l2(reg), name='dense_1')(flat2)

    dense_b1 = BatchNormalization(name='dense_b1')(dense_1)
    dense_r1 = Activation('relu', name='dense_r1')(dense_b1)
    dense_d1 = Dropout(0.3, name='dense_d1')(dense_r1)

    key_hat = Dense(key_length, activation='softmax', name='key_hat')(dense_d1)

    decoder = Model(inputs=[Input_ipd], outputs=[key_hat])

    return decoder


def read_ext_ipds_for_decoding(path_for_key, path_for_ipds, flow_size):
    ext_ipds_all, true_keys = [], []
    ext_ipds = []

    for f in range(130):
        try:

            keys = read_from_file(path_for_key + str(f) + ".txt").split(" ")

            keys = convert_string_arrays_to_float_array(keys)

            if len(keys) == 0:
                print(f, "keys are empty")
                continue
            true_keys.append(keys)

            ext_ipds_string = read_from_file(path_for_ipds + str(f) + ".txt").split(" ")
            # ext_ipds_string = read_from_file(path + "ipd_fing/" + str(f) + ".txt").split(" ")
            ext_ipds = convert_string_arrays_to_float_array(ext_ipds_string)

            if len(ext_ipds) < flow_size:
                # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", f, len(ext_ipds))
                print(" flow length if smaller than 100")
                # last = ext_ipds[-1]
                # average = sum(ext_ipds)/float(len(ext_ipds))
                ext_ipds.extend([0] * (flow_size - len(ext_ipds)))

            # if we are using ipd_fing: 1: 1+flow_size, otherwise: :flow_size
            # ext_ipds_all.append(ext_ipds[1:1 + flow_size])
            ext_ipds_all.append(ext_ipds[: flow_size])
        except IOError:
            pass
            # print("IO error on ", f)

    if len(ext_ipds) != len(true_keys):
        print("Number of keys and ipds are different....")

    print("correct files", len(true_keys))
    ext_ipds_all = np.array(ext_ipds_all)
    ext_ipds_all = ext_ipds_all.reshape((-1, flow_size, 1))
    return true_keys, ext_ipds_all


def read_ipd_fing_for_decoding(path_for_key, path_for_ipds, flow_size):
    ext_ipds_all, true_keys = [], []
    ext_ipds = []

    for f in range(130):
        try:

            keys = read_from_file(path_for_key + str(f) + ".txt").split(" ")

            keys = convert_string_arrays_to_float_array(keys)

            if len(keys) == 0:
                print(f, "keys are empty")
                continue
            true_keys.append(keys)

            ext_ipds_string = read_from_file(path_for_ipds + str(f) + ".txt").split(" ")
            # ext_ipds_string = read_from_file(path + "ipd_fing/" + str(f) + ".txt").split(" ")
            ext_ipds = convert_string_arrays_to_float_array(ext_ipds_string)

            if len(ext_ipds) < flow_size:
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", f, len(ext_ipds))

                ext_ipds.extend([0] * (flow_size - len(ext_ipds)))

            # if we are using ipd_fing: 1: 1+flow_size, otherwise: :flow_size
            ext_ipds_all.append(ext_ipds[1:1 + flow_size])
            # ext_ipds_all.append(ext_ipds[: flow_size])
        except IOError:
            print("IO error on ", f)

    if len(ext_ipds) != len(true_keys):
        print("Number of keys and ipds are different....")

    print("correct files", len(true_keys))
    ext_ipds_all = np.array(ext_ipds_all)
    ext_ipds_all = ext_ipds_all.reshape((-1, flow_size, 1))
    return true_keys, ext_ipds_all


def compute_bit_rate(keys_true_server, keys_true_client, ground_truth, n_bits):
    std_match_real, correct_match = 0, 0
    std_somhow_match, correct_std_somhow_match = 0, 0
    not_match, correct_not_match = 0, 0
    k = 0
    non_corrupt_ar = []
    non_corrupt = 0
    p = 0
    # bit_rate_error = 0
    for j in range(0, n_test):
        ind = 0 + j
        ext_rate = compute_extract_rate(keys_true_server[j:j + 1], true_keys=true_keys[ind:ind + 1])
        ext_rate_client = compute_extract_rate(keys_true_client[j:j + 1], true_keys=true_keys[ind:ind + 1])

        diff = abs(float(real_stds[ind]) - float(train_stds[ind]))
        if ext_rate_client or (not ground_truth[j]):
            # it means nothing has been wrong on client side, and then we go to check server result.
            non_corrupt_ar.append(j)
            non_corrupt += 1
            bit = compute_bit_rate_error(keys_true_server[j:j + 1], true_keys[j:j + 1], n_bits)
            if diff < 5:
                std_match_real += 1.0
                correct_match += bit
            elif diff < 10:
                std_somhow_match += 1.0
                correct_std_somhow_match += bit
            else:
                not_match += 1.0
                correct_not_match += bit

            if ext_rate != 1:
                '''print(ind, ext_rate, 'real key: ', np.argmax(true_keys[ind]), '       ext key: ',
                      np.argmax(keys_true_server[j]),
                      real_stds[ind], train_stds[ind])'''
                k += 1
        else:
            # print("Wrong: ", np.argmax(true_keys[ind]), np.argmax(keys_true_server[ind]), j)
            # print("Corrupted file:", j)
            p += 1

    '''if std_match_real != 0:
        print("Bit rate Error when std match: ", correct_match / (std_match_real * n_bits), correct_match)

    if std_somhow_match != 0:
        print("Bit rate when std somehow match: ", correct_std_somhow_match / (std_somhow_match * n_bits),
              correct_std_somhow_match)

    if not_match != 0:
        print("Bit rate when std not match: ", correct_not_match / (not_match * n_bits), correct_not_match)'''

    print("Bit rate for all: ", (correct_match + correct_std_somhow_match) / (
            (std_match_real + correct_std_somhow_match) * n_bits))
    print(std_match_real, std_somhow_match, not_match)
    print("K: ", k, 'number of corrupted files: ', p)


def compute_ext(keys_true_server, keys_true_client, ground_truth):
    std_match_real, correct_match = 0, 0
    std_somhow_match, correct_std_somhow_match = 0, 0
    not_match, correct_not_match = 0, 0
    k = 0
    non_corrupt_ar = []
    non_corrupt = 0
    p = 0
    for j in range(0, n_test):
        ind = 0 + j
        ext_rate = compute_extract_rate(keys_true_server[j:j + 1], true_keys=true_keys[ind:ind + 1])
        ext_rate_client = compute_extract_rate(keys_true_client[j:j + 1], true_keys=true_keys[ind:ind + 1])
        diff = abs(float(real_stds[ind]) - float(train_stds[ind]))
        if ext_rate_client or (not ground_truth[j]):  # ext_rate or
            # it means nothing has been wrong on client side, and then we go to check server result.
            non_corrupt_ar.append(j)
            non_corrupt += 1
            if diff < 5:
                std_match_real += 1.0
                if ext_rate:
                    correct_match += 1
            elif diff < 10:
                std_somhow_match += 1.0
                if ext_rate:
                    correct_std_somhow_match += 1
            else:
                not_match += 1.0
                if ext_rate:
                    correct_not_match += 1

            if ext_rate != 1:
                '''print(ind, ext_rate, 'real key: ', np.argmax(true_keys[ind]), '       ext key: ',
                      np.argmax(keys_true_server[j]),
                      real_stds[ind], train_stds[ind])'''
                k += 1
                # print("ext failed: ", j, "result of ipd_fing: ", ground_truth[j])
        else:
            print("# of not known wrongs: ", np.argmax(true_keys[ind]), np.argmax(keys_true_server[ind]), j,
                  real_stds[j], train_stds[j])
            # print("Corrupted file:", j)
            p += 1

    '''if std_match_real != 0:
        print("Ext rate when std match: ", correct_match / std_match_real, correct_match, std_match_real)

    if std_somhow_match != 0:
        print("Ext rate when std somehow match: ", correct_std_somhow_match / std_somhow_match,
              correct_std_somhow_match, std_somhow_match)

    if not_match != 0:
        print("Ext rate when std not match: ", correct_not_match / not_match, correct_not_match, not_match)
    print("Ext rate when std match or somehow match: ", (correct_match + correct_std_somhow_match) / (
            std_match_real + correct_std_somhow_match))

        '''

    print("Ext rate for all: ", (correct_match + correct_std_somhow_match + correct_not_match) / (
            std_match_real + correct_std_somhow_match + not_match))

    print(std_match_real, std_somhow_match, not_match)
    print("K: ", k, 'number of corrupted files: ', p)


# print(non_corrupt_ar)


def check_decoder():
    date = '2020-06-10/'
    flow_size = 100
    model_decoder = get_decoder(key_length=1024, sample_size=flow_size, reg=1e-6)
    model_decoder.summary()
    model_decoder.load_weights(
        '/home/fatemeh/MyProjects/Fingerprint/' + date + 'decoder.h5')

    true_keys, ipd_fing = read_ext_ipds_for_decoding(
        path_for_ipds='/home/fatemeh/MyProjects/Fingerprint/' + date + "/ipd_fing/",
        path_for_key='/home/fatemeh/MyProjects/Fingerprint/' + date + "/true_keys/", flow_size=flow_size)
    ext_keys = model_decoder.predict([ipd_fing])
    p = 0
    for i in range(len(ext_keys)):
        if np.argmax(ext_keys[i]) == np.argmax(true_keys[i]):
            p += 1
        else:
            print(i, np.argmax(ext_keys[i]), np.argmax(true_keys[i]))
    print(p, len(ext_keys), 775 / 999.0)


def compute_ipd_fing_result(path_for_key, path_for_ipds):
    ext_rate = []
    std_array_test = np.random.uniform(2, 10, 1000)
    noise_for_test = get_fingerprinting_arrays(1000, std_array_test, flow_size)
    true_keys, ext_ipds = read_ipd_fing_for_decoding(path_for_key, path_for_ipds, flow_size)
    noise_for_test = noise_for_test.reshape((-1, flow_size, 1))
    ext_ipds = noise_for_test[0:len(ext_ipds)] + ext_ipds
    keys_true_ipd_fing = model_decoder.predict([ext_ipds])
    for i in range(len(keys_true_ipd_fing)):
        if np.argmax(keys_true_ipd_fing[i]) == np.argmax(true_keys[i]):
            ext_rate.append(1)
        else:
            ext_rate.append(0)
    return ext_rate


def get_fingerprinting_arrays(n_data, std_array, sample_size):
    noise = []
    for x in range(0, n_data):
        noise.append(np.random.laplace(0, 1.25 * std_array[x], sample_size));

    noise = np.array(noise)
    return noise


def get_stds(date, file_number):
    real_stds = read_from_file(
        '/home/fatemeh/MyProjects/Fingerprint/flow_length/100' + "/real_stds" + str(file_number) + ".txt").split(" ")
    train_stds = read_from_file(
        '/home/fatemeh/MyProjects/Fingerprint/flow_length/100' + "/train_stds.txt").split(" ")
    return real_stds, train_stds


# 1024 and 2048
# 1024, 4096, 8192, 16000

flow_size = 100
date = '0_cellular/nowater/1024'  # 'cellular/key_length/1024/'
file_num = ''  # 2
n_bit = 10
# date = 'Key_length/16000/'
std_array_test = np.random.uniform(2, 10, 1000)
noise_for_test = get_fingerprinting_arrays(1000, std_array_test, flow_size)
# def compute_ext_for_server():

key_len = 1024
real_stds, train_stds = get_stds(date, file_number='')

model_decoder = get_decoder(key_length=key_len, sample_size=flow_size, layer=128, reg=1e-6)
model_decoder.summary()
model_decoder.load_weights('/home/fatemeh/MyProjects/Fingerprint/' + 'flow_length/100' + '/decoder.h5')

import time

date2 = 'flow_length/100'
b = time.time()
ground_truth = compute_ipd_fing_result(
    path_for_key='/home/fatemeh/MyProjects/Fingerprint/' + date2 + "/true_keys/",
    path_for_ipds='/home/fatemeh/MyProjects/Fingerprint/' + date2 + "/ipd_fing/")

true_keys, ext_ipds_all_server = read_ext_ipds_for_decoding(
    path_for_ipds='/home/fatemeh/MyProjects/Fingerprint/' + date + "/ext_ipds/" + str(
        file_num) + "/server/",
    path_for_key='/home/fatemeh/MyProjects/Fingerprint/' + date2 + "/true_keys/", flow_size=flow_size)

_, ext_ipds_all_client = read_ext_ipds_for_decoding(
    path_for_ipds='/home/fatemeh/MyProjects/Fingerprint/' + date + "/ext_ipds/" + str(
        file_num) + "/client/",
    path_for_key='/home/fatemeh/MyProjects/Fingerprint/' + date2 + "/true_keys/", flow_size=flow_size)

keys_true_server = model_decoder.predict([ext_ipds_all_server])
keys_true_client = model_decoder.predict([ext_ipds_all_client])
print(len(keys_true_server), len(keys_true_client), "llllllllllllllllllllllllllll", len(ground_truth))

n_test = 95
compute_ext(keys_true_server, keys_true_client, ground_truth)
print('#############################################################################')
compute_bit_rate(keys_true_server, keys_true_client, ground_truth, n_bits=n_bit)
# 16000 , 4096
print(time.time() - b, "hhhhhhhhhhhhhhhhhhhhhhhhhhh")
'''
bangelore
cellular:
1024:  
Ext rate for all:  0.9272727272727272
61.0 16.0 35.0
K:  10 number of corrupted files:  18
#############################################################################
Bit rate for all:  0.04857142857142857
61.0 16.0 35.0
K:  10 number of corrupted files:  18
1024:

Ext rate for all:  0.8660714285714286
63.0 16.0 36.0
K:  18 number of corrupted files:  15
#############################################################################
Bit rate for all:  0.09567901234567901
63.0 16.0 36.0
K:  18 number of corrupted files:  15
4096

Ext rate for all:  0.7894736842105263
65.0 15.0 36.0
K:  26 number of corrupted files:  14
#############################################################################
Bit rate for all:  0.11145833333333334
65.0 15.0 36.0
K:  26 number of corrupted files:  14

Ext rate for all:  0.8390804597701149
46.0 11.0 31.0
K:  15 number of corrupted files:  42
#############################################################################
Bit rate for all:  0.055031446540880505
46.0 11.0 31.0

16384:
Ext rate for all:  0.5779816513761468
63.0 16.0 36.0
K:  52 number of corrupted files:  15
#############################################################################
Bit rate for all:  0.1645658263305322
63.0 16.0 36.0
K:  52 number of corrupted files:  15




nowater
1024:

Ext rate for all:  0.8181818181818182
41.0 13.0 36.0
K:  18 number of corrupted files:  15
#############################################################################
Bit rate for all:  0.10666666666666667
41.0 13.0 36.0

1024:

Ext rate for all:  0.7230769230769231
35.0 13.0 20.0
K:  21 number of corrupted files:  7
#############################################################################
Bit rate for all:  0.11538461538461539
4096:
Ext rate for all:  0.7126436781609196
43.0 14.0 36.0
K:  31 number of corrupted files:  12
#############################################################################
Bit rate for all:  0.11529680365296803
43.0 14.0 36.0
K:  31 number of corrupted files:  12
0.9650523662567139


16000
Ext rate for all:  0.5444444444444444
45.0 15.0 36.0
K:  47 number of corrupted files:  4
#############################################################################
Bit rate for all:  0.15614617940199335
45.0 15.0 36.0
K:  47 number of corrupted files:  4
'''
