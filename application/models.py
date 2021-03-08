from flask_login import UserMixin
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}



    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    lastname = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    roles = db.relationship('Role', secondary='user_roles')

   
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)


    def __repr__(self):
        return '<User %r>' % self.username

class Role(db.Model):
    __tablename__ = 'roles'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), unique=True)
    users = db.relationship('User', secondary='user_roles')

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(
        db.Integer(), 
        db.ForeignKey('users.id'), 
    )

    role_id = db.Column(
        db.Integer, 
        db.ForeignKey('roles.id'),     
    )

class DriversVehicles(db.Model):
    __tablename__ = 'drivers_vehicles'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    driver_id = db.Column(
        db.Integer(), 
        db.ForeignKey('drivers.id'), 
    )

    vehicle_id = db.Column(
        db.Integer, 
        db.ForeignKey('vehicles.id'),     
    )


class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    plate = db.Column(db.String(10), unique=True)
    color = db.Column(db.String(20))
    model = db.Column(db.String(30))
    year = db.Column(db.SmallInteger())
    photo =  db.Column(db.String(150))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    #relations
    brand_id = db.Column(db.Integer, db.ForeignKey('vehicles_brands.id'))
    brand = db.relationship('VehicleBrand')
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id', ondelete='cascade'),nullable=True)
    driver = db.relationship('Driver')

class VehicleBrand(db.Model):
    __tablename__ = 'vehicles_brands'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    #relations
    vehicles = db.relationship("Vehicle", backref="vehicles", lazy='dynamic')
    
    
    
class Driver(db.Model):
    __tablename__ = 'drivers'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    dni = db.Column(db.String(15), unique=True)
    name = db.Column(db.String(40))
    lastname = db.Column(db.String(40))
    address = db.Column(db.String(200))
    email = db.Column(db.String(40))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    #relations
    vehicles = db.relationship("Vehicle", lazy='dynamic')

    #functions
    def update(self):
        db.session.commit()

    def create(self):
        db.session.add(self)
        db.session.commit()
