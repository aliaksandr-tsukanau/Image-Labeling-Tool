import numpy as np


def labels_to_one_hot(labels):
    # create mapping from label name to its index for better efficiency {label : int}
    label_to_int = {c: i for i, c in enumerate(labels)}

    # initialize array to save selected labels
    zero_one_arr = np.zeros([len(labels)], dtype=int)
    for label in labels:
        zero_one_arr[label_to_int[label]] = 1

    return zero_one_arr
