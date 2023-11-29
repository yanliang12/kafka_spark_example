'''
https://kafka-python.readthedocs.io/en/master/usage.html
'''


############producer

from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(
    bootstrap_servers='localhost:9092')

# Asynchronous by default
future = producer.send(
	topic = 'quickstart-events', 
	value = b'aaaa')

for i in range(100):
    future = producer.send(
        topic = 'quickstart-events', 
        key = bytes(f'k_{i}', 'utf-8'),
        value = bytes(f'v_{i}', 'utf-8'),
        )


# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=10)
except KafkaError:
    # Decide what to do if produce request failed...
    log.exception()
    pass

# Successful result returns assigned partition and offset
print (record_metadata.topic)
print (record_metadata.partition)
print (record_metadata.offset)

############consumer

from kafka import TopicPartition
from kafka import KafkaConsumer

consumer = KafkaConsumer(bootstrap_servers='localhost:9092')
consumer.assign([TopicPartition('quickstart-events', 0)])
msg = next(consumer)

print(msg)


##### spark 

import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 pyspark-shell'

from pyspark import SparkContext
from pyspark.sql import SparkSession

spark = SparkSession.builder\
.master("local")\
.getOrCreate()

df = spark \
.readStream \
.format("kafka") \
.option("kafka.bootstrap.servers", "localhost:9092") \
.option("subscribe", "quickstart-events") \
.load()

df.createOrReplaceTempView("kafka_streaming")
df_parsed = spark.sql(f"""
    select 
    cast(key as string) as key,
    cast(value as string) as value
    from kafka_streaming
    """)

query2 = df_parsed.writeStream.format("console").start()
