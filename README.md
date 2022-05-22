# KafkaStreaming
Project Setup:

1 - Install Kafka to start zookeeper and kafka
  - docker-compose up -d
2 - Create a Topic:
  - docker exec -it kafka /bin/sh
  - /opt/kafka/bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic kafka_distinct_counter
Let's export environment variables from .env file
  - export $(cat .env | grep -v ^# | xargs)

3 - Lets send test data to kafka topic using kafka producer
  - To copy data from host to docker container
	- docker cp data/stream.jsonl kafka:/stream.jsonl
  - To run the following command inside container
	- cat stream.jsonl | opt/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic kafka_distinct_counter

  - Alternatively run below command(outside the container)
	- gunzip data/stream.jsonl.gz
	- python src/kafka/producer.py

4 - A small to read the data from kafka and prints it to stdout
	- python src/kafka/consumer.py

5 - To count distinct items in kafka stream, Faust is used which is stream processing library
	- Run below command to start Faust
	- cd src/distinct_counter
	- faust -A users worker -l info
	- Open another terminal lets publish data using producer
	- python src/kafka/producer.py

	- In another terminal, run the consumer and check the topic to which faust worker writes the output
	- opt/kafka/bin/kafka-console-consumer.sh --from-beginning --bootstrap-server kafka:9092 --topic=users-unique-changelog

	- To list all available topics in our Kafka instance, we can use:

	- $KAFKA_HOME/bin/kafka-topics.sh --bootstrap-server kafka:9092 --list
	- To test that all is working correctly, to send some messages.
	- Start a producer on topic test:
	- $KAFKA_HOME/bin/kafka-console-producer.sh --broker-list kafka:9092 --topic=test


6 - Shut down and clean up
Stop the consumer/producer with Ctrl + C
Shut down the kafka broker system
	- docker compose down

KAFKA Streaming:
They are 4 main kafka concepts:
- Topic: All kafka messages pass through topics. A topic is simply a way for us to organize and group a collection of messages. We can have multiple topics, each 
with a unique name.

- Consumers: A consumer is an entity within kafka(subscriber) that is responsible for connection(subscribing) to a particular topic to read its messages.
- Producers: A producer is an entity within kafka(publisher) which is responsible for writing(publishing) messages to a particular topic.

- To run Kafka in docker container, wurstmeister is used. For external kafka cluster access from terminal or services, the docker-compose.yml needs to be updated.	

Faust writes the output to a new topic

6 - What are some efficient algorithms to benchmark:
- Hashset
- Hyperloglog
- Linear counting

Counter        Bytes Used        Count      Error
HashSet	   10447016		   67801      0%
Linear     	   3384		   67080	  1%
Hyperloglog    512	         70002	  3%

From above, you can see that using 512 bytes of space, there is error rate of 3%. 
Compare that to a perfect count using a HashMap that requires nearly 10 megabytes of space and you can easily see why cardinality estimators are useful. 
In applications where accuracy is not paramount, which is true for most web scale and network counting scenarios, using a probabilistic counter can result in tremendous space savings.

8 - Key Metrics for monitoring Kafka:
Kafka metrics can be broken down into three categories:
- Kafka server(broker) metrics - https://www.datadoghq.com/blog/monitoring-kafka-performance-metrics/#broker-metrics
- Producer metrics - https://www.datadoghq.com/blog/monitoring-kafka-performance-metrics/#kafka-producer-metrics
- Consumer metrics - https://www.datadoghq.com/blog/monitoring-kafka-performance-metrics/#kafka-consumer-metrics
As Kafka relies on Zookeeper to maintain state, its important to monitor zookeeper.

9 - Scalability:
- For scalability, define kafka nodes which would read from one or more topics and generate unique users count accordingly.

10 -  Edges cases, options and other things:
https://github.com/svetaj/KAFKA_CARDINALITY/blob/master/doc/data_engineer_work.pdf

Bonus: 

11 - How can you optimize kafka producer application for throughput?

Example use case:
When optimizing for performance, you'll typically need to consider tradeoffs between throughput and latency. Because of Kafka’s design, it isn't hard to write large volumes of data into it. But many of the Kafka configuration parameters have default settings that optimize for latency. 
If your use case calls for higher throughput, this tutorial walks you through how to use `kafka-producer-perf-test` to measure baseline performance and tune your producer for large volumes of data.


Short Answer:
They are some producer configuration to be set to increase throughput. 
batch.size: increase to 100000–200000 (default 16384)

linger.ms: increase to 10–100 (default 0)

compression.type=lz4 (default none, i.e., no compression)

acks=1 (default all, since Apache Kafka version 3.0)

For more info about above params and other configuration params, below link for more recommendations.
Link: https://www.confluent.io/resources/recommendations-developers-using-confluent-cloud/?_ga=2.181745316.2016507173.1652952737-1321594843.1652704845

Other ways to count the messages:
In slack forum: http://cnfl.io/slack, below thread i find it interesting.
'''
Srinivas Devaki: You can use GetOffsetShell to get the earliest and latest offsets and compute the number of messages by subtracting with each other

# Get Latest Offset
/opt/kafka/bin/kafka-run-class.sh kafka.tools.GetOffsetShell \
    --broker-list localhost:9092 \
    --topic my_topic \
    --time -1
# Get Earliest Offset
/opt/kafka/bin/kafka-run-class.sh kafka.tools.GetOffsetShell \
    --broker-list localhost:9092 \
    --topic my_topic \
    --time -2

Mitch Henderson: Small note, offsets are very much not guaranteed to be sequential. Not every offset will be a record the client will receive. 
The above will give you a round about estimate of the number of messages, not it will not be exact. The only way to get an exact number is to dump the topic and pipe it to wc

Srinivas: awesome detail, never knew that offsets are not guaranteed to be sequential. 
But why is that so? I’ve tried searching about this but couldn’t find any references, any link where I can read more on this?

Mitch: Idempotent and transactional production are the most common reasons. But there are others.

Weeco: Also because of gaps in compacted topics this won’t work If you don’t want to consume all messages to count the number of records I have just one idea how to get a rough estimate. I described that here: https://github.com/cloudhut/kowl/issues/83
'''

Scalability: Below doc is good:
https://github.com/svetaj/KAFKA_CARDINALITY/blob/master/doc/data_engineer_work.pdf


12 - What happens to the kafka messages if the microservice crashes before kafka commit?
An outage is a situation where applications cannot publish into Kafka. Outages may partially or entirely prevent an inflow of data. The outage does not necessarily have to disable the whole Kafka cluster at the same time.

An outage occurs where:

Multiple brokers in a cluster become unreachable around the same time
min.insync.replicas is not achievable on sends where acks=all or no leaders are available for partitions to which the producing application wants to send
A partial cluster failure that takes out a few partitions is enough over time to completely block a producing application from sending because the memory buffers in its client library fill up.

Extended outages are not defined by any particular time window but display specific characteristics:

Messages are unable to be sent into the client library by the application
Messages exceed the maximum retries or start to time out
Which one of these symptoms shows up first depends on the following client configuration settings:

The amount of memory that you have allocated to the Kafka library’s buffer
The maximum number of retries
The message expiry time

Things to consider:
Ordering -  Any messages which time out and are resent to kafka producer api, enter via external retry or a side channel, will lose their original send order. 
If the application performs synchronous single-message sends, which is not option of anything other than low-volume applications.

Writing to local storage:
-We need to address follwoing concerns in wriiting failed/timed-out messages to local storage:
-What is the resiliency of the local storage? How does it handle a failed disk?
-Is the local storage fast enough to accommodate the throughput? In a system where the sending application takes up a significant amount of memory, disk writes will go through a small page cache and involve a high number of flushes to disk.
-How do you guarantee the durability of the data in case the system shuts down? Applications that write to disk via the file system should periodically flush their writes to disk. They can do this by calling the fsync() function. The latency of the I/O pipeline limits the performance of this operation, which the application calls synchronously.
-You can achieve higher throughput with lower durability by using asynchronous disk APIs, such as libaio or io_uring via liburing. The frequency at which writes should occur to the local physical disks needs to be considered alongside the amount of data that resides in various application buffers that have not yet been written and would be lost if the system had a power outage.

-Should messages be written to a single file for all message types or one per target topic or partition? You need to consider this when the partitioning is predefined and not performed by a partitioner within the client library based on the message key.
-When ingesting from a file into Kafka, how do you keep track of which messages have already been read? This should be considered if your recovery process shuts down midway through its work.
-Any ingesting system needs to be able to handle partial writes (corrupted files).
-What should be the maximum size of a data file? When does the application roll over to a new file?
-When are consumed files deleted from the system?


13 - What are the strategies to handle outages :
Option 1 : Drop failed messages
Pro: Simple to implement
Con: Data loss occurs which is a big deal.

Option 2: Exert backpressure further up the application and retry:
Pro: No external dependencies, no message loss
Con: Message ordering is lost, implementing retries over top of kafka's client libraries is discouraged., blocking the system to inbound traffic closes service wtihout warning to external parties.

Option 3: Write all messages locally and ingest them into kafka asynchronously:
Pro: It is less complex than circuit breaker option, no message loss, no manual intervention.
Con: Local storage will be less reliable than cluster. Message flow will see additional end-to-end latency in standard case.

Option 4: Send timed-out messages to local storage and ingest these into kafka by a side process.
Pro: Low application complexity, no message loss, application can continue accepting inbound traffic for a much longer than memory alone.
Con: Message ordering is lost, Need to consider complexities of writing to local storage.

Option 5: Dual writes to parallel kafka clusters:
Pro: System continues to work even if an entire cluster is unavailable, no message loss, no loss of ordering
Con: Topic configuration must be kept identical in both clusters, addition log is required in sending lib to produce into two locations, this config does not guard against every issue, app may not send messages to either cluster in networking problems.

As part of kafke deployment and topic design, it is important to plan around common failures:
- Machine outages
- Rack/availability zone outages
- networking failures

Thank you
