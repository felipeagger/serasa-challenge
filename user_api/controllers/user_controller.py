from utils.crypto import Crypt, Decrypt
from utils.functions import corsify_response, timetostr
from dbconf.cache import config_cache, json_serializer, json_deserializer 
from models.users import User, user_schema, users_schema
from dbconf.db import db
from flask import jsonify
import json

# MemCached 
clientmc = config_cache()



# GET All Users
def getAllUsers():
    #get query from cache
    usersCache = clientmc.get('query_all_users')
    updateCache = False

    #check if it is not in cache
    if (usersCache):
        #Getting data from Cache
        all_users = usersCache   
        res = all_users   

    else:

        #Getting data from Database  
        updateCache = True
        all_users = User.query.all() 

        if all_users:
            res = users_schema.dump(all_users)

            for i in res:
                i['cpf'] = Decrypt(i['cpf'])
                i['email'] = Decrypt(i['email'])
                i['phone_number'] = Decrypt(i['phone_number'])            
    

    #if not is empty
    if not all_users:
        return corsify_response(jsonify({'msg':'No users found!'})), 204
        
    #Update Cache    
    if updateCache:
        clientmc.set('query_all_users', res)
    
    return corsify_response(jsonify(res)), 200




#GET User from DB
def getUserFromDB(id):
    return User.query.filter_by(id=id).first()




#GET User by Id
def getUserbyId(user):
    res = user_schema.dump(user)      
    doc = {
        'id': res['id'],
        'name': res['name'],
        'cpf': Decrypt(res['cpf']),
        'email': Decrypt(res['email']),            
        'phone_number': Decrypt(res['phone_number']),
        'created_at': res['created_at'],
        'updated_at': res['updated_at']
    }       
    return corsify_response(jsonify(doc)), 200




#POST
def post(body):
    #check if there is no other user with the same name
    user = User.query.filter_by(name=body['name']).first()
    if user:
        return corsify_response(jsonify({'msg':'User already exists!'})), 400

    try:
        #Insert New User
        newuser = User(name=body['name'],
                    cpf=Crypt(body['cpf'][:11]), 
                    email=Crypt(body['email'][:100]),
                    phone_number=Crypt(body['phone_number'][:15]))
        db.session.add(newuser)
        db.session.commit()


        #Select this user on DB for Return Id    
        newuser = User.query.filter_by(name=body['name']).first()
        res = user_schema.dump(newuser) 
        doc = {
            'id': res['id'],
            'name': res['name'],
            'cpf': Decrypt(res['cpf']),
            'email': Decrypt(res['email']),            
            'phone_number': Decrypt(res['phone_number']),
            'created_at': res['created_at'],
            'updated_at': res['updated_at']
        }

        #Clear Cache    
        clientmc.set('query_all_users', '')
        return corsify_response(jsonify(doc)), 201            
    except:
        return corsify_response(jsonify({'msg':'Bad Request!'})), 400




#PUT
def put(body, user):
    #Update User
    if body.get('name'):
        user.name = body['name']

    if body.get('cpf'):
        user.cpf = Crypt(body['cpf'][:11])

    if body.get('email'):
        user.email = Crypt(body['email'][:100])

    if body.get('phone_number'):
        user.phone_number = Crypt(body['phone_number'][:15])  

    db.session.commit()   

    #Clear Cache
    clientmc.set('query_all_users', '')      
    return corsify_response(jsonify({'msg':'User Updated!'})), 200




#DELETE
def delete(user):
    db.session.delete(user)
    db.session.commit()         

    #Clear Cache
    clientmc.set('query_all_users', '')
    return corsify_response(jsonify({'msg':'User Deleted!'})), 200 
