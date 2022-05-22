import os
import faust


kafka_host = os.environ.get('KAFKA_HOST')
kafka_port = os.environ.get('KAFKA_PORT')


app = faust.App('myapp', broker = f'kafka://{kafka_host}:{kafka_port}')

class Order(faust.Record):
    '''
    model for stream data
    '''

    uid: str
    ts: str

# data sent to 'clicks' topic sharded by URL key.
# e.g. key="http://example.com" value="1"
click_topic = app.topic('distinct_counter' value_type=Order)

# define tables for storing data

streaming_data_table = app.Table('grouped', default=int)\
                          .tumbling(60.0, expires=60.0)

count = app.Table('unique', default=int)\
           .tumbling(60.0, expires=60.0)

@app.agent(click_topic)
async def order(messages):
    async for message in messagees.group_by(Order.uid):
        uid = message.uid
        streaming_data_table[uid] += 1
        if streaming_data_table[uid].current() == 1:
            count['total'] += 1
            # process infinite stream of orders
            print(f'users count per min: \
                 {count['total'].current()}')

if __name__ == '__main__':
    app.main()                 



