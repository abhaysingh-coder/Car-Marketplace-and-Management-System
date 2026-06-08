# 🚗 Car Marketplace and Management System

A full-stack Django-based Car Marketplace and Management System that allows users to buy, sell, rent, service, and predict car prices through a role-based platform consisting of Customer, Staff, and Admin panels.

## 📌 Project Overview

This project is designed to provide a complete automobile marketplace solution where customers can browse vehicles, buy cars, sell their own vehicles, rent cars, request vehicle services, predict car prices using Machine Learning, and receive car recommendations based on vehicle preferences.

The system includes separate dashboards and management panels for Customers, Staff, and Administrators to ensure secure and organized operations.

---

## ✨ Features

### 👤 Customer Features

* User Registration & Login
* Car Collection Browsing
* Car Details Page
* Buy Car Request
* Sell Car Request
* Rent Car Request
* Vehicle Service Request
* Car Price Prediction
* Car Recommendation System
* Order History
* Prediction History
* Recommendation History
* Profile Management
* Notifications

---

### 👨‍💼 Staff Features

* Staff Dashboard
* Manage Buy Requests
* Manage Selling Requests
* Manage Renting Requests
* Manage Service Requests
* Complete Vehicle Deliveries
* Customer Notifications
* Profile Management

---

### 👨‍💻 Admin Features

* Admin Dashboard
* Customer Management
* Staff Management
* Buy Request Management
* Sell Request Management
* Rent Request Management
* Service Request Management
* Staff Approval System
* System Notifications
* Profile Management

---

## 🤖 Machine Learning Features

### Car Price Prediction

Predict vehicle prices using Machine Learning based on:

* Make
* Model
* Year
* Engine HP
* Engine Cylinders
* Transmission Type
* Driven Wheels
* Vehicle Size
* Vehicle Style
* Popularity
* Highway MPG
* City MPG

### Car Recommendation System

Provides similar vehicle recommendations based on:

* Brand
* Model
* Vehicle Specifications
* Market Category
* Similar Features

---

## 🏗️ Project Structure

```text
Car Marketplace and Management System
│
├── Admin/
├── Staff/
├── mainapp/
├── static/
│   ├── CSS/
│   ├── JS/
│   └── Image/
│
├── Data/
├── Data Science/
│   ├── Models/
│   ├── Encoder/
│   └── Notebooks/
│
├── templates/
├── manage.py
└── db.sqlite3
```

## 🛠️ Technology Stack

### Backend

* Python
* Django
* SQLite

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap
* Font Awesome

### Data Science

* Pandas
* NumPy
* Scikit-Learn
* TensorFlow
* Joblib

### Version Control

* Git
* GitHub

---

## 🔐 Role-Based Access Control

The system supports three user roles:

### Admin

* Manage staff
* Manage customers
* Manage all requests
* Approve operations

### Staff

* Process approved requests
* Manage vehicle operations
* Update request status

### Customer

* Buy vehicles
* Sell vehicles
* Rent vehicles
* Request services
* Use ML features

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/abhaysingh-coder/Car-Marketplace-and-Management-System.git
```

### Move into Project Directory

```bash
cd Car-Marketplace-and-Management-System
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Migrations

```bash
python manage.py migrate
```

### Start Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## 📊 Future Improvements

* Online Payment Gateway
* Email Notifications
* SMS Notifications
* Vehicle Image Upload System
* AI Chatbot Support
* Advanced Recommendation Engine
* Cloud Deployment
* REST API Integration

---

## 👨‍💻 Developer

**Abhay Singh**

B.Tech Computer Science Engineering

GitHub:
https://github.com/abhaysingh-coder

---

## 📄 License

This project is developed for educational and learning purposes.
