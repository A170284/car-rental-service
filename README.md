# 🚗 Car Rental Service

A Flask + PostgreSQL web application for managing a car rental business.  
Supports branches, cars, customers, employees, reservations, rentals, payments, accidents, and transaction history.  

---

## 📦 Features
- Add, edit, delete, and view all entities (branches, cars, customers, etc.)
- Rental start/end with automatic cost calculation
- Transaction history tracking
- PostgreSQL relational schema with dummy data
- Fully container-ready (can extend with Docker later)

---

## 🛠️ Requirements
- **Python 3.10+** (works with 3.13 too)
- **PostgreSQL 14+** (tested with PostgreSQL 18)
- **Git**

Python dependencies are in `requirements.txt`:
```txt
Flask
Flask-SQLAlchemy
pg8000
python-dotenv
