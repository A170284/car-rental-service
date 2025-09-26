-- Branches
INSERT INTO branches (branchname, address, phone) VALUES
('Bangalore Wheels', '12 MG Road, Bangalore', '9876543210'),
('Mumbai Central Cars', '221B Marine Drive, Mumbai', '9988776655'),
('Delhi Drive Rentals', '45 Connaught Place, Delhi', '9123456780');

-- Customers
INSERT INTO customers (name, phone, email, licensenumber) VALUES
('Amit Sharma', '9876501234', 'amitsharma@gmail.com', 'KA0123456'),
('Priya Nair', '9988776655', 'priyanair@gmail.com', 'TN7890123'),
('Ravi Kumar', '9123456789', 'ravikumar@gmail.com', 'DL3456789'),
('Sneha Gupta', '9001122334', 'snehagupta@gmail.com', 'MH9876543');

-- Employees
INSERT INTO employees (branchid, name, position, phone) VALUES
(1, 'Suresh Iyer', 'Manager', '9876000001'),
(1, 'Neha Desai', 'Agent', '9876000002'),
(2, 'Rohit Menon', 'Manager', '9876000003'),
(2, 'Pooja Patel', 'Agent', '9876000004'),
(3, 'Karan Verma', 'Manager', '9876000005'),
(3, 'Anjali Singh', 'Agent', '9876000006');

-- Cars
INSERT INTO cars (model, make, year, cartype, registrationnumber, availabilitystatus, branchid, dailyrate) VALUES
('Swift', 'Maruti', 2020, 'Hatchback', 'KA09AB1234', 'Available', 1, 800),
('Ciaz', 'Maruti', 2021, 'Sedan', 'KA09AB5678', 'Available', 1, 1000),
('Creta', 'Hyundai', 2022, 'SUV', 'MH12CD3456', 'Available', 2, 1500),
('i20', 'Hyundai', 2019, 'Hatchback', 'MH12CD7890', 'Available', 2, 900),
('Seltos', 'Kia', 2021, 'SUV', 'DL05EF1234', 'Available', 3, 1200);

-- Locations
INSERT INTO locations (branchid, address) VALUES
(1, 'Bangalore Airport'),
(2, 'Mumbai Airport'),
(3, 'Delhi Airport');

-- Reservations
INSERT INTO reservations (customerid, carid, pickuplocationid, dropofflocationid, reservationdate, returndate, status) VALUES
(1, 1, 1, 1, CURRENT_DATE, CURRENT_DATE + INTERVAL '3 days', 'Active'),
(2, 2, 2, 2, CURRENT_DATE, CURRENT_DATE + INTERVAL '5 days', 'Active');

-- Rentals
INSERT INTO rentals (reservationid, rentalstartdate) VALUES
(1, CURRENT_DATE),
(2, CURRENT_DATE);

-- Payments
INSERT INTO payments (rentalid, amount, paymentdate, paymentmethod) VALUES
(1, 2400, CURRENT_DATE, 'UPI'),
(2, 4500, CURRENT_DATE, 'Credit Card');

-- Accident History
INSERT INTO accidenthistory (carid, accidentdate, description) VALUES
(1, CURRENT_DATE - INTERVAL '100 days', 'Minor scratch on bumper');

-- Transaction History
INSERT INTO transactionhistory (rentalid, action, actiondate) VALUES
(1, 'Rental Created', CURRENT_DATE),
(2, 'Rental Created', CURRENT_DATE);
