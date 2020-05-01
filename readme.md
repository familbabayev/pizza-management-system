# Pizza Management System
Simple project for ordering pizzas.
## Contents
* [General Info](#general-info)
* [Technologies used](#technologies-used)
* [Setup](#setup)
* [Usage](#usage)
* [Relational Database diagram](#relational-database-diagram)
* [Class diagram of Decorator Pattern](#class-diagram-of-decorator-pattern)

## General Info
The application includes the following functionalities:
* Registration of a new user
* Login as user and admin
* As a user
  * Selecting pizza and customizing toppings and quantity
  * Adding multiple pizzas to basket
  * Ordering pizza
* As an admin
  * Adding new pizza
  * Viewing all orders
* Notifying users when new pizza added

## Technologies used
Project created with:
* Python3
* Tkinter
* SQLite

## Setup
1. Install python3
2. Clone this repository
```
git clone https://github.com/familbabayev/Pizza_Management_System.git
```
3. Install the requirements of this repository
```
pip install -r requirements.txt
```
4. Run main.py
```
python3 main.py
```
## Usage
If you don't want to have empty database at beginning, uncomment the sample database instructions in main.py, run it once and comment it again.
## Relational Database diagram
![PizzaRelationalDatabase](https://user-images.githubusercontent.com/44068684/80802158-9ac77a00-8bbf-11ea-9c0b-1a53c72e344d.png)
## Class diagram of Decorator Pattern
![PizzaClassDiagram](https://user-images.githubusercontent.com/44068684/80802167-a024c480-8bbf-11ea-9a5f-540b1be69b2a.png)
