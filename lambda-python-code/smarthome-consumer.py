import redis
import boto3 
import csv
import io
import json 
from opensearchpy import OpenSearch, RequestsHttpConnection
import datetime
import os

def connect_to_open_search():
    region = 'eu-central-1' # e.g. us-west-1
    service = 'es'
    host = os.environ['OPENSEARCH_ENDPOINT']
    credentials = boto3.Session().get_credentials()
    auth = ('redis-test', 'Redis-@-test-1')
    
    search = OpenSearch(
        hosts = [{'host': host, 'port': 443}],
        http_auth = auth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )
    return search 

def os_new_index(search,index_name):
    index_body = {
      'settings': {
        'index': {
          'number_of_shards': 1
        }
      }
    }
    search.indices.create(index_name,body=index_body)
    
def consume(r,search,stream_dict,stream_key):
    while True:
        # count messages one at a time
        msg = r.xread(stream_dict, count=1)
        if not msg:
            break
        
        last_id = msg[0][1][0][0]
        stream_dict[stream_key] = last_id
        data = msg[0][1][0][1]
        # value==1 is refering to the load data (not cumulative)
        if data['property'] == '1':
            # converting the dict values from string to int and float
            for key in data:
                if key != 'value':
                    data[key] = int(data[key])
            data['value'] = float(data['value'])
            
            # enriching the data structure with a new attribute
            dt = datetime.datetime.fromtimestamp(data['timestamp'])
            data['hour'] = int(dt.hour)
            print(f"Message id {last_id}")
            print(f"Data consumed: {data}")
            # sending data to visualization tool
            try: 
                response = search.index(index='first-index', id=data['id'], body=data)
            except Exception as e:
                print(e)
                print(data)

def lambda_handler(event, context):  
    r = redis.Redis(
        host = os.environ['ELASTICACHE_ENDPOINT'], 
        port = 6379,
        charset = "utf-8", 
        decode_responses = True
        )
    stream_key = 'smarthome:subeset'
    stream_dict = {stream_key: '0-1'}
    
    # connect to Open Search
    search = connect_to_open_search()
    # create new index (if needed)
    index_name = 'first-index'
    # uncomment this the first time
    # os_new_index(search, index_name)
    consume(r,search,stream_dict,stream_key)
    