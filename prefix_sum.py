import numpy as np
import math


def summator(array, level, elements):
    for sum_index in elements:
        array[sum_index] = array[sum_index] + array[sum_index - pow(2, (level-1))]
    return array


def down_summator(array, level, elements):
    for sum_index in elements:
        val = array[sum_index]
        array[sum_index] = array[sum_index] + array[sum_index - pow(2, (level-1))]
        array[sum_index - pow(2, (level-1))] = val
    return array


def process(array, func, start, end, inc, max_cores):
    length = len(array)
    for level in range(start, end, inc):
        processing_field = pow(2, level)
        core_number = int(length / processing_field)
        if core_number > max_cores:
            core_number = max_cores
            processing_field = int(length / core_number)
        print("Level:", level, " Used cores:", core_number)
        for core in range(core_number):
            lbound = processing_field * core
            rbound = processing_field * (core + 1)
            elements = range(lbound + pow(2, level) - 1, rbound, pow(2, level))
            print("Level:", level, "   Core: ", core, "   Processing_field: ", processing_field, "   L: ", lbound, "   R: ", rbound, elements)
            func(array, level, elements)
    return array


def shift_bit_length(x):
    return 1 << (x-1).bit_length()


def pad(array):
    pad_left = shift_bit_length(len(array)) - len(array)
    return np.pad(array, (pad_left, 0), mode='constant')


def parallel_prefix_sum(array, max_cores=4):
    length = len(array)
    depth = math.ceil(math.log(length, 2))
    print("Depth:", depth)

    b = np.copy(array)
    b = process(b, summator, start=1, end=depth + 1, inc=1, max_cores=max_cores)
    b = np.insert(b, length - 1, 0)
    print("After summator:", b)
    b = process(b, down_summator, start=depth, end=0, inc=-1, max_cores=max_cores)
    print("After down summator:", b)


if __name__ == "__main__":
    initial = np.ones(15, dtype=np.int32)
    parallel_prefix_sum(pad(initial))
