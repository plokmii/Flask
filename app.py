from flask import Flask, request
from flask import render_template
from model import add_user
from model import add_patient_toDB,get_one_patient
from model import Patient
from model import get_user, get_patient
from model import is_user_validate
from flask import Flask, session
from model import update_patient_name
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import os




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
        patient_ids = request.form.getlist('patient_id')
        ages = request.form.getlist('age')
        genders = request.form.getlist('gender')
        drinkings = request.form.getlist('drinking')
        remarkss = request.form.getlist('remarks')
        biopsyDates = request.form.getlist('biopsyDate')
        files = request.files.getlist('file')

        print("names:",names)
        print("patient_ids:",patient_ids)
        print("ages:",ages)
        print("genders:",genders)
        print("drinkings:",drinkings)
        print("remarkss:",remarkss)
        print("biopsyDates:",biopsyDates)
        print("files:",files)
       
        patient_show_list=[]
        print("patient_show_list:",patient_show_list)
        #print(type(names))
        for i in range(len(names)):
            name=names[i]
            patient_id = patient_ids[i]
            age=ages[i]
            gender=genders[i]
            drinking=drinkings[i]
            remarks=remarkss[i]
            biopsyDate=biopsyDates[i]
            biopsyDate = datetime.strptime(biopsyDate, '%Y-%m-%d').date()  # 假設日期格式為 'YYYY-MM-DD'
            file=files[i]
            if file:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            patient_show_list.append(name+'_'+str(age)+'_'+gender+'_'+drinking+'_'+remarks+'_'+str(biopsyDate)+str(patient_id))
            add_patient_toDB(name,patient_id, age,gender,drinking,remarks,biopsyDate)

        return str(patient_show_list)
    
@app.route("/patient_list", methods=['GET'])
def get_patient_action():
     patients = get_patient()
     
     return render_template('show_patients.html', patients=patients)

@app.route('/edit_patient/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    print("request.method:",request.method )
    print("patient_id:",patient_id)
    patient = get_one_patient(patient_id)
    
    if request.method == 'POST':
        # 假設你從表單中取得資料並更新 user 的 name 和 gender
        name = request.form['name']
        gender = request.form['gender']
        age = request.form['age']
        drinking = request.form['drinking']
        remarks = request.form['remarks']
        biopsyDate = request.form['biopsyDate']
        biopsyDate = datetime.strptime(biopsyDate, '%Y-%m-%d').date()  # 假設日期格式為 'YYYY-MM-DD'
        print("name:",name)
        print("gender:",gender)
        print("age:",age)
        print("drinking:",drinking)
        print("remarks:",remarks)
        print("biopsyDate:",biopsyDate)
        update_patient_name(patient_id, name,gender,age,drinking,remarks,biopsyDate)
        #db.session.commit() 
        return redirect(url_for('get_patient_action'))
    
    return render_template('edit_patient.html', patient=patient)


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


#upload pdf 
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/upload_page')
def upload_page():
    return render_template('upload_page.html')

@app.route('/upload_action', methods=['POST'])
def upload_file():
    # if 'file' not in request.files:
    #     return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f"File {filename} uploaded successfully!"
    return "Invalid file type"


if __name__ == "__main__":
    app.run(debug=False)