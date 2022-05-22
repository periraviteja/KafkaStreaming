import os
import json
from kafka import KafkaConsumer


def consume():
    '''
    to consume data from topic
    '''
    kafka_host = os.environ.get('KAFKA_HOST')
    kafka_port = os.environ.get('KAFKA_PORT')

    consumer = KafkaConsumer('kafka_distinct_number',
                            bootstrap_servers=[f'{kafka_host}:{kafka_port}'],
                            auto_offset_reset = 'earliest',
                            enable_auto_commit = True,
                            group_id = 'distinct_counter')

    for message in consumer:
        data = json.loads(message.Value)
        print(data)



if __name__ == '__main__':
    consume()