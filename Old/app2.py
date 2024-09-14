from flask import Flask, request
from flask import render_template

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
        input_dic = {}

        name = request.form.get('name')
        password = request.form.get('password')
        
        return name +str(password)
    
    return 'default value'

if __name__ == "__main__":
    app.run(debug=False)