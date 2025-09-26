-- Drop tables if exist (clean reset)
DROP TABLE IF EXISTS transactionhistory CASCADE;
DROP TABLE IF EXISTS accidenthistory CASCADE;
DROP TABLE IF EXISTS payments CASCADE;
DROP TABLE IF EXISTS rentals CASCADE;
DROP TABLE IF EXISTS reservations CASCADE;
DROP TABLE IF EXISTS cars CASCADE;
DROP TABLE IF EXISTS employees CASCADE;
DROP TABLE IF EXISTS locations CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS branches CASCADE;

-- Branches
CREATE TABLE branches (
    BranchId SERIAL PRIMARY KEY,
    BranchName VARCHAR(100) NOT NULL,
    Address VARCHAR(200),
    Phone VARCHAR(20)
);

-- Customers
CREATE TABLE customers (
    CustomerId SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Phone VARCHAR(20),
    Email VARCHAR(100),
    LicenseNumber VARCHAR(50) UNIQUE NOT NULL
);

-- Employees
CREATE TABLE employees (
    EmployeeId SERIAL PRIMARY KEY,
    BranchId INT REFERENCES branches(BranchId) ON DELETE CASCADE,
    Name VARCHAR(100) NOT NULL,
    Position VARCHAR(50),
    Phone VARCHAR(20)
);

-- Cars
CREATE TABLE cars (
    CarID SERIAL PRIMARY KEY,
    Model VARCHAR(100) NOT NULL,
    Make VARCHAR(50),
    Year INT,
    CarType VARCHAR(50),
    RegistrationNumber VARCHAR(20) UNIQUE NOT NULL,
    AvailabilityStatus VARCHAR(20) DEFAULT 'Available', -- Available, Rented, Maintenance, Reserved
    BranchID INT REFERENCES branches(BranchId),
    DailyRate NUMERIC(10,2) NOT NULL DEFAULT 1000.00
);

-- Locations
CREATE TABLE locations (
    LocationId SERIAL PRIMARY KEY,
    BranchId INT REFERENCES branches(BranchId) ON DELETE CASCADE,
    Address VARCHAR(200)
);

-- Reservations
CREATE TABLE reservations (
    ReservationId SERIAL PRIMARY KEY,
    CustomerId INT REFERENCES customers(CustomerId) ON DELETE CASCADE,
    CarId INT REFERENCES cars(CarId) ON DELETE CASCADE,
    PickupLocationId INT REFERENCES locations(LocationId),
    DropoffLocationId INT REFERENCES locations(LocationId),
    ReservationDate DATE NOT NULL,
    ReturnDate DATE NOT NULL,
    Status VARCHAR(20) DEFAULT 'Active'
);

-- Rentals
CREATE TABLE rentals (
    RentalId SERIAL PRIMARY KEY,
    ReservationId INT REFERENCES reservations(ReservationId) ON DELETE CASCADE,
    RentalStartDate DATE NOT NULL,
    ActualReturnDate DATE,
    TotalCost NUMERIC(10,2)
);

-- Payments
CREATE TABLE payments (
    PaymentId SERIAL PRIMARY KEY,
    RentalId INT REFERENCES rentals(RentalId) ON DELETE CASCADE,
    Amount NUMERIC(10,2) NOT NULL,
    PaymentDate DATE DEFAULT CURRENT_DATE,
    PaymentMethod VARCHAR(50)
);

-- Accident History
CREATE TABLE accidenthistory (
    AccidentId SERIAL PRIMARY KEY,
    CustomerId INT REFERENCES customers(CustomerId) ON DELETE CASCADE,
    CarId INT REFERENCES cars(CarId) ON DELETE CASCADE,
    Description TEXT,
    AccidentDate DATE NOT NULL
);

-- Transaction History
CREATE TABLE transactionhistory (
    TransactionId SERIAL PRIMARY KEY,
    RentalId INT REFERENCES rentals(RentalId) ON DELETE CASCADE,
    Action VARCHAR(50),
    ActionDate DATE DEFAULT CURRENT_DATE
);

-- Indexes
CREATE INDEX idx_cars_status ON cars(AvailabilityStatus);
CREATE INDEX idx_reservations_status ON reservations(Status);
CREATE INDEX idx_rentals_return ON rentals(ActualReturnDate);
