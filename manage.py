# Import necessary modules and classes
from flask.cli import FlaskGroup
from app import create_app, db
from flask import current_app
from datetime import datetime
import csv
import os

# Import models for users and products
from app.models.users import Users
from app.models.products import Products

# Import models for editor-related entities
from app.models.editor.customer import Customer
from app.models.editor.supplier import Supplier
from app.models.editor.company_products import CompanyProducts
from app.models.editor.company_orders import CompanyOrders
from app.models.editor.order_item import OrderItems

# Create a FlaskGroup CLI object with create_app function
cli = FlaskGroup(create_app=create_app)

# Define user data in JSON format
user_json = [
	{
		"name": "John Doe",
		"email": "john.doe@gmail.com",
		"password": "hello_john",
		"contact": "+1 (1234) 123 123"
	},
	{
		"name": "James Bond",
		"email": "james.bond@gmail.com",
		"password": "bond007",
		"contact": "+37 (1234) 567 890"
	},
	{
		"name": "Amy Brown",
		"email": "amy.brown@gmail.com",
		"password": "brownamy3",
		"contact": "+83 (4456) 285 847"
	},
	{
		"name": "John Wick",
		"email": "john.wick@gmail.com",
		"password": "johndog_1",
		"contact": "+49 (8712) 419 063"
	},
	{
		"name": "Helene Sebi",
		"email": "helene.sebi@gmail.com",
		"password": "helenelove1",
		"contact": "+33 (9331) 740 903"
	},
	{
		"name": "Maria Anders",
		"email": "maria.anders@gmail.com",
		"password": "nebraska123",
		"contact": "+1 202-918-2132"
	},
	{
		"name": "Antonio Moreno",
		"email": "antonio.moreno@gmail.com",
		"password": "@ntonio",
		"contact": "+355 69 142 4503"
	},
	{
		"name": "Christina Berglund",
		"email": "christina.berglund@gmail.com",
		"password": "Christin3",
		"contact": "+244 941 357 755"
	},
	{
		"name": "Frédérique Citeaux",
		"email": "frederique.citeaux@gmail.com",
		"password": "citeauxfrederique@123",
		"contact": "+297 290 4119"
	},
	{
		"name": "Laurence Lebihans",
		"email": "laurence.lebihans@gmail.com",
		"password": "thaifoodie@7",
		"contact": "+54 9 2954 73-5865"
	},
	{
		"name": "Michael Scott",
		"email": "michael.scott@gmail.com",
		"password": "worldsbestbossever_",
		"contact": "+61 493 338 894"
	},
	{
		"name": "Victoria Ashworth",
		"email": "victoria.ashworth@gmail.com",
		"password": "vic@$hworth",
		"contact": "+246 384 7383"
	},
	{
		"name": "Francisco Chang",
		"email": "francisco.chang@gmail.com",
		"password": "chan6co",
		"contact": "+357 99 203492"
	},
	{
		"name": "Sven Ottlieb",
		"email": "sven.ottilieb@gmail.com",
		"password": "sven.ottlieb@1",
		"contact": "+44 7781 699274"
	},
	{
		"name": "Aria Cruz",
		"email": "aria.cruz@gmail.com",
		"password": "@ria_Cruz",
		"contact": "+250 782 980 146"
	}
]

# Define product data in JSON format


product_json = [
	{
		"name": "Sergeant Rodog AI",
		"image": "/static/images/toy1.png",
		"rating": "5",
		"marked_price": "99.99",
		"selling_price": "94.99"
	},
	{
		"name": "Dwayne - The Bot - Johnson",
		"image": "/static/images/toy2.png",
		"rating": "5",
		"marked_price": "99.99",
		"selling_price": "94.99"
	},
	{
		"name": "RC Race Car - Mercedes",
		"image": "/static/images/toy3.png",
		"rating": "5",
		"marked_price": "49.99",
		"selling_price": "39.99"
	},
	{
		"name": "Hoblox - Build Houses",
		"image": "/static/images/toy4.png",
		"rating": "4",
		"marked_price": "29.99",
		"selling_price": "24.99"
	},
	{
		"name": "Kidzz Car",
		"image": "/static/images/toy5.png",
		"rating": "3",
		"marked_price": "19.99",
		"selling_price": "18.99"
	},
	{
		"name": "Toy Plain - Hoblox Edition",
		"image": "/static/images/toy6.png",
		"rating": "5",
		"marked_price": "19.99",
		"selling_price": "18.99"
	},
	{
		"name": "Crained - Hoblox Edition",
		"image": "/static/images/toy7.png",
		"rating": "5",
		"marked_price": "19.99",
		"selling_price": "16.99"
	},
	{
		"name": "Dumber - Hoblox Edition",
		"image": "/static/images/toy8.png",
		"rating": "5",
		"marked_price": "19.99",
		"selling_price": "17.99"
	},
	{
		"name": "Super Train - Hoblox Edition",
		"image": "/static/images/toy9.png",
		"rating": "4",
		"marked_price": "29.99",
		"selling_price": "24.99"
	},
	{
		"name": "Rubber Fish",
		"image": "/static/images/toy10.png",
		"rating": "5",
		"marked_price": "14.99",
		"selling_price": "12.99"
	},
	{
		"name": "Roller Bunny (Pink)",
		"image": "/static/images/toy11.png",
		"rating": "4",
		"marked_price": "9.99",
		"selling_price": "9.49"
	}
]


# Function to recreate the database by dropping and creating all tables
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

# Function to seed the database with initial data
def seeder():
    # Create users using user_json data
    for user in user_json:
        Users.create(user.get("name"), user.get("email"), user.get("password"), user.get("contact"))

    # Create products using product_json data
    for product in product_json:
        Products.create(product.get("name"), product.get("image"), product.get("rating"), product.get("marked_price"), product.get("selling_price"))

    # Seed editor-related entities from CSV files
    with open("app/editor_data/customer.csv", "r") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            try:
                Customer.create(int(row[0]), row[1], row[2], row[3], row[4], row[5])
            except:
                pass

    with open("app/editor_data/supplier.csv", "r") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            try:
                Supplier.create(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6])
            except:
                pass

    with open("app/editor_data/company_products.csv", "r") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            try:
                CompanyProducts.create(int(row[0]), row[1], int(row[2]), float(row[3]), row[4], int(row[5]))
            except:
                pass

    with open("app/editor_data/company_orders.csv", "r") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            try:
                CompanyOrders.create(int(row[0]), datetime.strptime(row[1], "%b %d %Y %I:%M:%S:%f%p"), int(row[2]), float(row[3]), int(row[4]))
            except:
                pass

    with open("app/editor_data/order_items.csv", "r
