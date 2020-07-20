# LSH Ensemble
This is an assignment for the *Big Data* course in **Roma Tre University**.

This repo is based on the work reported in this paper: [LSH Ensemble: Internet-Scale Domain Search.](http://www.vldb.org/pvldb/vol9/p1185-zhu.pdf) 

## Requirements
To run this project you need:

- [Python](https://www.python.org/downloads/release/python-369/) 3.6.9
- [Hadoop](https://hadoop.apache.org/releases.html) 3.2.1
- [Spark](https://spark.apache.org/downloads.html) 3.0.0
- pip3 intstalled in your machine. To install pip3 run the following commands in a shell
```bash
sudo apt update
sudo apt install python3-pip
```

## Usage
###To run the project locally

Start Hadoop, open a shell and run
```bash
$HADOOP_HOME/sbin/start-dfs.sh 
```

Download this repo or clone it by running
```bash
git clone https://github.com/ebtelmarz/big_data_lsh_ensemble.git
```

Move inside the downloaded directory
```bash
cd big_data_lsh_ensemble/
```

Execute the run.sh script by running in a shell
 ```bash
sh run.sh
```
&nbsp;

###To run the project on cluster
Create a virtual environment 
 ```bash
python3 -m venv my_env
source .my_env/bin/activate 
``` 
Execute the run_cluster.sh script by running
 ```bash
sh run_cluster.sh
``` 