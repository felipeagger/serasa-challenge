import json
import pytest
from random import randint
from os.path import dirname, isfile, join, abspath
from dotenv import load_dotenv
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

_ENV_FILE = join(dirname(__file__), '.env_')

if isfile(_ENV_FILE):
    load_dotenv(dotenv_path=_ENV_FILE)

from app import app #create_app

newid = randint(1,1000)
orderid = ''

@pytest.fixture(scope='session')
def client():    
    #flask_app = create_app('testing') 
    client = app.test_client()
    return client

def test_orders_Post_response_201(client):     
    global orderid
    global newid
    doc = {
        'user_id': newid,
        'item_description': 'Description Test',
        'item_quantity': 2,
        'item_price': 10.5,
        'total_value': 21.00
    }
    response = client.post('/api/orders', json=doc)
    orderid = response.json['_id']
    assert response.status_code == 201

def test_orders_getAll_response_200(client): 
    response = client.get('/api/orders')
    
    #status_code = 200
    assert response.status_code == 200    
    #assert len(response.json) > 0


def test_orders_getAllbyUser_response_404(client): 
    global newid
    response = client.get('/api/orders/user/'+str(newid))
    
    #status_code = 404
    assert response.status_code == 404    
    assert len(response.json) > 0    
    

def test_orders_getOne_response_200(client): 
    global orderid
    response = client.get('/api/orders/'+orderid)

    #status_code = 200 & not is empty
    assert response.status_code == 200
    assert len(response.json) > 0


def test_orders_getOne_response_404(client): 
    response = client.get('/api/orders/abcxyz')
    #status_code = 404 
    assert response.status_code == 404


def test_orders_Put_response_200(client): 
    global orderid
    doc = {
        'item_description': 'Desc. Test Updated'
    }
    response = client.put('/api/orders/'+orderid, json=doc)
    assert response.status_code == 200    

def test_orders_Delete_response_200(client): 
    global orderid
    response = client.delete('/api/orders/'+orderid)

    #status_code = 200 & not is empty
    assert response.status_code == 200
    assert len(response.json) > 0    