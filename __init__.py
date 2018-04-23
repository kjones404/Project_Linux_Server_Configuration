#!/usr/bin/env python3

""" Project Build an Item Catalog

This project is part of the Udacity Full Stack Nanodegree program.

"""


import random
import string
import httplib2
import json
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, \
    jsonify, session as login_session, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from database_setup import Base, Collection, MovieItem, User


app = Flask(__name__)

# Set Google OAuth Information
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Fresh Tomatoes v3"

# Configure Database
engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    """Builds Login Session.

    Args:
        None
    Behavior:
        Builds anti forgery state token.
    Returns:
        Login template & state token.
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Logs user into Google.

    Args:
        None
    Behavior:
        Checks for valid state token. Preforms Googles OAuth2 authorization.
        Checks login status and creates login session if needed.
    Returns:
        Google username.
    """
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
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']

    # See if a user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += login_session['username']
    flash("you are now logged in as %s" % login_session['username'])
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """Disconnects from Google.

    Args:
        None
    Behavior:
        Attempts to disconnect form google. If successful deletes user data.
    Returns:
        Redirect URL and disconnect status.
    """
    access_token = login_session.get('access_token')
    if access_token is None:
        flash("Current user not connected.")
        return redirect(url_for('home'))
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % \
        login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        flash("Successfully logged out.")
        return redirect(url_for('home'))
    else:
        flash("Failed to revoke token for given user.")
        return redirect(url_for('home'))


@app.route('/collections/JSON')
def allJSON():
    """JSON Query for whole Database

    Args:
        None
    Behavior:
        Pulls requested DB data
    Returns:
        Provides request DB data in JSON format.
    """
    collection = session.query(Collection).all()
    return jsonify(collection=[i.serialize for i in collection])


@app.route('/collections/<int:collection_id>/JSON')
def collectionJSON(collection_id):
    """JSON Query for requested collection.

    Args:
        collection_id = Primary_key for collection
    Behavior:
        Pulls requested DB data
    Returns:
        Provides request DB data in JSON format.
    """
    collection = session.query(Collection).filter_by(id=collection_id).one()
    movies = session.query(MovieItem).filter_by(
        collection_id=collection_id).all()
    return jsonify(MovieItems=[i.serialize for i in movies])


@app.route('/collections/<int:collection_id>/<int:movie_id>/JSON')
def movieJSON(collection_id, movie_id):
    """JSON Query for requested movie.

    Args:
        collection_id: Primary_key for collection
        movie_id: Primary_key for movie
    Behavior:
        Pulls requested DB data
    Returns:
        Provides request DB data in JSON format.
    """
    collection = session.query(Collection).filter_by(id=collection_id).one()
    movie = session.query(MovieItem).filter_by(id=movie_id).one()
    return jsonify(MovieItem=movie.serialize)


@app.route('/')
@app.route('/home')
def home():
    """Display application home page.

    Args:
        None
    Behavior:
        Collect list of collections
    Returns:
        home page with collection list.
    """
    collection = session.query(Collection).all()
    return render_template('home.html', collection=collection)


# Create route for newMovieItem function here
@app.route('/collections/add', methods=['GET', 'POST'])
@app.route('/collections/add/', methods=['GET', 'POST'])
def addCollection():
    """Create a new movie collection.

    Args:
        None
    Behavior:
        Checks login status. Handle post or get requests. Collects new
        collection name and commits change to database.
    Returns:
        Get request: template to create a new collection.
        Post request: flash update and redirect to home.html
    """
    if 'username' not in login_session:
        collection = session.query(Collection).all()
        flash("Login before you create a new collection.")
        return render_template('home.html', collection=collection)
    elif request.method == 'POST':
        newItem = Collection(name=request.form['name'],
                             user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash("New collection created!")
        return redirect(url_for('home'))
    else:
        return render_template('add.html')


@app.route('/collections/<int:collection_id>')
@app.route('/collections/<int:collection_id>/')
def movieCollection(collection_id):
    """Display movie collection.

    Args:
        collection_id: Primary_key for collection
    Behavior:
        Checks login status. Collects collection data
    Returns:
        Collection website based on login status.
    """
    collection = session.query(Collection).filter_by(id=collection_id).one()
    creator = getUserInfo(collection.user_id)
    items = session.query(MovieItem).filter_by(collection_id=collection.id)
    if ('username' not in login_session or creator.id !=
       login_session['user_id']):
        return render_template('collection_pub.html', collection=collection,
                               items=items)
    else:
        return render_template('collection.html', collection=collection,
                               items=items)


@app.route('/collections/<int:collection_id>/edit', methods=['GET', 'POST'])
@app.route('/collections/<int:collection_id>/edit/', methods=['GET', 'POST'])
def editCollection(collection_id):
    """Edit movie collection data.

    Args:
        collection_id: Primary_key for collection
    Behavior:
        Checks login status. Handle post or get requests. Collects new
        collection data. Commit changes to database.
    Returns:
        Get request: template to edit collection data.
        Post request: flash update and redirect to collection
    """
    collection = session.query(Collection).filter_by(id=collection_id).one()
    creator = getUserInfo(collection.user_id)
    items = session.query(MovieItem).filter_by(collection_id=collection.id)
    if ('username' not in login_session or creator.id !=
       login_session['user_id']):
        flash("Please login as the collection owner.")
        return redirect(url_for('home'))
    elif request.method == 'POST':
        if request.form['name']:
            collection.name = request.form['name']
        session.add(collection)
        session.commit()
        flash("Collection Updated!")
        return redirect(url_for('movieCollection',
                                collection_id=collection_id))
    else:
        return render_template(
            'edit.html', collection_id=collection_id)


@app.route('/collections/<int:collection_id>/delete', methods=['GET', 'POST'])
@app.route('/collections/<int:collection_id>/delete/', methods=['GET', 'POST'])
def deleteCollection(collection_id):
    """Delete collection data.

    Args:
        collection_id: Primary_key for collection
    Behavior:
        Checks login status. Handle post or get requests. Deletes collection
        data from database.
    Returns:
        Get request: confirm request to delete data
        Post request: flash update and redirect to home.html
    """
    collection = session.query(Collection).filter_by(id=collection_id).one()
    creator = getUserInfo(collection.user_id)
    if ('username' not in login_session or creator.id !=
       login_session['user_id']):
        flash("Please login as the collection owner.")
        return redirect(url_for('home'))
    items = session.query(MovieItem).filter_by(collection_id=collection.id)
    if request.method == 'POST':
        session.delete(collection)
        session.commit()
        flash("Collection Deleted!")
        return redirect(url_for('home'))
    else:
        return render_template('delete.html', collection_id=collection_id)


@app.route('/collections/<int:collection_id>/new', methods=['GET', 'POST'])
@app.route('/collections/<int:collection_id>/new/', methods=['GET', 'POST'])
def newMovie(collection_id):
    """Create new movie.

    Args:
        collection_id: Primary_key for collection
    Behavior:
        Checks login status. Handle post or get requests. Collects new movie
        information. Commits new movie to database.
    Returns:
        Get request: template for new movie data
        Post request: flash update and redirect to movie collection
    """
    collection = session.query(Collection).filter_by(id=collection_id).one()
    creator = getUserInfo(collection.user_id)
    if ('username' not in login_session or creator.id !=
       login_session['user_id']):
        flash("Please login as the collection owner.")
        return redirect(url_for('home'))
    items = session.query(MovieItem).filter_by(collection_id=collection.id)
    if request.method == 'POST':
        newItem = MovieItem(
            title=request.form['title'],
            year=request.form['year'],
            description=request.form['description'],
            img=request.form['img'],
            collection_id=collection_id,
            user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash("New movie created!")
        return redirect(url_for('movieCollection',
                                collection_id=collection_id))
    else:
        return render_template('newmovie.html', collection_id=collection_id)


# Create route for editmovieItem function here
@app.route('/collections/<int:collection_id>/<int:movie_id>/edit',
           methods=['GET', 'POST'])
@app.route('/collections/<int:collection_id>/<int:movie_id>/edit/',
           methods=['GET', 'POST'])
def editMovie(collection_id, movie_id):
    """Edit movie data.

    Args:
        collection_id: Primary_key for collection
        movie_id: Primary_key for movie
    Behavior:
        Checks login status. Handle post or get requests. Collects new movie
        information. Commits movie data changes to database.
    Returns:
        Get request: template for edit movie data
        Post request: flash update and redirect to movie collection
    """
    collection = session.query(Collection).filter_by(id=collection_id).one()
    creator = getUserInfo(collection.user_id)
    if ('username' not in login_session or creator.id !=
       login_session['user_id']):
        flash("Please login as the collection owner.")
        return redirect(url_for('home'))
    items = session.query(MovieItem).filter_by(collection_id=collection.id)
    editedItem = session.query(MovieItem).filter_by(id=movie_id).one()
    if request.method == 'POST':
        if request.form['title']:
            editedItem.title = request.form['title']
        if request.form['year']:
            editedItem.year = request.form['year']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['img']:
            editedItem.img = request.form['img']
        session.add(editedItem)
        session.commit()
        flash("Movie Updated!")
        return redirect(url_for('movieCollection',
                                collection_id=collection_id))
    else:
        return render_template('editmovie.html', collection_id=collection_id,
                               movie_id=movie_id, item=editedItem)


# Create a route for deleteMovieItem function here
@app.route('/collections/<int:collection_id>/<int:movie_id>/delete',
           methods=['GET', 'POST'])
@app.route('/collections/<int:collection_id>/<int:movie_id>/delete/',
           methods=['GET', 'POST'])
def deleteMovie(collection_id, movie_id):
    """Delete movie data.

    Args:
        collection_id: Primary_key for collection
        movie_id: Primary_key for movie
    Behavior:
        Checks login status. Handle post or get requests. Deletes movie
        from database.
    Returns:
        Get request: confirm request to delete movie
        Post request: flash update and redirect to movie collection
    """
    collection = session.query(Collection).filter_by(id=collection_id).one()
    creator = getUserInfo(collection.user_id)
    if ('username' not in login_session or creator.id !=
       login_session['user_id']):
        flash("Please login as the collection owner.")
        return redirect(url_for('home'))
    items = session.query(MovieItem).filter_by(collection_id=collection.id)
    itemToDelete = session.query(MovieItem).filter_by(id=movie_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Movie Deleted!")
        return redirect(url_for('movieCollection',
                                collection_id=collection_id))
    else:
        return render_template('deletemovie.html', item=itemToDelete)


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
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


# set server settings
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run()
