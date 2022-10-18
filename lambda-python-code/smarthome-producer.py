import redis
import boto3 
import csv
import io
import smart_open
import os

def produce(r, dataset, topic):
    count = 0 
    data = smart_open.smart_open(dataset, 'r')
    for line in smart_open.smart_open(dataset, 'r'):
        
        if len(line) < 3:
            continue
        
        line = clean_line(line)
        split = line.split(':')
        
        columns = ['id','timestamp','value','property','plug_id', 'household_id', 'house_id']
        d = dict(zip(columns,split))
        
        print('Count: ' + str(count))
        print( r.xadd( topic, fields=d ) + " produced: " + str(d) )
        print( 'The len of the stream is ' + str( r.xlen(topic) ) )
        print('')
        count += 1
       
def reset_redis_topic(r,topic):
    deleted = r.xtrim(topic, maxlen=0)
    print( f'deleted entries: {deleted}')
    print('The len of the stream is now ' + str(r.xlen(topic)))
    
def clean_line(line):
    line = line.replace('\",\"', ":")
    line = line.replace(',','')
    line = line.replace('\"','')
    line = line.replace('\n','')
    return line 
    

def lambda_handler(event, context):   
    r = redis.Redis(
            host = os.environ['ELASTICACHE_ENDPOINT'], 
            port = 6379,
            charset = "utf-8", 
            decode_responses = True
            )
    topic = 'smarthome:subeset'
    reset_redis_topic(r,topic)
    dataset = 's3://data-reply-redis-demo/dataset/smarthome-dataset-subset.csv'
    to_skip = 0
    produce(r, dataset, topic)
    return