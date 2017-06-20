from flask import Flask, request, redirect
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['POST', 'GET'])
def index():
    template = jinja_env.get_template('index.html')
    return template.render(title = 'User Signup')

@app.route('/signup', methods=['POST'])
def signup():
    template = jinja_env.get_template('index.html')

    username_error = ''
    password_error = ''
    password_verify_error = ''
    user_email_error = ''

    username = request.form['username']
    if check_valid(username) == True:
        good_username = username
    else:
        username = ''
        username_error = 'Not a valid username.'
    password = request.form['password']
    if check_valid(password) == True:
        good_password = password
    else:
        password_error = 'Not a valid password.'
    password_verify = request.form['password_verify']
    if password_verify != password:
        password_verify_error = 'Passwords do not match.'
    user_email = request.form['user_email']
    if check_email(user_email) == False:
        user_email_error = 'Not a valid email address.'
    if username_error or password_error or password_verify_error or user_email_error:
        return template.render(title = 'User Signup', username = username, user_email = user_email, username_error = username_error, password_error = password_error, password_verify_error = password_verify_error, user_email_error = user_email_error)
    else:
        return redirect('/greeting?username=' + good_username)

@app.route('/greeting')
def greeting():
    template = jinja_env.get_template('greeting.html')
    username = request.args.get('username')
    return template.render(title = 'Hello, ' + username + '!', username = username)

def check_valid(password):
    for char in password:
        if char == ' ':
            return False
    if len(password) < 3:
        return False
    elif len(password) > 20:
        return False
    else:
        return True

def check_email(user_email):
    if user_email == '':
        return True
    if len(user_email) > 20 or len(user_email) < 3:
        return False
    at_count = 0
    dot_count = 0
    for char in user_email:
        if char == ' ':
            return False;
        if char.isalnum() == False:
            if char == '@':
                at_count += 1
            elif char == '.':
                dot_count += 1
            else:
                return False
    if dot_count != 1:
        return False
    elif at_count != 1:
        return False
    return True

app.run()
