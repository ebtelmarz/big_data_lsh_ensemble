#!/usr/bin/env python3

import sys


def main():
    index = 0
    for line in sys.stdin:
        try:
            line.strip()

            values_string = line.split('\t')[1].split(',')
            values_string[-1] = values_string[-1].replace('\n', '')
            values = set(values_string)
            values = list(values)

            print('%s\t%s' % (str(index), values))
            index += 1
        except IndexError:
            continue


if __name__ == '__main__':
    main()
