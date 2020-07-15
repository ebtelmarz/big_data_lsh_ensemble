#!/usr/bin/env python3

import sys
import config
from datasketch.minhash import MinHash
from datasketch.lshensemble import MinHashLSHEnsemble
import prepare_dataset.set_threshold as set_threshold


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


def get_values(values):
    result_values = []

    for elem in values:
        elemento = elem[2:-1]
        elemento_c = elemento[:-1] if elemento[-1] == '\'' else elemento
        result_values.append(elemento_c)
    return result_values


def main():
    query_file = config.QUERY_FILE
    to_pass = []
    global_map = {}
    keys = []

    query_set = prepare_query(query_file)

    for line in sys.stdin:
        key, values = line.split('\t')
        fields = values.split(',')
        fields[-1] = fields[-1].replace(']', '')

        records = get_values(fields)
        minhash = prepare_domain(records)
        length = len(records)
        if key not in keys:
            to_pass.append((key, minhash, length))
        global_map.update({key: records})
        keys.append(key)

    sim_search(query_set, to_pass, global_map)


if __name__ == '__main__':
    main()
