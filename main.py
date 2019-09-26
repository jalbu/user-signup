from flask import Flask, request, redirect, render_template
import jinja2, os
import pdb
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)

app.config['DEBUG'] = True    


@app.route("/")
def display():
    template = jinja_env.get_template("main.html")
    return template.render()

@app.route("/", methods=['post'])
def validate_user():
    # If string is a valid string, then return true, else false
    def validate_string(field,val_string):
        error = ''
        if val_string == '':
            error = field + 'cannot be empty'
        elif ' ' in val_string:
            error = field + 'must not contain spaces.'
        elif len(val_string) < 3 or len(val_string) > 20:
            error = field + 'must be between 3 and 20 characters'
        return error
            
        

    username = request.form['username']
    password = request.form['password']
    verify_pass = request.form['verify_pass']
    email = request.form['email']
    user_error = ''
    pass_error = ''
    verify_pass_error = ''
    email_error = ''
    
    # See if fields are empty, have spaces, or not the right length
    user_error = validate_string('Username ', username)
    pass_error = validate_string('Password ', password)
    verify_pass_error = validate_string('Validate Password ', verify_pass)
    if len(email) > 0:
        email_error = validate_string('Email ',email)
        if (email.count('@') != 1 or email.count(".") != 1):
            email_error = "Email must contain one '@' and one '.'"
    
    if password != verify_pass:
        verify_pass_error = "Passwords do not match"
        password = ""
        verify_pass = ""

    # Clear passwords if password or verify pass has an error
    if pass_error != '' or verify_pass_error != '':
        password = ""
        verify_pass = ""

    if user_error == '' and pass_error == '' and verify_pass_error == '' and email_error == '':
        # Fill this in
        return redirect(f'/welcome?user={username}')
    else:
        # template = jinja_env.get_template("main.html")
        return render_template('main.html', 
        username=username,
        password=password,
        verify_pass=verify_pass,
        email=email,
        user_error=user_error,
        pass_error=pass_error,
        verify_pass_error=verify_pass_error,
        email_error=email_error)

@app.route('/welcome')
def welcome_page():
    username = request.args.get('user')
    return render_template('welcome.html',username=username)

app.run()