from flask_restful import Resource, reqparse
from flask import Flask, jsonify, request, make_response
from sqlalchemy import and_, not_

from models import db, Car

class CarResource(Resource):
    def get(self, id=None):
        if id:
            car = Car.query.filter_by(id=id).first()
            
            if car:
                return car.to_dict(), 200
            else:
                return {"message": "Car not found"}, 404
        else:
            cars = [n.to_dict() for n in Car.query.all()]
            response = make_response(jsonify(cars), 200)
            return response
    def post(self):
       data = request.get_json() 
       
       new_car = Car(
           name = data['name'],
           description = data ['description'],
           current_location = data['current_location'],
           imageURL = data['imageURL'],
           cost = data['cost']
       )
       
       db.session.add(new_car)
       db.session.commit()
       
       return {"message": "Car created successfully"}
       