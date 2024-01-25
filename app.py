import re
import hashlib
import os


from flask import Flask, request, render_template, redirect, url_for, session
from pymongo import MongoClient
from functools import wraps
from datetime import datetime
from bson import ObjectId

app = Flask(__name__)

app.secret_key = 'b4ffc5b470c8b243452a9803b8b3d89a8e11c6127298dce8'
app.config['UPLOAD_FOLDER'] = './static/user_uploads/'
app.config['DEFAULT_PFP'] = './../static/user_uploads/pfp/blank-profile-picture.webp'


# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['blog']
users = db["users"]
postsColl = db["posts"]


def login_required(route_function):
    """
    Custom decorator to require login for a route.
    """
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if 'username' in session:
            # If the user is logged in, proceed to the original route function
            return route_function(*args, **kwargs)
        else:
            # If the user is not logged in, redirect to the login page
            return redirect(url_for('login'))
    return wrapper

def is_square(image):
    width, height = image.size
    return width == height

@app.route("/")
def home():
    if not 'username' in session:
        return render_template("index.html")
    else:
        return redirect(url_for('feed'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username").lower()
        email = request.form.get("email").lower()
        password = request.form.get("password")
        if not username or not email or not password:
            return render_template("register.html", error="Must enter a username, an Email, and a password")
        
        username_regex = r'^[a-zA-Z0-9_.]{6,}$'
        # Use re.match to check if the password matches the pattern
        username_regex = re.match(username_regex, username)
        if not username_regex:
            return render_template(
                "register.html", 
                error="Username must:<ul><li>contain at least 6 characters</li><li>Only alphanumeric characters and/or '_', '.'</li></ul>"
                )
        

        userFind = users.find_one({'username': username})
        if userFind:
            return render_template("register.html", error="Username already taken")

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        # Use re.match to check if the email matches the pattern
        emailMatch = re.match(email_regex, email)
        if not emailMatch:
            return render_template("register.html", error="Please enter a valid email")
        
        emailFind = users.find_one({'email': email})
        if emailFind:
            return render_template("register.html", error="Email already registered")

        password_regex = (
        r'^(?=.*[a-z])'     # At least one lowercase letter
        r'(?=.*[A-Z])'      # At least one uppercase letter
        r'(?=.*\d)'         # At least one digit
        r'(?=.*[@$!%*?&#])' # At least one special character
        r'[\w@$!%*?&#]{8,}$'  # At least 8 characters in total
        )
        # Use re.match to check if the password matches the pattern
        passMatch = re.match(password_regex, password)
        if not passMatch:
            return render_template(
                "register", 
                error="Password must have:<ul><li>At least one lowercase letter</li><li>At least one uppercase letter</li><li>At least one digit</li><li>At least one special character</li><li>At least 8 characters in total</li></ul>"
                )
        
        confPassword = request.form.get("confPassword")
        if not confPassword:
            return render_template(
                "register.html", 
                error="Must re-enter password"
                )
        if password != confPassword:
            return render_template(
                "register.html", 
                error="Password and re-entered password must match"
                )
        
        md5_hash = hashlib.md5()
        md5_hash.update(password.encode('utf-8'))

        # Get the hexadecimal representation of the hash
        hashedPass = md5_hash.hexdigest()
        users.insert_one({'username' : username, 'email' : email, 'hashPass' : hashedPass, 'details':{'pfp_url': app.config['DEFAULT_PFP'], 'cover_url': None, 'description': None}})
        return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        if not 'username' in session:
            return render_template("login.html")
        else:
            return redirect(url_for('feed'))
    else:
        email = request.form.get("email")
        if not email:
            return render_template("login.html", error="Must Enter Email Address")
        password = request.form.get('password')
        if not password:
            return render_template("login.html", error="Must Enter Password")
        
        # Create an MD5 hash object
        md5_hash = hashlib.md5()
        # Update the hash object with the bytes of the input string
        md5_hash.update(password.encode('utf-8'))

        # Get the hexadecimal representation of the hash
        hashedPass = md5_hash.hexdigest()

        validUser = users.find_one({'email':email,'hashPass':hashedPass})
        print(email)
        print(password)
        print(hashedPass)
        print(validUser)
        if validUser:
            session['username'] = validUser["username"]
            return redirect(url_for('feed'))
        else:
            return render_template("login.html", error="Wrong Email Or Password")
        

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    username = session["username"]
    if request.method == 'GET':
        userDetails = users.find_one({'username': username})['details']
        description = userDetails['description']
        pfp = userDetails['pfp_url']
        cover = userDetails['cover_url'] or ''
        posts = list(postsColl.find({'header.username': session['username']}))
        posts.reverse()
        return render_template('profile.html', username=username, description=description, pfp=pfp, cover=cover, posts=posts, navPfp=pfp)
    else:
        # User updated Their cover picture
        if 'new_cover' in request.files:
            newCover = request.files['new_cover']
            coverExtension = '.' + newCover.filename.split('.')[1]
            newCover.filename = username + '@cover' + coverExtension
            print(newCover.content_type)
            coverPath = os.path.join(app.config['UPLOAD_FOLDER'], 'cover/', newCover.filename)
            newCover.save(coverPath)
            coverPath = coverPath.replace('./', './../', 1)
            users.update_one({'username': username}, {'$set': {'details.cover_url': coverPath}})
        # User updated their profile picture
        if 'new_pfp' in request.files:
            newPfp = request.files['new_pfp']
            pfpExtension = '.' + newPfp.filename.split('.')[1]
            newPfp.filename = username + '@pfp' + pfpExtension
            pfpPath = os.path.join(app.config['UPLOAD_FOLDER'], 'pfp/', newPfp.filename)
            newPfp.save(pfpPath)
            pfpPath = pfpPath.replace('./', './../', 1)
            users.update_one({'username': username}, {'$set': {'details.pfp_url': pfpPath}})
        # User updated their description
        description = request.form.get("description")
        if description == None or len(description) <= 250:
            users.update_one({'username': username}, {'$set': {'details.description': description}})
        return redirect(url_for('profile'))

@app.route("/delete", methods=['POST'])
@login_required
def delete():
    postId = request.json['post_id']
    postsColl.delete_one({'_id': ObjectId(postId)})
    return redirect(url_for('profile'))

@app.route("/editor", methods=['GET', 'POST'])
@login_required
def editor():
    record = {'header':{'username':'', 'date':''}, 'body':''}
    if request.method == "POST":
        body = request.form.get("body")
        if not body:
            return render_template("editor.html", error="Feeling empty-minded today?")
        body = body.replace('\r\n', '<br/>')
        while body.endswith('<br/>'):
            body = body.removesuffix('<br/>')
        record['body'] = body
        record['header']['username'] = session['username']
        record['header']['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        postsColl.insert_one(record)
        return redirect(url_for("feed"))
    else:
        username = session['username']
        userDetails = users.find_one({'username': username})['details']
        pfp = userDetails['pfp_url']
        return render_template("editor.html", navPfp=pfp)

@app.route("/feed")
@login_required
def feed():
    posts = list(postsColl.find({}))
    for post in posts:
        post['pfp'] = users.find_one({'username': post['header']['username']})['details']['pfp_url']
    posts.reverse()

    username = session['username']
    userDetails = users.find_one({'username': username})['details']
    pfp = userDetails['pfp_url']
    return render_template("feed.html", posts=posts, navPfp=pfp)

@app.route('/logout')
@login_required
def logout():
    # Clear the session to log out the user
    session.pop('username', None)
    return redirect(url_for('login'))