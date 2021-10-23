"""Blogly application."""


# from operator import lshift
from flask import Flask, render_template, request, redirect

from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = '12345abcde'

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def user_page():

    users = User.query.all()
    return render_template('users/users.html', users=users )

@app.route('/users/new', methods=["GET"])
def new_page():
    """New user form"""
    return render_template('/users/new_page.html')

@app.route("/users/new", methods=["POST"])
def new_user():
    """form submission for a new user"""


    new_user = User(first_name=request.form['first_name'], last_name=request.form['last_name'], image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show user page"""
    user = User.query.get_or_404(user_id)
    return render_template('/users/show_page.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """form to edit page"""
    user = User.query.get_or_404(user_id)
    return render_template('/users/edit_page.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """ Form submission for update"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']


    db.session.add(user)
    db.session.commit()

    return redirect("/")

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")
