from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Customer, customer_schema, customers_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/customers', methods = ['POST'])
@token_required
def create_customer(current_user_token):
    name = request.json['name']
    event_type = request.json['event_type']
    phone_number = request.json['phone_number']
    email = request.json['email']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')
    
    customer = Customer(name, event_type, phone_number, email, user_token=user_token)

    db.session.add(customer)
    db.session.commit()

    response = customer_schema.dump(customer)
    return jsonify(response)
@api.route('/customers', methods = ['GET'])
@token_required
def get_customer(current_user_token):
    a_user = current_user_token.token
    customers = Customer.query.filter_by(user_token = a_user).all()
    response = customers_schema.dump(customers)
    return jsonify(response)

# Get Single Customer
@api.route('/customers/<id>', methods = ['GET'])
@token_required
def get_single_customer(current_user_token, id):
    customer = Customer.query.get(id)
    response = customer_schema.dump(customer)
    return jsonify(response)


# UPDATE ENDPOINT/CUSTOMER
@api.route('/customers/<id>', methods = ['POST', 'PUT'])
@token_required
def update_customer(current_user_token, id):
    customer = Customer.query.get(id)
    customer.name = request.json['name']
    customer.event_type = request.json['event_type']
    customer.phone_number = request.json['phone_number']
    customer.email = request.json['email']
    customer.user_token = current_user_token.token

    db.session.commit()
    response = customer_schema.dump(customer)
    return jsonify(response)

    
# Delete endpoint
@api.route('/customers/<id>', methods = ['DELETE'])
@token_required
def delete_customer(current_user_token, id):
    customer = Customer.query.get(id)
    db.session.delete(customer)
    db.session.commit()
    response = customer_schema.dump(customer)
    return jsonify(response)
