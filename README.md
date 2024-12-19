# Django ToDoApp

A simple ToDo application built with Django.

## Requirements

- Python 3.x
- Django 4.x

## Getting Started

1. **Clone the Repository**
   ```bash
   git clone https://github.com/gimmevsc/todoapp.git

2. **Install Required Packages Run the following command to install the necessary packages:
   ```bash
   pip install -r requirements.txt

3. Set Up Environment Variables
   Create a .env file in the project root by copying .env.example:
   ```bash
   cp .env.example .env
   ```

4. Make Database Migrations Run the migrations to set up your database:
   ```bash
   python3 manage.py makemigrations todoapp

   python3 manage.py migrate

5. Start the Development Server Use the following command to run the development server:
   ```bash
   python3 manage.py runserver
