from flask import Flask, request
from flask import render_template
from model import add_user
from model import get_user
from model import is_user_validate
from flask import Flask, session

app = Flask(__name__)
# 設定密鑰
app.secret_key = 'jjhs123$$!'  # 請使用隨機生成的密鑰

@app.route("/", methods=['GET'])
def hello():
    return "Hello, World! test1"

@app.route('/register')
def register_page():
 return render_template('register.html')

@app.route("/register_action", methods=['POST'])
def register_action_func():
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')
        password = str(password)
        add_user(email, password)

        return email + password

@app.route("/register_list", methods=['GET'])
def get_register_action():
     users = get_user()
     return str(users)


@app.route('/add_patient')
def add_patient():
    return render_template('add_patient.html')

@app.route('/add_patient_result', methods=['POST'])
def result():
    if request.method == 'POST':
        names = request.form.getlist('name')
        ages = request.form.getlist('age')

        print('[add_patient_result] request.form:', request.form )
        patient_dict = dict(zip(names, ages))
        print('[add_patient_result] patient_dict:', patient_dict )
        return str(patient_dict)


from flask import Flask, render_template, request, redirect, url_for, session, flash
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        passowrd = str(password)
        
        # 檢查使用者名稱和密碼

        if is_user_validate(username,password):
            session['username'] = username  # 將使用者名稱儲存在 session 中
            flash('登入成功！', 'success')
            return redirect(url_for('profile'))
        else:
            flash('使用者名稱或密碼錯誤！', 'danger')
    
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template('profile.html', username=session['username'])
    else:
        flash('請先登入！', 'warning')
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=False)