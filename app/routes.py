from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime, date
from . import db
from .models import (
    Branch, Customer, Employee, Car, Location, Reservation,
    Rental, Payment, AccidentHistory, TransactionHistory
)

main_bp = Blueprint('main', __name__)

# Home
@main_bp.route('/')
def index():
    # simple dashboard counts
    branch_count = Branch.query.count()
    car_count = Car.query.count()
    reservation_count = Reservation.query.count()
    rental_count = Rental.query.count()
    return render_template('index.html', branch_count=branch_count, car_count=car_count,
                           reservation_count=reservation_count, rental_count=rental_count)


def list_entities(model, template_name, order_by=None):
    q = model.query
    if order_by:
        q = q.order_by(order_by)
    items = q.all()
    return render_template(template_name, items=items)


# BRANCHES
@main_bp.route('/branches')
def branches_list():
    return list_entities(Branch, 'entities/branches_list.html')

@main_bp.route('/branches/add', methods=['GET','POST'])
def branches_add():
    if request.method == 'POST':
        b = Branch(
            branchname = request.form.get('branchname'),
            address = request.form.get('address'),
            phone = request.form.get('phone')
        )
        db.session.add(b); db.session.commit(); flash("Branch added.", "success")
        return redirect(url_for('main.branches_list'))
    return render_template('form_generic.html', action=url_for('main.branches_add'),
                           fields=[('branchname','text'),('address','text'),('phone','text')], title="Add Branch")

@main_bp.route('/branches/<int:id>/edit', methods=['GET','POST'])
def branches_edit(id):
    b = Branch.query.get_or_404(id)
    if request.method == 'POST':
        b.branchname = request.form.get('branchname')
        b.address = request.form.get('address')
        b.phone = request.form.get('phone')
        db.session.commit(); flash("Branch updated.", "success"); return redirect(url_for('main.branches_list'))
    return render_template('form_generic.html', obj=b, action=url_for('main.branches_edit', id=id),
                           fields=[('branchname','text'),('address','text'),('phone','text')], title="Edit Branch")

@main_bp.route('/branches/<int:id>/delete', methods=['POST'])
def branches_delete(id):
    b = Branch.query.get_or_404(id); db.session.delete(b); db.session.commit(); flash("Branch deleted.", "success")
    return redirect(url_for('main.branches_list'))


# CUSTOMERS
@main_bp.route('/customers')
def customers_list():
    return list_entities(Customer, 'entities/customers_list.html')

@main_bp.route('/customers/add', methods=['GET','POST'])
def customers_add():
    if request.method == 'POST':
        c = Customer(
            name = request.form.get('name'),
            phone = request.form.get('phone'),
            email = request.form.get('email'),
            licensenumber = request.form.get('licensenumber')
        )
        db.session.add(c); db.session.commit(); flash("Customer added.", "success"); return redirect(url_for('main.customers_list'))
    return render_template('form_generic.html', action=url_for('main.customers_add'),
                           fields=[('name','text'),('phone','text'),('email','email'),('licensenumber','text')], title="Add Customer")

@main_bp.route('/customers/<int:id>/edit', methods=['GET','POST'])
def customers_edit(id):
    c = Customer.query.get_or_404(id)
    if request.method == 'POST':
        c.name = request.form.get('name'); c.phone = request.form.get('phone')
        c.email = request.form.get('email'); c.licensenumber = request.form.get('licensenumber')
        db.session.commit(); flash("Customer updated.", "success"); return redirect(url_for('main.customers_list'))
    return render_template('form_generic.html', obj=c, action=url_for('main.customers_edit', id=id),
                           fields=[('name','text'),('phone','text'),('email','email'),('licensenumber','text')],
                           title="Edit Customer")

@main_bp.route('/customers/<int:id>/delete', methods=['POST'])
def customers_delete(id):
    c = Customer.query.get_or_404(id); db.session.delete(c); db.session.commit(); flash("Customer deleted.", "success")
    return redirect(url_for('main.customers_list'))


# EMPLOYEES
@main_bp.route('/employees')
def employees_list():
    return list_entities(Employee, 'entities/employees_list.html')

@main_bp.route('/employees/add', methods=['GET','POST'])
def employees_add():
    if request.method == 'POST':
        e = Employee(
            branchid = int(request.form.get('branchid')) if request.form.get('branchid') else None,
            name = request.form.get('name'),
            position = request.form.get('position'),
            phone = request.form.get('phone')
        )
        db.session.add(e); db.session.commit(); flash("Employee added.", "success"); return redirect(url_for('main.employees_list'))
    branches = Branch.query.all()
    return render_template('form_generic.html', action=url_for('main.employees_add'),
                           fields=[('branchid','select',branches),('name','text'),('position','text'),('phone','text')],
                           title="Add Employee")

@main_bp.route('/employees/<int:id>/edit', methods=['GET','POST'])
def employees_edit(id):
    e = Employee.query.get_or_404(id)
    if request.method == 'POST':
        e.branchid = int(request.form.get('branchid')) if request.form.get('branchid') else None
        e.name = request.form.get('name'); e.position = request.form.get('position'); e.phone = request.form.get('phone')
        db.session.commit(); flash("Employee updated.", "success"); return redirect(url_for('main.employees_list'))
    branches = Branch.query.all()
    return render_template('form_generic.html', obj=e, action=url_for('main.employees_edit', id=id),
                           fields=[('branchid','select',branches),('name','text'),('position','text'),('phone','text')],
                           title="Edit Employee")

@main_bp.route('/employees/<int:id>/delete', methods=['POST'])
def employees_delete(id):
    e = Employee.query.get_or_404(id); db.session.delete(e); db.session.commit(); flash("Employee deleted.", "success"); return redirect(url_for('main.employees_list'))


# CARS
@main_bp.route('/cars')
def cars_list():
    return list_entities(Car, 'entities/cars_list.html')

@main_bp.route('/cars/add', methods=['GET','POST'])
def cars_add():
    if request.method == 'POST':
        car = Car(
            model = request.form.get('model'),
            make = request.form.get('make'),
            year = int(request.form.get('year')) if request.form.get('year') else None,
            cartype = request.form.get('cartype'),
            registrationnumber = request.form.get('registrationnumber'),
            availabilitystatus = request.form.get('availabilitystatus') or 'Available',
            branchid = int(request.form.get('branchid')) if request.form.get('branchid') else None,
            dailyrate = float(request.form.get('dailyrate') or 1000.0)
        )
        db.session.add(car); db.session.commit(); flash("Car added.", "success"); return redirect(url_for('main.cars_list'))
    branches = Branch.query.all()
    return render_template('form_generic.html', action=url_for('main.cars_add'),
                           fields=[('model','text'),('make','text'),('year','number'),('cartype','text'),
                                   ('registrationnumber','text'),('availabilitystatus','text'),('branchid','select',branches),('dailyrate','number')],
                           title="Add Car")

@main_bp.route('/cars/<int:id>/edit', methods=['GET','POST'])
def cars_edit(id):
    car = Car.query.get_or_404(id)
    if request.method == 'POST':
        car.model = request.form.get('model'); car.make = request.form.get('make')
        car.year = int(request.form.get('year')) if request.form.get('year') else None
        car.cartype = request.form.get('cartype'); car.registrationnumber = request.form.get('registrationnumber')
        car.availabilitystatus = request.form.get('availabilitystatus') or car.availabilitystatus
        car.branchid = int(request.form.get('branchid')) if request.form.get('branchid') else None
        car.dailyrate = float(request.form.get('dailyrate') or car.dailyrate)
        db.session.commit(); flash("Car updated.", "success"); return redirect(url_for('main.cars_list'))
    branches = Branch.query.all()
    return render_template('form_generic.html', obj=car, action=url_for('main.cars_edit', id=id),
                           fields=[('model','text'),('make','text'),('year','number'),('cartype','text'),
                                   ('registrationnumber','text'),('availabilitystatus','text'),('branchid','select',branches),('dailyrate','number')],
                           title="Edit Car")

@main_bp.route('/cars/<int:id>/delete', methods=['POST'])
def cars_delete(id):
    car = Car.query.get_or_404(id); db.session.delete(car); db.session.commit(); flash("Car deleted.", "success"); return redirect(url_for('main.cars_list'))


# LOCATIONS
@main_bp.route('/locations')
def locations_list():
    return list_entities(Location, 'entities/locations_list.html')

@main_bp.route('/locations/add', methods=['GET','POST'])
def locations_add():
    if request.method == 'POST':
        loc = Location(
            branchid = int(request.form.get('branchid')) if request.form.get('branchid') else None,
            address = request.form.get('address')
        )
        db.session.add(loc); db.session.commit(); flash("Location added.", "success"); return redirect(url_for('main.locations_list'))
    branches = Branch.query.all()
    return render_template('form_generic.html', action=url_for('main.locations_add'),
                           fields=[('branchid','select',branches),('address','text')],
                           title="Add Location")

@main_bp.route('/locations/<int:id>/edit', methods=['GET','POST'])
def locations_edit(id):
    loc = Location.query.get_or_404(id)
    if request.method == 'POST':
        loc.branchid = int(request.form.get('branchid')) if request.form.get('branchid') else None
        loc.address = request.form.get('address')
        db.session.commit(); flash("Location updated.", "success"); return redirect(url_for('main.locations_list'))
    branches = Branch.query.all()
    return render_template('form_generic.html', obj=loc, action=url_for('main.locations_edit', id=id),
                           fields=[('branchid','select',branches),('address','text')],
                           title="Edit Location")

@main_bp.route('/locations/<int:id>/delete', methods=['POST'])
def locations_delete(id):
    loc = Location.query.get_or_404(id); db.session.delete(loc); db.session.commit(); flash("Location deleted.", "success"); return redirect(url_for('main.locations_list'))


# RESERVATIONS
@main_bp.route('/reservations')
def reservations_list():
    return list_entities(Reservation, 'entities/reservations_list.html')

@main_bp.route('/reservations/add', methods=['GET','POST'])
def reservations_add():
    if request.method == 'POST':
        reservation_date = datetime.strptime(request.form.get('reservationdate'), '%Y-%m-%d').date()
        return_date = datetime.strptime(request.form.get('returndate'), '%Y-%m-%d').date()
        r = Reservation(
            customerid = int(request.form.get('customerid')),
            carid = int(request.form.get('carid')),
            pickuplocationid = int(request.form.get('pickuplocationid')),
            dropofflocationid = int(request.form.get('dropofflocationid')),
            reservationdate = reservation_date,
            returndate = return_date,
            status = request.form.get('status') or 'Active'
        )
        # basic conflict check
        conflict = Reservation.query.filter(Reservation.carid==r.carid, Reservation.status != 'Cancelled').first()
        if conflict:
            flash("Car already reserved. Choose another car.", "warning"); return redirect(url_for('main.reservations_add'))
        car = Car.query.get(r.carid)
        if car:
            car.availabilitystatus = 'Reserved'
        db.session.add(r); db.session.commit(); flash("Reservation created.", "success"); return redirect(url_for('main.reservations_list'))

    customers = Customer.query.all(); cars = Car.query.all(); locations = Location.query.all()
    return render_template('form_generic.html', action=url_for('main.reservations_add'),
                           fields=[('customerid','select',customers),('carid','select',cars),
                                   ('pickuplocationid','select',locations),('dropofflocationid','select',locations),
                                   ('reservationdate','date'),('returndate','date'),('status','text')],
                           title="Add Reservation")

@main_bp.route('/reservations/<int:id>/delete', methods=['POST'])
def reservations_delete(id):
    r = Reservation.query.get_or_404(id)
    car = Car.query.get(r.carid)
    if car:
        car.availabilitystatus = 'Available'
    db.session.delete(r); db.session.commit(); flash("Reservation deleted.", "success"); return redirect(url_for('main.reservations_list'))


# RENTALS
@main_bp.route('/rentals')
def rentals_list():
    return list_entities(Rental, 'entities/rentals_list.html')

@main_bp.route('/rentals/add', methods=['GET','POST'])
def rentals_add():
    if request.method == 'POST':
        rental_start = datetime.strptime(request.form.get('rentalstartdate'), '%Y-%m-%d').date()
        reservation_id = int(request.form.get('reservationid'))
        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            flash("Reservation not found.", "danger"); return redirect(url_for('main.rentals_add'))
        car = Car.query.get(reservation.carid)
        if car:
            car.availabilitystatus = 'Rented'
        r = Rental(reservationid=reservation_id, rentalstartdate=rental_start)
        db.session.add(r); db.session.commit(); flash("Rental started.", "success"); return redirect(url_for('main.rentals_list'))
    reservations = Reservation.query.filter(Reservation.status!='Cancelled').all()
    return render_template('form_generic.html', action=url_for('main.rentals_add'),
                           fields=[('reservationid','select',reservations),('rentalstartdate','date')],
                           title="Start Rental")

@main_bp.route('/rentals/<int:id>/end', methods=['POST'])
def rentals_end(id):
    r = Rental.query.get_or_404(id)
    if r.actualreturndate:
        flash("Rental already ended.", "warning"); return redirect(url_for('main.rentals_list'))

    r.actualreturndate = datetime.today().date()
    res = Reservation.query.get(r.reservationid)
    if res:
        car = Car.query.get(res.carid)
        if car:
            days = (r.actualreturndate - r.rentalstartdate).days
            days = max(days, 1)
            r.totalcost = float(car.dailyrate) * days
            car.availabilitystatus = "Available"

    txn = TransactionHistory(rentalid=r.rentalid, action="Rental Ended", actiondate=datetime.today().date())
    db.session.add(txn)
    db.session.commit()
    flash("Rental ended and cost calculated.", "success")
    return redirect(url_for('main.rentals_list'))

@main_bp.route('/rentals/<int:id>/delete', methods=['POST'])
def rentals_delete(id):
    r = Rental.query.get_or_404(id); db.session.delete(r); db.session.commit(); flash("Rental deleted.", "success")
    return redirect(url_for('main.rentals_list'))


# PAYMENTS
@main_bp.route('/payments')
def payments_list():
    return list_entities(Payment, 'entities/payments_list.html')

@main_bp.route('/payments/add', methods=['GET','POST'])
def payments_add():
    if request.method == 'POST':
        p = Payment(
            rentalid = int(request.form.get('rentalid')),
            amount = float(request.form.get('amount')),
            paymentdate = datetime.strptime(request.form.get('paymentdate'), '%Y-%m-%d').date() if request.form.get('paymentdate') else date.today(),
            paymentmethod = request.form.get('paymentmethod')
        )
        db.session.add(p); db.session.commit(); flash("Payment recorded.", "success"); return redirect(url_for('main.payments_list'))
    rentals = Rental.query.all()
    return render_template('form_generic.html', action=url_for('main.payments_add'),
                           fields=[('rentalid','select',rentals),('amount','number'),('paymentdate','date'),('paymentmethod','text')],
                           title="Record Payment")

@main_bp.route('/payments/<int:id>/delete', methods=['POST'])
def payments_delete(id):
    p = Payment.query.get_or_404(id); db.session.delete(p); db.session.commit(); flash("Payment deleted.", "success")
    return redirect(url_for('main.payments_list'))


# ACCIDENT HISTORY
@main_bp.route('/accidents')
def accidents_list():
    return list_entities(AccidentHistory, 'entities/accidenthistory_list.html')

@main_bp.route('/accidents/add', methods=['GET','POST'])
def accidents_add():
    if request.method == 'POST':
        a = AccidentHistory(
            customerid = int(request.form.get('customerid')),
            carid = int(request.form.get('carid')),
            description = request.form.get('description'),
            accidentdate = datetime.strptime(request.form.get('accidentdate'), '%Y-%m-%d').date()
        )
        db.session.add(a); db.session.commit(); flash("Accident recorded.", "success"); return redirect(url_for('main.accidents_list'))
    customers = Customer.query.all(); cars = Car.query.all()
    return render_template('form_generic.html', action=url_for('main.accidents_add'),
                           fields=[('customerid','select',customers),('carid','select',cars),('accidentdate','date'),('description','text')],
                           title="Report Accident")

@main_bp.route('/accidents/<int:id>/delete', methods=['POST'])
def accidents_delete(id):
    a = AccidentHistory.query.get_or_404(id); db.session.delete(a); db.session.commit(); flash("Accident deleted.", "success")
    return redirect(url_for('main.accidents_list'))


# TRANSACTIONS
@main_bp.route('/transactions')
def transactions_list():
    return list_entities(TransactionHistory, 'entities/transactionhistory_list.html')

@main_bp.route('/transactions/add', methods=['GET','POST'])
def transactions_add():
    if request.method == 'POST':
        t = TransactionHistory(
            rentalid = int(request.form.get('rentalid')),
            action = request.form.get('action'),
            actiondate = datetime.strptime(request.form.get('actiondate'), '%Y-%m-%d').date() if request.form.get('actiondate') else date.today()
        )
        db.session.add(t); db.session.commit(); flash("Transaction logged.", "success"); return redirect(url_for('main.transactions_list'))
    rentals = Rental.query.all()
    return render_template('form_generic.html', action=url_for('main.transactions_add'),
                           fields=[('rentalid','select',rentals),('action','text'),('actiondate','date')],
                           title="Add Transaction")

@main_bp.route('/transactions/<int:id>/delete', methods=['POST'])
def transactions_delete(id):
    t = TransactionHistory.query.get_or_404(id); db.session.delete(t); db.session.commit(); flash("Transaction deleted.", "success")
    return redirect(url_for('main.transactions_list'))
