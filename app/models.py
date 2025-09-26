from . import db
from datetime import datetime

class Branch(db.Model):
    __tablename__ = 'branches'
    branchid = db.Column(db.Integer, primary_key=True)
    branchname = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))


class Customer(db.Model):
    __tablename__ = 'customers'
    customerid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    licensenumber = db.Column(db.String(50), unique=True, nullable=False)


class Employee(db.Model):
    __tablename__ = 'employees'
    employeeid = db.Column(db.Integer, primary_key=True)
    branchid = db.Column(db.Integer, db.ForeignKey('branches.branchid', ondelete="CASCADE"))
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(50))
    phone = db.Column(db.String(20))


class Car(db.Model):
    __tablename__ = 'cars'
    carid = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    make = db.Column(db.String(50))
    year = db.Column(db.Integer)
    cartype = db.Column(db.String(50))
    registrationnumber = db.Column(db.String(20), unique=True, nullable=False)
    availabilitystatus = db.Column(db.String(20), default='Available')  # Available, Rented, Maintenance, Reserved
    branchid = db.Column(db.Integer, db.ForeignKey('branches.branchid'))
    dailyrate = db.Column(db.Numeric(10, 2), nullable=False, default=1000.00)


class Location(db.Model):
    __tablename__ = 'locations'
    locationid = db.Column(db.Integer, primary_key=True)
    branchid = db.Column(db.Integer, db.ForeignKey('branches.branchid', ondelete="CASCADE"))
    address = db.Column(db.String(200))


class Reservation(db.Model):
    __tablename__ = 'reservations'
    reservationid = db.Column(db.Integer, primary_key=True)
    customerid = db.Column(db.Integer, db.ForeignKey('customers.customerid', ondelete="CASCADE"))
    carid = db.Column(db.Integer, db.ForeignKey('cars.carid', ondelete="CASCADE"))
    pickuplocationid = db.Column(db.Integer, db.ForeignKey('locations.locationid'))
    dropofflocationid = db.Column(db.Integer, db.ForeignKey('locations.locationid'))
    reservationdate = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    returndate = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='Active')


class Rental(db.Model):
    __tablename__ = 'rentals'
    rentalid = db.Column(db.Integer, primary_key=True)
    reservationid = db.Column(db.Integer, db.ForeignKey('reservations.reservationid', ondelete="CASCADE"))
    rentalstartdate = db.Column(db.Date, nullable=False)
    actualreturndate = db.Column(db.Date)
    totalcost = db.Column(db.Numeric(10, 2))


class Payment(db.Model):
    __tablename__ = 'payments'
    paymentid = db.Column(db.Integer, primary_key=True)
    rentalid = db.Column(db.Integer, db.ForeignKey('rentals.rentalid', ondelete="CASCADE"))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    paymentdate = db.Column(db.Date, default=datetime.utcnow)
    paymentmethod = db.Column(db.String(50))


class AccidentHistory(db.Model):
    __tablename__ = 'accidenthistory'
    accidentid = db.Column(db.Integer, primary_key=True)
    customerid = db.Column(db.Integer, db.ForeignKey('customers.customerid', ondelete="CASCADE"))
    carid = db.Column(db.Integer, db.ForeignKey('cars.carid', ondelete="CASCADE"))
    description = db.Column(db.Text)
    accidentdate = db.Column(db.Date, nullable=False)


class TransactionHistory(db.Model):
    __tablename__ = 'transactionhistory'
    transactionid = db.Column(db.Integer, primary_key=True)
    rentalid = db.Column(db.Integer, db.ForeignKey('rentals.rentalid', ondelete="CASCADE"))
    action = db.Column(db.String(50))
    actiondate = db.Column(db.Date, default=datetime.utcnow)
