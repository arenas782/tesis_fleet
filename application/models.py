from flask_login import UserMixin
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class Base(db.Model):
    __abstract__ = True
    #functions
    def update(self):
        db.session.commit()

    def create(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()



class User(UserMixin,Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    lastname = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(200), nullable=False) 
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    #relations

    role_id = db.Column(
        db.Integer, 
        db.ForeignKey('roles.id'),     
    )

    
    role = db.relationship('Role')

    
   
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

class Role(Base):
    __tablename__ = 'roles'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), unique=True)
   



class DriversVehicles(Base):
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


class Vehicle(Base):
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
    vehicle_status_id = db.Column(db.Integer, db.ForeignKey('vehicles_status.id'))
    status = db.relationship('VehicleStatus')
    vehicle_type_id = db.Column(db.Integer, db.ForeignKey('vehicles_types.id'))
    vehicle_type = db.relationship('VehicleType')
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id', ondelete='cascade'),nullable=True)
    driver = db.relationship('Driver')
    maintenances = db.relationship('Maintenance',cascade="all, delete-orphan")
    
    
    
    tracker = db.relationship("Tracker", backref="trackers", lazy='dynamic')

class VehicleBrand(Base):
    __tablename__ = 'vehicles_brands'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    #relations
    vehicles = db.relationship("Vehicle", backref="vehicles", lazy='dynamic')
    
class VehicleStatus(Base):
    __tablename__ = 'vehicles_status'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    
    
    
class VehicleType(Base):
    __tablename__ = 'vehicles_types'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    
    
    
class Driver(Base):
    __tablename__ = 'drivers'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    dni = db.Column(db.String(15), unique=True)
    name = db.Column(db.String(40))
    lastname = db.Column(db.String(40))
    address = db.Column(db.String(200))
    email = db.Column(db.String(40))
    phone = db.Column(db.String(20))
    photo = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    #relations
    vehicles = db.relationship("Vehicle", lazy='dynamic')




class Tracker(Base):
    __tablename__ = 'trackers'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    imei = db.Column(db.String(15), unique=True)
    phone = db.Column(db.String(15))
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    #relations
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id', ondelete='cascade'),nullable=True)
    vehicle = db.relationship('Vehicle')

    tracker_protocol_id = db.Column(db.Integer, db.ForeignKey('trackers_protocols.id', ondelete='cascade'),nullable=True)
    protocol = db.relationship('TrackerProtocol')



class TrackerProtocol(Base):
    __tablename__ = 'trackers_protocols'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), unique=True)
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    
    
class TrackerCommand(Base):
    __tablename__ = 'trackers_commands'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    command = db.Column(db.String(150))
    description = db.Column(db.String(30))    
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    #relations
    tracker_protocol_id = db.Column(db.Integer, db.ForeignKey('trackers_protocols.id', ondelete='cascade'),nullable=True)
    protocol = db.relationship('TrackerProtocol')
    


class TrackerCommandHistory(Base):
    __tablename__ = 'trackers_commands_history'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    status = db.Column(db.String(20),nullable=True)
    
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    #relations
    tracker_id = db.Column(db.Integer, db.ForeignKey('trackers.id', ondelete='cascade'),nullable=True)
    tracker_command_id = db.Column(db.Integer, db.ForeignKey('trackers_commands.id', ondelete='cascade'),nullable=True)
    tracker = db.relationship('Tracker')
    commands = db.relationship('TrackerCommand')

class TrackerLog(Base):
    __tablename__ = 'trackers_logs'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    latitude = db.Column(db.Numeric(10,6),nullable=True)
    longitude = db.Column(db.Numeric(10,6),nullable=True)
    event = db.Column(db.String(15))
    date = db.Column(db.DateTime)

    #relations
    tracker_id = db.Column(db.Integer, db.ForeignKey('trackers.id', ondelete='cascade'),nullable=True)
    tracker = db.relationship('Tracker')

    @property
    def serialize(self):
        return {
            'id'         : self.id,
            'date': self.date.strftime('%d/%m/%Y %H:%M:%S'),
            'latitude':float(self.latitude),
            'longitude':float(self.longitude),
            'event':self.event                
        }


        
    
class Maintenance(Base):
    __tablename__ = 'maintenance_vehicles'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)    
    status = db.Column(db.Numeric(10,6),nullable=True,default="Pendiente")
    comment = db.Column(db.Numeric(10,6),nullable=True)
    maintenance_type = db.Column(db.String(15))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    
    #relations
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id', ondelete='cascade'))
    vehicle = db.relationship('Vehicle')

    comments = db.relationship('MaintenanceComment',cascade="all, delete-orphan")
    

class MaintenanceComment(Base):
    __tablename__ = 'maintenance_comments'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)        
    comment = db.Column(db.Numeric(10,6),nullable=True)    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    #relations
    maintenance_id = db.Column(db.Integer, db.ForeignKey('maintenance_vehicles.id', ondelete='cascade'))
    maintenance = db.relationship('Maintenance')
    
