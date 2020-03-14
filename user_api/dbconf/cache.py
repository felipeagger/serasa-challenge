#Dependencies
from os import getenv
from pymemcache.client import base
import json


def json_serializer(key, value):
    if type(value) == str:
        return value, 1
    return json.dumps(value), 2

def json_deserializer(key, value, flags):
    if flags == 1:
        return value
    if flags == 2:
        return json.loads(value)
    raise Exception("Unknown serialization format")


#MemCached Conection
def config_cache():
    try:
        clientmc = base.Client((getenv('CACHE'), 11211), serializer=json_serializer,
        deserializer=json_deserializer) 

        print('Connected to MemCached')
    except:
        print('Exiting because MemCached not Connected!')
        exit(1)

    return clientmc

