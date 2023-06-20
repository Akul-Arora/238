from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from app.models.products import Products
from app.models.address import Address
from app.models.users import Users
from app.models.orders import Orders
from app import db

from flask_cors import cross_origin

# Create a Blueprint named 'views' with the URL prefix '/'
views = Blueprint('views', __name__, url_prefix="/")

# Login route
@views.route('/')
@cross_origin()
def login():
    try:
        return render_template("/login/login.html")
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

# Dashboard route
@views.route('/dashboard')
@cross_origin()
def dashboard():
    try:
        # Query all products from the database
        query = "select * from products;"
        products = db.engine.execute(query).all()
        return render_template("/dashboard/dashboard.html", products=products, user_id=session.get('user_id'))
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

# Profile route
@views.route('/profile')
@cross_origin()
def profile():
    try:
        # Get the user ID from the request arguments
        user_id = request.args.get("id")

        # Query the user from the database
        user_query = f"select * from users where id='{user_id}';"
        user = db.engine.execute(user_query).first()

        # Query orders for the user
        order_query = f"select p.image, p.name, o.amount from products p right join orders o on o.user_id={user['id']} and p.id=o.product_id;"
        orders = db.engine.execute(order_query).all()

        # Query tickets for the user
        ticket_query = f"select * from tickets where user_id='{user['id']}';"
        tickets = db.engine.execute(ticket_query).all()

        # Query addresses for the user
        address_query = f"select * from address where user_id='{user['id']}'"
        addresses = db.engine.execute(address_query).all()

        return render_template("/profile/profile.html", user=user, orders=orders, addresses=addresses, tickets=tickets, user_id=session.get("user_id"))
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

# Order route
@views.route('/order')
@cross_origin()
def order():
    try:
        # Get the product ID from the request arguments
        product_id = request.args.get("id")
        if not product_id:
            return jsonify({
                "message": "No product for purchase!",
                "status": "error"
            }), 400

        # Query the product from the database
        query = f"select * from products where id={product_id};"
        product = db.engine.execute(query).first()

        # Query addresses for the user
        address_query = f"select * from address where user_id='{session.get('user_id')}'"
        addresses = db.engine.execute(address_query).all() or []

        return render_template("/order/order.html", product=product, addresses=addresses, user_id=session.get('user_id'))
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

# Help route
@views.route("/help")
@cross_origin()
def help_page():
    try:
        return render_template("/help/help.html", user_id=session.get('user_id'))
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

# Editor route
@views.route("/editor")
@cross_origin()
def editor():
    try:
        return render_template("/editor/editor.html")
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

    
