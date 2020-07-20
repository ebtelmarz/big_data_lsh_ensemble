DATA_DIR = 'data/'

HADOOP_OUTPUT_DIR = 'hdfs://localhost:9000/output/out_lsh'
HADOOP_DATASET = 'hdfs://localhost:9000/output/out_dataset'
HADOOP_QUERY = 'hdfs://localhost:9000/output/out_query'

QUERY_FILE = 'data/query.txt'

QUERY_KEYWORD = 'query'

MINHASH_PARAMS = {
    'num_permutations': 128,
    'encoding': 'utf8'
}

DATASETS_REFERENCES = {
    # 'BMS-POS_dup_dr.inp.gz': 'https://storage.googleapis.com/set-similarity-search/BMS-POS_dup_dr.inp.gz',
    # 'KOSARAK_dup_dr.inp.gz': 'https://storage.googleapis.com/set-similarity-search/KOSARAK_dup_dr.inp.gz',
    # 'FLICKR-london2y_dup_dr.inp.gz': 'https://storage.googleapis.com/set-similarity-search/FLICKR-london2y_dup_dr.inp.gz',
    # 'NETFLIX_dup_dr.inp.gz': 'https://storage.googleapis.com/set-similarity-search/NETFLIX_dup_dr.inp.gz',
    # 'orkut_ge10.inp.gz': 'https://storage.googleapis.com/set-similarity-search/orkut_ge10.inp.gz',
    'canada_us_uk_opendata.inp.gz': 'https://storage.googleapis.com/set-similarity-search/canada_us_uk_opendata.inp.gz',
    'canada_us_uk_opendata_queries_1k.inp.gz': 'https://storage.googleapis.com/set-similarity-search/canada_us_uk_opendata_queries_1k.inp.gz',
    'canada_us_uk_opendata_queries_10k.inp.gz': 'https://storage.googleapis.com/set-similarity-search/canada_us_uk_opendata_queries_10k.inp.gz',
    'canada_us_uk_opendata_queries_100k.inp.gz': 'https://storage.googleapis.com/set-similarity-search/canada_us_uk_opendata_queries_100k.inp.gz',
    'wdc_webtables_2015_english_relational.inp.gz': 'https://storage.googleapis.com/set-similarity-search/wdc_webtables_2015_english_relational.inp.gz',
    'wdc_webtables_2015_english_relational_queries_100.inp.gz': 'https://storage.googleapis.com/set-similarity-search/wdc_webtables_2015_english_relational_queries_100.inp.gz',
    'wdc_webtables_2015_english_relational_queries_1k.inp.gz': 'https://storage.googleapis.com/set-similarity-search/wdc_webtables_2015_english_relational_queries_1k.inp.gz',
    'wdc_webtables_2015_english_relational_queries_10k.inp.gz': 'https://storage.googleapis.com/set-similarity-search/wdc_webtables_2015_english_relational_queries_10k.inp.gz',
}

DATASETS_REFERENCES_LOCAL = {
    'canada_us_uk_opendata_queries_1k.inp.gz': 'https://storage.googleapis.com/set-similarity-search/canada_us_uk_opendata_queries_1k.inp.gz',
    'canada_us_uk_opendata_queries_10k.inp.gz': 'https://storage.googleapis.com/set-similarity-search/canada_us_uk_opendata_queries_10k.inp.gz',
    'wdc_webtables_2015_english_relational_queries_100.inp.gz': 'https://storage.googleapis.com/set-similarity-search/wdc_webtables_2015_english_relational_queries_100.inp.gz',
    'wdc_webtables_2015_english_relational_queries_1k.inp.gz': 'https://storage.googleapis.com/set-similarity-search/wdc_webtables_2015_english_relational_queries_1k.inp.gz',
    'wdc_webtables_2015_english_relational_queries_10k.inp.gz': 'https://storage.googleapis.com/set-similarity-search/wdc_webtables_2015_english_relational_queries_10k.inp.gz',
}

DATASETS_REFERENCES_CLUSTER = {
    'canada_us_uk_opendata.inp.gz': 'https://storage.googleapis.com/set-similarity-search/canada_us_uk_opendata.inp.gz',
    'canada_us_uk_opendata_queries_1k.inp.gz': 'https://storage.googleapis.com/set-similarity-search/canada_us_uk_opendata_queries_1k.inp.gz',
    'canada_us_uk_opendata_queries_10k.inp.gz': 'https://storage.googleapis.com/set-similarity-search/canada_us_uk_opendata_queries_10k.inp.gz',
    'canada_us_uk_opendata_queries_100k.inp.gz': 'https://storage.googleapis.com/set-similarity-search/canada_us_uk_opendata_queries_100k.inp.gz',
    'wdc_webtables_2015_english_relational.inp.gz': 'https://storage.googleapis.com/set-similarity-search/wdc_webtables_2015_english_relational.inp.gz',
    'wdc_webtables_2015_english_relational_queries_100.inp.gz': 'https://storage.googleapis.com/set-similarity-search/wdc_webtables_2015_english_relational_queries_100.inp.gz',
    'wdc_webtables_2015_english_relational_queries_1k.inp.gz': 'https://storage.googleapis.com/set-similarity-search/wdc_webtables_2015_english_relational_queries_1k.inp.gz',
    'wdc_webtables_2015_english_relational_queries_10k.inp.gz': 'https://storage.googleapis.com/set-similarity-search/wdc_webtables_2015_english_relational_queries_10k.inp.gz',
}
