from flask import jsonify, request, Blueprint
from utils.functions import corsify_response
from controllers.user_controller import *

userRoutes = Blueprint('routes', __name__)

### ---- Routes ---- ###

###  /api/users  ###
@userRoutes.route('/api/users', methods=['GET', 'POST'])
def users():

    ### GET ###
    if (request.method == 'GET'):        
        return getAllUsers()


    ### POST ###
    if (request.method == 'POST'):
        return post(request.get_json())      


###  /api/users/:id  ###
@userRoutes.route('/api/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def users_id(id):

    ### Get User From Database ###
    user = getUserFromDB(id)        
    if not user:
        return corsify_response(jsonify({'msg':'User not found!'})), 404


    ### GET ###
    if (request.method == 'GET'):   
        return getUserbyId(user)


    ### PUT ###
    if (request.method == 'PUT'):
        return put(request.get_json(), user)      
           

    ### DELETE ###
    if (request.method == 'DELETE'):
        return delete(user)     
