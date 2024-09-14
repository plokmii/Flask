from flask import Flask, request
from flask import render_template
from model import add_user
from model import get_user

app = Flask(__name__)
@app.route("/", methods=['GET'])
def hello():
    return "Hello, World!"

@app.route('/register')
def register_page():
 return render_template('register.html')

@app.route("/register_action", methods=['POST'])
def register_action_func():
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')
        add_user(email, password)

        return email + str(password)

@app.route("/register_list", methods=['GET'])
def get_register_action():
     users = get_user()
     return str(users)

if __name__ == "__main__":
    app.run(debug=False)