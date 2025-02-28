from sqlalchemy import MetaData, DateTime,func
from sqlalchemy.ext.associationproxy import association_proxy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

#model
class Car(db.Model, SerializerMixin):
    __tablename__ = 'cars'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    imageURL = db.Column(db.String)
    description = db.Column(db.Text)
    current_location = db.Column(db.String)
    status = db.Column(db.String)
    mileage = db.Column(db.Integer)
    fuel_type = db.Column(db.String)
    horse_power = db.Column(db.Integer)
    transmission = db.Column(db.String)
    cost = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    
    bookings = db.relationship('Booking', back_populates ='car')
    reviews = db.relationship('Review', back_populates='car')
    
    serialize_only = ('id', 'name', 'imageURL', 'description', 'current_location', 'status',
                       'mileage', 'fuel_type', 'horse_power', 'transmission', 'cost', 'created_at')

class Booking(db.Model, SerializerMixin):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))
    cost = db.Column(db.Integer, nullable=False)
    start_date = db.Column (DateTime, nullable=False)
    end_date = db.Column (DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    user = db.relationship('User', back_populates ='bookings')
    car = db.relationship('Car', back_populates = 'bookings')
    
    serialize_only = ('id','user_id', 'car_id', 'cost', 'start_date', 'end_date', 'created_at')

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=func.now())
    
    bookings = db.relationship('Booking', back_populates='user')
    reviews = db.relationship('Review', back_populates='user')

    serialize_rules = ('-password',)

class Review(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=func.now())
    
    car = db.relationship('Car', back_populates = 'reviews')
    user = db.relationship('User', back_populates = 'reviews')
    
    serialize_only = ('id', 'user_id', 'rating', 'comment', 'created_at')