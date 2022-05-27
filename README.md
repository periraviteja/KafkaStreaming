# KafkaStreaming

Task Description:
The initial prototype should provide unique user IDs per minute, from the ingested data described bellow:

The test data consists of (Log)-Frames of JSON data;
ts - timestamp (unixtime);
uid - user id;
Display results as soon as possible;

The following items should be provided:
READme document explaining the thought process;
instructions to build/run;
reasoning behind the key points;
metrics.

To run in os/linux, .sh command run replacing the \bin\windows\*.bat command which works in windows.

- To access historical data, one of the two ways is via spark providing the docs to process in batch.
- But Storing historical data in kafka clusters will become expensive as kafka stores multiple copies of each message on hard drives connected to servers. 
- This can lead to risk in production environments resulting low performance.
- Given the significant technical hurdles inherent in reading data directly from Kafka, using a data lake to store raw events makes sense.  
- To manage this raw Kafka data and make it useful, establish an ETL pipeline to extract the data from Kafka or a staging environment, transform it into structured data, and then load it into the database or analytics tool of choice

Prerequisites:
	- Install JDM/JRE

Install below libraries:
	- kafka-python
	- cython
	- pdsa

Project Setup:

Project Setup:

1- Start Zookeeper
Zookeeper server:
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties

2 - Start Kafka
Kafka server:
.\bin\windows\kafka-server-start.bat .\config\server.properties

3 - List Topics
.\bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092

4 - Topic Creation
.\bin\windows\kafka-topics.bat --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic distinct_nummer2

5 - To confirm the running topic
.\bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092

6 - Easy way to pass the test data to console producer :
.\bin\windows\kafka-console-producer.bat --broker-list localhost:9092 --topic distinct_nummer2 < stream.jsonl

7 - Stopping kafka
ps ax | grep -i 'kafka.Kafka' | grep -v grep | awk '{print $1}' | xargs kill -9

=========================================================

Useful links:
- https://spark.apache.org/docs/2.2.0/structured-streaming-kafka-integration.html
- http://activisiongamescience.github.io/2016/06/15/Kafka-Client-Benchmarking/
- https://buildmedia.readthedocs.org/media/pdf/pdsa/stable/pdsa.pdf

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
- Kafka server(broker) metrics -
- Producer metrics 
- Consumer metrics 

Broker Metrics:
All messages must pass through a Kafka broker in order to be consumed, monitoring and alerting on issues as they emerge in broker cluster. 
They can be broken into three metrics:
- Kafka emitted metrics
	- Some metrics to watch are 
		- UnderReplicatedPartitions, IsrShrinksPerSec/IsrExpandsPerSec , ActiveControllerCount, OfflinePartitionsCount(controller only), LeaderElectionRateAndTimeMs, UncleanLeaderElectionsPerSec, TotalTimeMs, PurgatorySize, BytesInPerSec/BytesOutPerSec, RequestsPerSec
- Host-level metrics
	- Some Metrics to watch are
		- Page cache read ratio, Disk usage, CPU usage, Network bytes sent/received
- JVM garbage collection metrics
	- Some metrics to watch are
		- Young generation garbage collection time, Old generation garbage collection count/time


Kafka Producer Metrics:
Some Metrics to watch are:
	- Compression rate, response rate, request rate, request latency average, Outgoing byte rate, I/O wait time, Batch size

Consumer Metrics:
	- Some metrics to watch are:
		- Records lag/ Records lag max, bytes consumed rate, records consumed rate, fetch rate

Why ZooKeeper?
It plays important role in Kafka deployments, which is responsible for maintaining information about brokers and topics, applying quotas to govern the rate of traffic moving through your deployment, and storing information about replicas so Kafka can elect partition leaders as state of deployment changes.
To run a reliable kafka cluster, one should deploy Zookeeper in a high-availability configuration called ensemble.

ZooKeeper Metrics:
	 -  Some metrics to watch are:
		- Outstanding requests, average latency, number of alive connections , Followers(leader only), Pending syncs (leaders only), Open file descriptor count

Zookeeper system metrics:
	 - Some metrics to watch for:
		- Bytes sent/ received, Usable memory, Swap usage, Disk latency

As Kafka relies on Zookeeper to maintain state, its important to monitor zookeeper.

9 - Scalability:
- For scalability, define kafka nodes which would read from one or more topics and generate unique users count accordingly.

10 -  Edges cases, options and other things:
There can be several estimator records containing same timestamp and range.
- Query from application reads all records that match given criteria and performs estimator addition to produce resulting cardinality estimation.
- To minimize error, resulting cardinality should be less than expected cardinality( provided as input param)
- Any batch processing produces same way separate estimator records with appropriate time stamps and range according to configured granularity.
- Scalability is achieved same way:
- Separate kafka nodes read from one or more kafka topic and produce estimator records in proposed manner. 
Link: http://highscalability.com/blog/2019/2/27/give-meaning-to-100-billion-events-a-day-the-shift-to-redshi.html

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
One can use GetOffsetShell to get the earliest and latest offsets and compute the number of messages by subtracting with each other

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
