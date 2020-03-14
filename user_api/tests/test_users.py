import json
import pytest
from random import randint
from os.path import dirname, isfile, join, abspath
from dotenv import load_dotenv
import random
import string
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

_ENV_FILE = join(dirname(__file__), '.env_')

if isfile(_ENV_FILE):
    load_dotenv(dotenv_path=_ENV_FILE)

from app import app #create_app

#Genereta a Randomic Name
userid = 0
username = ''.join(random.choice(string.ascii_lowercase) for i in range(7))


@pytest.fixture(scope='session')
def client():    
    #flask_app = create_app('testing') 
    client = app.test_client()
    return client

def test_users_Post_response_201(client):     
    global userid
    global username
    doc = {
        'name': 'Test User'+username,
        'cpf': '01234567890',
        'email': 'user@test.com',
        'phone_number': '11900001111'
    }
    response = client.post('/api/users', json=doc)

    userid = response.json['id']
    #assert response.json == 'sda'
    assert response.status_code == 201

def test_users_getAll_response_200(client): 
    response = client.get('/api/users')
    
    #status_code = 200
    assert response.status_code == 200    
    #assert len(response.json) > 0
    

def test_users_getOne_response_200(client): 
    global userid
    response = client.get('/api/users/'+str(userid))

    #status_code = 200 & not is empty
    assert response.status_code == 200
    assert len(response.json) > 0


def test_users_getOne_response_404(client): 
    response = client.get('/api/users/9999')
    #status_code = 404 
    assert response.status_code == 404


def test_users_Put_response_200(client): 
    global userid
    doc = {
        'name': 'Name Test Updated',
        'email': 'test@test.com'
    }
    response = client.put('/api/users/'+str(userid), json=doc)
    assert response.status_code == 200    

def test_users_Delete_response_200(client): 
    global userid
    response = client.delete('/api/users/'+str(userid))

    #status_code = 200 & not is empty
    assert response.status_code == 200
    assert len(response.json) > 0    