#!/usr/bin/python3

def remove_zeroes(x_values, y_values):
    if len(x_values) != len(y_values):
        raise ValueError("Cannot make xy graph. Length of arrays not equal")

    for i in range(len(x_values) - 1, -1, -1):
        if y_values[i] == 0:
            del x_values[i]
            del y_values[i]

    return x_values, y_values
