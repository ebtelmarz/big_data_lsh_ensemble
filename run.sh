#!/usr/bin/env bash

rm data/query.txt
pip3 install -r requirements.txt
python3 prepare_dataset/dataset_provision.py
python3 prepare_dataset/create_random_query.py
python3 prepare_dataset/set_threshold.py

#value=$(cat prepare_dataset/tmp.txt)
#echo $value
#if [[ $value == no ]]; then
#    echo 'si'
#    exit 1
#fi

hdfs dfs -rm -r /input
hdfs dfs -rm -r /output

hdfs dfs -mkdir /input
hdfs dfs -mkdir /output

cd data
for entry in *
    do
        hdfs dfs -put "$entry" /input
        if [[ $entry != "query.txt" ]];
        then
            dataset=$entry
        fi
    done

cd ..
hadoop jar jars/hadoop-streaming-3.2.1.jar -D mapreduce.job.reduces=0 -mapper lsh_mapred/map.py -input /input/"$dataset" -output /output/out_dataset
hadoop jar jars/hadoop-streaming-3.2.1.jar -D mapreduce.job.reduces=0 -mapper lsh_mapred/map.py -input /input/query.txt -output /output/out_query
hadoop jar jars/hadoop-streaming-3.2.1.jar -mapper lsh_mapred/map.py -reducer lsh_mapred/reduce.py -input /input/"$dataset" -output /output/out_lsh
echo ''
echo "LSH Ensemble results were saved to 'hdfs://localhost:9000/output/out_lsh'"
echo ''
python3 evaluation/evaluate_mapreduce_results.py
rm prepare_dataset/tmp.txt