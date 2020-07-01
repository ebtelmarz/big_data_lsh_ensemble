import findspark
findspark.init()
from datetime import datetime
from pyspark.sql import SparkSession
import config
from datasketch import MinHash


def compute_actual_inclusion_coeff(coppia):
    col1, col2 = set(coppia['col1'].split(',')), set(coppia['col2'].split(','))
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
    precision = pos / length
    print('Precision: ' + str(precision))
    return precision


def evaluate_precision(df):
    positives = 0
    for coppia in df.take(df.count()):
        actual_coeff = compute_actual_inclusion_coeff(coppia)

        col1 = coppia['col1'].split(',')
        col2 = coppia['col2'].split(',')
        union = set(col1).union(set(col2))

        minhash_col1 = compute_minhash(col1)
        minhash_col2 = compute_minhash(col2)
        minhash_union = compute_minhash(union)

        jaccard_col1_col2 = minhash_col1.jaccard(minhash_col2)
        jaccard_union_col1 = minhash_union.jaccard(minhash_col1)

        estimated_inclusion = jaccard_col1_col2 / jaccard_union_col1
        # print(jaccard_col1_col2, jaccard_union_col1, estimated_inclusion, actual_coeff)
        if round(actual_coeff, 1) == round(estimated_inclusion, 1):
            positives += 1

    get_precision(positives, df.count())


def get_recall(cardinality, positives):
    try:
        recall = cardinality / positives
    except ZeroDivisionError:
        recall = 0.0

    if recall > 1.0:
        recall = cardinality - positives
        print('LSH Ensemble found ' + str(recall) + ' values more than expected')
    else:
        print('Recall: ' + str(recall))


def evaluate_recall(dataframe, cardinality):
    positives = 0
    for coppia in dataframe.take(dataframe.count()):
        actual_coeff = compute_actual_inclusion_coeff(coppia)

        if round(actual_coeff, 1) >= config.LSH_PARAMS['threshold']:           # > or >= ??
            positives += 1

    get_recall(cardinality, positives)


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
    print('\nLSH Ensemble results were saved to \'' + config.HADOOP_OUTPUT_DIR + '\'\n')
    # start = datetime.now()
    spark = SparkSession.builder.appName("LSH_Ensemble").getOrCreate()

    df_precision, df_recall, lsh_result_cardinality = generate_dataframes(spark)

    print('\nEvaluating precision of LSH Ensemble...')
    evaluate_precision(df_precision)

    print('\nEvaluating recall of LSH Ensemble...')
    evaluate_recall(df_recall, lsh_result_cardinality)

    # print('Total time of evaluation: ' + str(datetime.now() - start))


if __name__ == '__main__':
    main()
