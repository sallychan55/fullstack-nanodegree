from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shop, ShoppingItem, User

from flask import session as login_session
from functools import wraps
import re
import random
import string
import json
import httplib2
import requests

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Online Flea Market App"

# Connect to Database and create database session
engine = create_engine('sqlite:///shopitemswithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)


EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)


# Sign up
@app.route('/signup', methods=['GET', 'POST'])
def showSignup():
    if request.method == 'POST':
        if not (valid_username(request.form['name']) and valid_email(request.form['email'])):
            flash("Please set your name and email address")
            return render_template('signup.html')
        user_id = getUserID(request.form['email'])
        if user_id:
            flash("User %s alreay exists. Please login instead of sign up." % request.form['name'])
            return redirect(url_for('showLogin'))
        login_session['provider'] = "local"
        login_session['username'] = request.form['name']
        login_session['email'] = request.form['email']
        login_session['picture'] = "dummy"
        user_id = createUser(login_session)
        login_session['user_id'] = user_id
        flash("Now logged in as %s" % user.name)
        return redirect(url_for('showShops'))
    else:
        return render_template('signup.html')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session and 'user_id' not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated_function

# Create anti-forgery state token
@app.route('/login', methods=['GET', 'POST'])
def showLogin():
    if request.method == 'POST':
        user_id = getUserID(request.form['email'])
        if not user_id:
            flash("Invalid Login: User name %s doesn't match with email %s!" % (
            request.form['name'], request.form['email']))
            return redirect(url_for('showLogin'))
        user = getUserInfo(user_id)
        login_session['provider'] = "local"
        login_session['username'] = user.name
        login_session['email'] = user.email
        login_session['picture'] = "dummy"
        login_session['user_id'] = user.id
        flash("Now logged in as %s" % user.name)
        return redirect(url_for('showShops'))
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Connect facebook
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['facebook_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['provider']
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
        'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['user_id']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['provider']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['user_id']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['provider']

        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view Restaurant Information
@app.route('/shop/<int:shop_id>/items/JSON')
def shopItemsJSON(shop_id):
    shop = session.query(Shop).filter_by(id=shop_id).one()
    items = session.query(ShoppingItem).filter_by(shop_id=shop_id).all()
    return jsonify(shoppingItems=[i.serialize for i in items])


@app.route('/shop/<int:shop_id>/item/<int:item_id>/JSON')
def shopItemJSON(shop_id, item_id):
    item = session.query(ShoppingItem).filter_by(id=item_id).one()
    return jsonify(shopingItem=item.serialize)


@app.route('/shops/JSON')
def shopsJSON():
    shops = session.query(Shop).all()
    return jsonify(shops=[s.serialize for s in shops])


# Show all shops
@app.route('/')
@app.route('/shops/')
def showShops():
    shops = session.query(Shop).order_by(asc(Shop.name))
    return render_template('shops.html', shops=shops)

# Create a new shop
@app.route('/shop/new/', methods=['GET', 'POST'])
@login_required
def newShop():
    if request.method == 'POST':
        newShop = Shop(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newShop)
        flash('New Shop %s Successfully Created' % newShop.name)
        session.commit()
        return redirect(url_for('showShops'))
    else:
        return render_template('newShop.html')


# Edit a shop
@app.route('/shop/<int:shop_id>/edit/', methods=['GET', 'POST'])
@login_required
def editShop(shop_id):
    editedShop = session.query(Shop).filter_by(id=shop_id).one()
    if editedShop.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this shop. \
        Please create your own shop in order to edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name'] and request.form['name'] != editedShop.name:
            editedShop.name = request.form['name']
            flash('Shop Successfully Edited %s' % editedShop.name)
        return redirect(url_for('showShops'))
    else:
        return render_template('editshop.html', shop=editedShop)


# Delete a shop
@app.route('/shop/<int:shop_id>/delete/', methods=['GET', 'POST'])
@login_required
def deleteShop(shop_id):
    shopToDelete = session.query(Shop).filter_by(id=shop_id).one()
    if shopToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this shop. \
        Please create your own shop in order to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(shopToDelete)
        flash('%s Successfully Deleted' % shopToDelete.name)
        session.commit()
        return redirect(url_for('showShops', shop_id=shop_id))
    else:
        return render_template('deleteshop.html', shop=shopToDelete)


# Show a shopping items
@app.route('/shop/<int:shop_id>/')
@app.route('/shop/<int:shop_id>/items/')
def showItem(shop_id):
    shop = session.query(Shop).filter_by(id=shop_id).one()
    creator = getUserInfo(shop.user_id)
    items = session.query(ShoppingItem).filter_by(shop_id=shop_id).all()
    if 'user_id' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicitems.html', items=items, shop=shop, creator=creator)
    else:
        return render_template('items.html', items=items, shop=shop, creator=creator)


# Create a new shopping item
@app.route('/shop/<int:shop_id>/items/new/', methods=['GET', 'POST'])
@login_required
def newShoppingItem(shop_id):
    shop = session.query(Shop).filter_by(id=shop_id).one()
    if login_session['user_id'] != shop.user_id:
        return "<script>function myFunction() {alert('You are not authorized to add shopping items to this shop. \
        Please create your own shop in order to add items.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        newItem = ShoppingItem(name=request.form['name'], description=request.form['description'],
                               price=request.form['price'], category=request.form['category'],
                               shop_id=shop_id, user_id=shop.user_id)
        session.add(newItem)
        session.commit()
        flash('New Shopping %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showItem', shop_id=shop_id))
    else:
        return render_template('newItem.html', shop_id=shop_id)


# Edit a shopping item
@app.route('/shop/<int:shop_id>/item/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def editShoppingItem(shop_id, item_id):
    editedItem = session.query(ShoppingItem).filter_by(id=item_id).one()
    shop = session.query(Shop).filter_by(id=shop_id).one()
    if login_session['user_id'] != shop.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit items to this shop. \
        Please create your own shop in order to edit items.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        isEdited = False
        if request.form['name'] and editedItem.name != request.form['name']:
            editedItem.name = request.form['name']
            isEdited = True
        if request.form['description'] and editedItem.description != request.form['description']:
            editedItem.description = request.form['description']
            isEdited = True
        if request.form['price'] and editedItem.price != request.form['price']:
            editedItem.price = request.form['price']
            isEdited = True
        if request.form['category'] and editedItem.category != request.form['category']:
            editedItem.category = request.form['category']
            isEdited = True
        if isEdited:
            session.add(editedItem)
            session.commit()
            flash('Shopping Item Successfully Edited')
        return redirect(url_for('showItem', shop_id=shop_id))
    else:
        return render_template('edititem.html', shop_id=shop_id, item_id=item_id, item=editedItem)


# Delete a shopping item
@app.route('/shop/<int:shop_id>/item/<int:item_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteShoppingItem(shop_id, item_id):
    shop = session.query(Shop).filter_by(id=shop_id).one()
    itemToDelete = session.query(ShoppingItem).filter_by(id=item_id).one()
    if login_session['user_id'] != shop.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete items to this shop. \
        Please create your own shop in order to delete items.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Shopping Item Successfully Deleted')
        return redirect(url_for('showItem', shop_id=shop_id))
    else:
        return render_template('deleteItem.html', item=itemToDelete)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
        elif login_session['provider'] == 'facebook':
            fbdisconnect()
        else:
            del login_session['provider']
            del login_session['username']
            del login_session['email']
            del login_session['user_id']
        flash("You have successfully been logged out.")
        return redirect(url_for('showShops'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showShops'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
