########Dockerfile##########
FROM openjdk:8

RUN apt-get update
RUN apt-get install -y wget
RUN apt-get install -y git 
RUN apt-get install -y curl
RUN apt-get install -y vim
RUN apt-get install -y tar
RUN apt-get install -y bzip2

RUN wget https://dlcdn.apache.org/kafka/3.6.0/kafka_2.13-3.6.0.tgz
RUN tar -xzf kafka_2.13-3.6.0.tgz

RUN apt-get update
RUN apt-get install -y python3-dev
RUN apt-get install -y python3-pip

RUN pip3 install kafka-python
RUN pip3 install pyspark

RUN python3 -c "import os;os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 pyspark-shell';from pyspark import SparkContext;from pyspark.sql import SparkSession;spark = SparkSession.builder.master('local').getOrCreate()"

WORKDIR /kafka_2.13-3.6.0

RUN echo "tesg"

COPY zookeeper.properties /
COPY server.properties /

########Dockerfile##########