from datetime import datetime
from utils.functions import corsify_response
from flask import jsonify
from dbconf.db import config_db
from os import getenv
import json
import requests

#Connect to ElasticSearch
es = config_db()

#Define HOST of the Microservice "User_API"
MS_USER_HOST = 'http://'+getenv('USERS_HOST')+':8080/api/users/'


# GET All Orders
def getAllOrders():
    query = {
        "size" : 10000,
        "query": { "match_all": {} }
    }

    #get all orders from ElasticSearch
    all_orders = es.search(index="orders", doc_type="_doc", body=query ,scroll='1m')['hits']    
    
    #if not is empty
    if not all_orders:
        return jsonify({'msg':'No Orders found!'}), 204
                
    #Define new array          
    resultarray = []      
    
    #Mount new Object with data of "User"
    for i in all_orders['hits']: 
        try:
            #Get user in microservice "User"
            res = requests.get(MS_USER_HOST+str(i['_source']['user_id']))  
            user = res.json()   
                    
            doc = {
                'id': i['_id'],
                'user_id': i['_source']['user_id'],
                'user_name': user['name'],
                'user_cpf': user['cpf'],
                'user_email': user['email'],            
                'user_phone_number': user['phone_number'],
                'item_description': i['_source']['item_description'],
                'item_quantity': i['_source']['item_quantity'],
                'item_price': i['_source']['item_price'],
                'total_value': i['_source']['total_value'],
                'created_at': i['_source']['created_at'],
                'updated_at': i['_source']['updated_at']
            }

            resultarray.append(doc)
        except:
            #if result == 404 (User not found)

            #Return only order
            doc = {
                'id': i['_id'],
                'user_id': i['_source']['user_id'],
                'item_description': i['_source']['item_description'],
                'item_quantity': i['_source']['item_quantity'],
                'item_price': i['_source']['item_price'],
                'total_value': i['_source']['total_value'],
                'created_at': i['_source']['created_at'],
                'updated_at': i['_source']['updated_at']
            }
            resultarray.append(doc)


    return  corsify_response(jsonify(resultarray)), 200




#GET Order from DB
def getOrderFromDB(id):
    resdb = es.get(index="orders", doc_type='_doc', id=id)
    order = resdb['_source'] 
    return order



#GET Order by Id
def getOrderbyId(order, id):
    try:
        #Get user in microservice "User"
        res = requests.get(MS_USER_HOST+str(order['user_id']))  
        user = res.json()   
                
        document = {
            'id': id,
            'user_id': order['user_id'],
            'user_name': user['name'],
            'user_cpf': user['cpf'],
            'user_email': user['email'],            
            'user_phone_number': user['phone_number'],
            'item_description': order['item_description'],
            'item_quantity': order['item_quantity'],
            'item_price': order['item_price'],
            'total_value': order['total_value'],
            'created_at': order['created_at'],
            'updated_at': order['updated_at']
        }
    except:
        #if result == 404 (User not found)

        #Return only order
        document = {
            'id': id,
            'user_id': order['user_id'],
            'item_description': order['item_description'],
            'item_quantity': order['item_quantity'],
            'item_price': order['item_price'],
            'total_value': order['total_value'],
            'created_at': order['created_at'],
            'updated_at': order['updated_at']
        }

    return corsify_response(jsonify(document)), 200


#GET Orders by User
def getOrdersbyUser(id):
    query = {
        "size" : 10000,
        "query": { 
            "match": { "user_id": id} }
    }

    #Get all Orders from this User
    all_orders = es.search(index="orders", doc_type="_doc", body=query ,scroll='1m')['hits']    
    
    #if not is empty
    if not all_orders:
        return corsify_response(jsonify({'msg':'No Orders found!'})), 204
                
    #Get user in microservice "User"            
    res = requests.get(MS_USER_HOST+str(id))  
    user = res.json() 

    #check if user exists
    if not user.get('name'):
        return corsify_response(jsonify({'msg':'User not found!'})), 404

    #Define new array
    resultarray = []      
    
    #Mount new Object with data of "User"
    for i in all_orders['hits']:          
        doc = {
            'id': i['_id'],
            'user_id': i['_source']['user_id'],
            'user_name': user['name'],
            'user_cpf': user['cpf'],
            'user_email': user['email'],            
            'user_phone_number': user['phone_number'],
            'item_description': i['_source']['item_description'],
            'item_quantity': i['_source']['item_quantity'],
            'item_price': i['_source']['item_price'],
            'total_value': i['_source']['total_value'],
            'created_at': i['_source']['created_at'],
            'updated_at': i['_source']['updated_at']
        }
        resultarray.append(doc)

    return corsify_response(jsonify(resultarray)), 200




#POST
def post(body):
    try:
        document = {
            'user_id': body['user_id'],
            'item_description': body['item_description'],
            'item_quantity': body['item_quantity'],
            'item_price': body['item_price'],
            'total_value': body['total_value'],
            'created_at': datetime.now(),
            'updated_at':''
        }

        #Create a new Order 
        res = es.index(index='orders', doc_type='_doc', body=document)

        return corsify_response(jsonify(res)), 201            
    except:
        return corsify_response(jsonify({'msg':'Bad Request!'})), 400



#PUT
def put(body, order, id):
    try:           
        #Update Order    
        if body.get('user_id'):
            order['user_id'] = body['user_id']

        if body.get('item_description'):
            order['item_description'] = body['item_description']

        if body.get('item_quantity'):
            order['item_quantity'] = body['item_quantity']

        if body.get('item_price'):
            order['item_price'] = body['item_price']

        if body.get('total_value'):
            order['total_value'] = body['total_value']                

        order['updated_at'] = datetime.now()

        #Persist on database    
        es.index(index='orders', doc_type='_doc', id=id, body=order)   

        return corsify_response(jsonify({'msg':'Order Updated!'})), 200
    except:
        return corsify_response(jsonify({'msg':'Bad Request!'})), 400 




#DELETE
def delete(id):
    es.delete(index='orders', doc_type='_doc', id=id)         
    return corsify_response(jsonify({'msg':'Order Deleted!'})), 200
