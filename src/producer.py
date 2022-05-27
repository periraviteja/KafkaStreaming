import jsonlines
import json
import os
from kafka import KafkaProducer


def publish():
    """
    publish data to topic
    """
    #kafka_host = os.environ.get('KAFKA_HOST')
    #kafka_port = os.environ.get('KAFKA_PORT')
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

    filename = 'stream.jsonl'
    with jsonlines.open(filename) as f:
        for line in f:
            try:
                line = f.read()
                data = producer.send('distinct_nummer',
                                     json.dumps(line).encode('utf-8'))
                data.get(timeout=60)
            except EOFError:
                break
        print('Done.')


if __name__ == '__main__':
    publish()