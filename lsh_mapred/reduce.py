#!/usr/bin/env python3

import sys
import config
from datasketch.minhash import MinHash
from datasketch.lshensemble import MinHashLSHEnsemble
from prepare_dataset import set_threshold


def sim_search(query_set, to_pass, glob):
    thresh = set_threshold.get_threshold()['threshold']
    permutations = set_threshold.get_threshold()['num_permutations']
    partitions = set_threshold.get_threshold()['num_partitions']
    lshensemble = MinHashLSHEnsemble(threshold=thresh, num_perm=permutations, num_part=partitions)
    lshensemble.index(to_pass)

    #print('Sets with containment > ' + str(thresh) + ':')
    query_len = query_set[1]
    query_minhash = query_set[0]
    result_keys = lshensemble.query(query_minhash, query_len)

    for key in result_keys:
        if key in glob.keys():
            print(key, '\t', glob[key])


def prepare_query(filename):
    file = open(filename)
    first_line = file.readlines()[0]
    vals_string = first_line.split('\t')[1]
    vals = vals_string.split(',')

    length = len(vals)
    permutations = config.MINHASH_PARAMS['num_permutations']
    encoding = config.MINHASH_PARAMS['encoding']
    m_query = MinHash(num_perm=permutations)

    for elem in vals:
        m_query.update(elem.encode(encoding))
    query_set = [m_query, length]
    return query_set


def prepare_domain(vals):
    permutations = config.MINHASH_PARAMS['num_permutations']
    encoding = config.MINHASH_PARAMS['encoding']
    m_set = MinHash(num_perm=permutations)

    for elem in vals:
        m_set.update(elem.encode(encoding))

    return m_set


def get_values(valori):
    vals = []

    for elem in valori:
        elemento = elem[2:-1]
        elemento_c = elemento[:-1] if elemento[-1] == '\'' else elemento
        vals.append(elemento_c)
    return vals


def main():
    query_file = config.QUERY_FILE
    to_pass = []
    glob = {}

    query_set = prepare_query(query_file)

    for line in sys.stdin:
        key, values = line.split('\t')
        valori = values.split(',')
        valori[-1] = valori[-1].replace(']', '')

        vals = get_values(valori)
        minhash = prepare_domain(vals)
        length = len(vals)
        to_pass.append((key, minhash, length))
        glob.update({key: vals})

    sim_search(query_set, to_pass, glob)


if __name__ == '__main__':
    main()
