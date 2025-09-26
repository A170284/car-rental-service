import os
from faker import Faker
from app import create_app, db
from app.models import Branch, Customer, Employee, Car, Location, Reservation, Rental, Payment, AccidentHistory, TransactionHistory
import random
from datetime import datetime, timedelta

fake = Faker('en_IN')

app = create_app()
app.app_context().push()

def seed():
    db.drop_all()
    db.create_all()

    # Branches
    branches = []
    for _ in range(3):
        branch = Branch(
            BranchName=fake.company(),
            Address=fake.address(),
            Phone=fake.phone_number()
        )
        db.session.add(branch)
        branches.append(branch)

    db.session.commit()

    # Employees
    for branch in branches:
        for _ in range(2):
            emp = Employee(
                BranchID=branch.BranchID,
                Name=fake.name(),
                Position=fake.job(),
                Phone=fake.phone_number()
            )
            db.session.add(emp)

    # Customers
    customers = []
    for _ in range(5):
        cust = Customer(
            Name=fake.name(),
            Phone=fake.phone_number(),
            Email=fake.email(),
            LicenseNumber=fake.unique.license_plate()
        )
        db.session.add(cust)
        customers.append(cust)

    db.session.commit()

    # Cars
    cars = []
    for branch in branches:
        for _ in range(3):
            car = Car(
                Model=fake.word().capitalize(),
                Make=fake.company(),
                Year=random.randint(2015, 2023),
                CarType=random.choice(["Sedan", "SUV", "Hatchback"]),
                RegistrationNumber=fake.unique.license_plate(),
                AvailabilityStatus="Available",
                BranchID=branch.BranchID,
                DailyRate=random.choice([800, 1000, 1200, 1500])
            )
            db.session.add(car)
            cars.append(car)

    db.session.commit()

    # Locations
    locations = []
    for branch in branches:
        loc = Location(
            BranchID=branch.BranchID,
            Address=fake.address()
        )
        db.session.add(loc)
        locations.append(loc)

    db.session.commit()

    # Sample Reservations
    for cust in customers:
        res_date = datetime.today().date()
        ret_date = res_date + timedelta(days=random.randint(2, 7))
        reservation = Reservation(
            CustomerID=cust.CustomerID,
            CarID=random.choice(cars).CarID,
            PickupLocationID=random.choice(locations).LocationID,
            DropoffLocationID=random.choice(locations).LocationID,
            ReservationDate=res_date,
            ReturnDate=ret_date,
            Status="Active"
        )
        db.session.add(reservation)

    db.session.commit()

    print("✅ Database seeded successfully!")

if __name__ == "__main__":
    seed()
