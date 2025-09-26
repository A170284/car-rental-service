from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, DateTimeLocalField, DecimalField, SelectField, BooleanField
from wtforms.validators import DataRequired, Optional, Email

class BranchForm(FlaskForm):
    BranchId = IntegerField('BranchId', validators=[DataRequired()])
    BranchName = StringField('BranchName', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    PhoneNo = StringField('PhoneNo', validators=[Optional()])

class CustomerForm(FlaskForm):
    CustomerID = IntegerField('CustomerID', validators=[DataRequired()])
    First_Name = StringField('First Name', validators=[DataRequired()])
    Last_Name = StringField('Last Name', validators=[DataRequired()])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    PhoneNo = StringField('Phone No', validators=[Optional()])
    Address = StringField('Address', validators=[Optional()])
    LicenseNumber = StringField('LicenseNumber', validators=[Optional()])
    DateofBirth = DateField('DOB', validators=[Optional()])
