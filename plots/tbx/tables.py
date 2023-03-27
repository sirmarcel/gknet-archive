from copy import deepcopy
from functools import partial


def rounder(digits):
    def formatter(number):
        return "{0:.{digits}f}".format(number, digits=digits)

    return formatter


def aligner(width):
    def formatter(s):
        return "{0:>{width}}".format(s, width=width)

    return formatter


def map_across(table, fns):
    result = []

    for row in table:
        result.append([fns[i](entry) for i, entry in enumerate(row)])

    return result


def ncols(data):
    return len(data[0])


def table_to_string(
    data, rownames=None, colnames=None, width=10, colsep="|", rowsep="\n"
):
    data = deepcopy(data)

    if rownames is not None:
        for i, rowname in enumerate(rownames):
            data[i].insert(0, rowname)

    if colnames is not None:
        data.insert(0, colnames)

    if isinstance(width, int):
        aligners = [aligner(width) for i in range(ncols(data))]
    else:
        aligners = [aligner(w) for w in width]

    data = map_across(data, aligners)

    strings = []

    for i, row in enumerate(data):
        strings.append(f" {colsep} ".join(row))

    return rowsep.join(strings) + rowsep


table_to_tex = partial(table_to_string, colsep=" & ", rowsep=" \\\\ \n")


# def table_to_string(data, colnames=None, rownames=None, digits=2):
#     if isinstance(digits, int):
#         digits = [digits for i in range(len(data[0]))]

#     table = []
#     for ir, row in enumerate(data):
#         rowlist = []
#         for ic, entry in enumerate(row):
#             dd = digits[ic]
#             formatted = f"{entry:.{dd}f}"
#             rowlist.append(formatted)

#         table.append(rowlist)
