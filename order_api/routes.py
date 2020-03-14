from flask import jsonify, request, Blueprint
from utils.functions import corsify_response
from controllers.order_controller import *

orderRoutes = Blueprint('routes', __name__)

### ---- Routes ---- ###

###  /api/orders  ###
@orderRoutes.route('/api/orders', methods=['GET', 'POST'])
def orders():

    ### GET ###
    if (request.method == 'GET'):
        return getAllOrders()


    ### POST ###
    if (request.method == 'POST'):
        return post(request.get_json())
         


###  /api/orders/:id  ###
@orderRoutes.route('/api/orders/<string:id>', methods=['GET', 'PUT', 'DELETE'])
def orders_id(id):

    ### Get Order From Database ###
    try:
        order = getOrderFromDB(id)   
    except:
        return corsify_response(jsonify({'msg':'Order not found!'})), 404


    ### GET ###
    if (request.method == 'GET'):  
        return getOrderbyId(order, id)


    ### PUT ###
    if (request.method == 'PUT'):
        return put(request.get_json(), order, id)       


    ### DELETE ###
    if (request.method == 'DELETE'):
        return delete(id)        



###  /api/orders/user/:id  ###
@orderRoutes.route('/api/orders/user/<int:id>', methods=['GET'])
def orders_user_id(id):
    return getOrdersbyUser(id)