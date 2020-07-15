import pandas as pd
import numpy as np
import os
from config import config
"""
df = pd.DataFrame(np.random.randn(50, 4), columns=list('ABCD'))

for row in df.itertuples():
    df._set_value(row.Index, 'test', row.D)

print(df.head())

filename = os.listdir(config.DATA_DIR)[0]
file = open(os.path.join(config.DATA_DIR, filename))
line = file.readlines()[100]
print(line)
"""

import findspark
findspark.init()

from pyspark.sql import SparkSession
from datasketch import MinHash
from prepare_dataset import set_threshold
import config

def clean_columns(coppia):
    col1_values = coppia['col1'].split(',')
    col1_values[-1] = col1_values[-1].replace(']', '')
    col1_values[0] = col1_values[0].replace('[', '')
    col2_values = coppia['col2'].split(',')
    col2_values[-1] = col2_values[-1].replace(']', '')
    col2_values[0] = col2_values[0].replace('[', '')

    return set(col1_values), set(col2_values)


def compute_actual_inclusion_coeff(coppia):
    col1, col2 = clean_columns(coppia)

    actual_coeff = len(col1.intersection(col2)) / len(col1)

    return actual_coeff


def compute_minhash(column):
    permutations = config.MINHASH_PARAMS['num_permutations']
    encoding = config.MINHASH_PARAMS['encoding']
    minhash = MinHash(num_perm=permutations)

    for elem in column:
        minhash.update(elem.encode(encoding))
    hash = minhash

    return hash


def get_precision(pos, length):
    if pos == 0 and length == 0:
        precision = 0.0                     # right??
    else:
        try:
            precision = pos / length
        except ZeroDivisionError:
            precision = 0.0

    return precision


def evaluate_precision(df):
    positives = 0
    for coppia in df.take(df.count()):
        actual_coeff = compute_actual_inclusion_coeff(coppia)
        # col1 = coppia['col1'].split(',')
        # col2 = coppia['col2'].split(',')
        # union = set(col1).union(set(col2))

        # minhash_col1 = compute_minhash(col1)
        # minhash_col2 = compute_minhash(col2)
        # minhash_union = compute_minhash(union)

        # jaccard_col1_col2 = minhash_col1.jaccard(minhash_col2)
        # jaccard_union_col1 = minhash_union.jaccard(minhash_col1)

        # estimated_inclusion = jaccard_col1_col2 / jaccard_union_col1
        if round(actual_coeff, 1) >= set_threshold.get_threshold()['threshold']:
            positives += 1

    precision = get_precision(positives, df.count())
    return positives, precision


def get_recall(cardinality, positives):
    if cardinality == 0 and positives == 0:
        recall = 1.0
    else:
        try:
            recall = cardinality / positives
        except ZeroDivisionError:
            recall = 0.0

    if recall > 1.0:
        recall = 1.0

    return recall


def evaluate_recall(dataframe, cardinality):
    positives = 0
    for coppia in dataframe.take(dataframe.count()):
        actual_coeff = compute_actual_inclusion_coeff(coppia)

        if round(actual_coeff, 1) >= set_threshold.get_threshold()['threshold']:           # > or >= ??
            positives += 1
    # print(positives)
    return get_recall(cardinality, positives), positives


def generate_dataframes(spark):
    query = config.HADOOP_QUERY
    dataset = config.HADOOP_DATASET
    data = config.HADOOP_OUTPUT_DIR

    df = spark.read.csv(query, sep='\t', header=False) \
        .withColumnRenamed('_c0', 'key1') \
        .withColumnRenamed('_c1', 'col1')
    df2 = spark.read.csv(data, sep='\t', header=None) \
        .withColumnRenamed('_c0', 'key2') \
        .withColumnRenamed('_c1', 'col2')
    df3 = df.crossJoin(df2)

    df4 = spark.read.csv(dataset, sep='\t', header=None) \
        .withColumnRenamed('_c0', 'key2') \
        .withColumnRenamed('_c1', 'col2')
    df5 = df.crossJoin(df4)

    return df3, df5, df2.count()


def main():
    spark = SparkSession.builder\
        .appName('LSH_Ensemble') \
        .config('spark.memory.fraction', 0.8) \
        .config('spark.executor.memory', '6g') \
        .config('spark.driver.memory', '4g') \
        .getOrCreate()

    df_precision, df_recall, lsh_result_cardinality = generate_dataframes(spark)

    print('\nEvaluating precision and recall of LSH Ensemble...')
    positives, precision = evaluate_precision(df_precision)
    # print('\nEvaluating recall of LSH Ensemble...')
    recall, positive_recall = evaluate_recall(df_recall, positives)

    if recall == 1.0 and positives == 0 and positive_recall == 0 and lsh_result_cardinality == 0:
        print('\nPrecision: ' + str(1.0))
        print('Recall: ' + str(recall))
    else:
        print('\nPrecision: ' + str(precision))
        print('Recall: ' + str(recall))

    spark.stop()


if __name__ == '__main__':
    main()
