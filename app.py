from flask import Flask, request
from flask import render_template
from model import add_user
from model import add_patient_toDB,get_one_patient,get_patients_by_filters
from model import Patient
from model import get_user, get_patient
from model import is_user_validate,is_user_validate_editor
from flask import Flask, session
from model import update_patient_name
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from flask import Flask, render_template, send_from_directory
import pandas as pd
from model import add_patient_extend_data
from model import get_patient_extend_data


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
        add_user(email, password,2)

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
        patient_str_ids = request.form.getlist('patient_str_id')
        
        genders = request.form.getlist('gender')
        ages = request.form.getlist('age')
        drinkings = request.form.getlist('drinking')
        remarkss = request.form.getlist('remarks')
        biopsyDates = request.form.getlist('biopsyDate')
        files = request.files.getlist('file')

        print("names:",names)
        print("patient_str_ids:",patient_str_ids)
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
            patient_str_id = patient_str_ids[i]
            age=ages[i]
            gender=genders[i]
            drinking=drinkings[i]
            remarks=remarkss[i]
            biopsyDate=biopsyDates[i]
            biopsyDate = datetime.strptime(biopsyDate, '%Y-%m-%d').date()  # 假設日期格式為 'YYYY-MM-DD'
            file=files[i]
            if file:
                filename = str(patient_str_id) +'_chartID.pdf'
                print("filename:",filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            patient_show_list.append(name+'_'+str(patient_str_id)+'_'+gender+'_'+str(age)+'_'+drinking+'_'+remarks+'_'+str(biopsyDate))
            add_patient_toDB(name,patient_str_id, gender,age,drinking,remarks,biopsyDate)

        return str(patient_show_list)
    
@app.route("/patient_list", methods=['GET', 'POST'])
def get_patient_action():
    print("session:",session)
    if request.method == 'POST':
        # 按鈕被按下，下載CSV
        return download_csv()

    
    if "user_level" in session and session["user_level"]==1:  
        patients = get_patient()
        return render_template('show_patients.html', patients=patients)
    else:
        return("You are not editor")


def download_csv():
    # 連接資料庫並讀取表格
    patients = get_patient()
    df = pd.DataFrame([patient.__dict__ for patient in patients])
    df = df[['name','age','remarks','gender','id','drinking','biopsyDate']]
    # 將DataFrame存成CSV
    df.to_csv('output.csv', index=False)
    print("download_csv:",df)
    return send_file('output.csv', as_attachment=True)
    # 下載CSV檔案
    #return send_file('output.csv', as_attachment=True)


@app.route('/search', methods=['POST'])
def search():
    filters = {}

    query_name = request.form.get('query_name')
    if len(query_name)>0:
        filters["name"]= query_name

    query_gender = request.form.get('query_gender')
    if len(query_gender)>0:
        filters["gender"]= query_gender

    print("!!!!!!!!!filters:", filters)
    results = get_patients_by_filters(filters)
    return render_template('show_patients.html', patients=results)

 

@app.route('/edit_patient/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    print("request.method:",request.method )
    print("_id:",patient_id)
    patient = get_one_patient(patient_id)
    
    if request.method == 'POST':
        # 假設你從表單中取得資料並更新 user 的 name 和 gender
        patient_str_id = request.form['patient_str_id']
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        drinking = request.form['drinking']
        remarks = request.form['remarks']
        biopsyDate = request.form['biopsyDate']
        biopsyDate = datetime.strptime(biopsyDate, '%Y-%m-%d').date()  # 假設日期格式為 'YYYY-MM-DD'
        print("name:",name)
        print("age:",age)
        print("gender:",gender)
        print("drinking:",drinking)
        print("remarks:",remarks)
        print("biopsyDate:",biopsyDate)
        update_patient_name(patient_id, patient_str_id,name,age,gender,drinking,remarks,biopsyDate)
        #db.session.commit() 
        return redirect(url_for('get_patient_action'))
    else:
        patient.biopsyDate = patient.biopsyDate.strftime('%Y-%m-%d')
    
    return render_template('edit_patient.html', patient=patient)


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    print("upload_file function:",filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename,as_attachment=False)



@app.route('/show_patient_pdf/<int:patient_id>', methods=['GET'])
def show_patient_pdf(patient_id):
    print("pdf preview function:",patient_id)
    patient = get_one_patient(patient_id)
    print("patient.patient_id:",patient.patient_id)
    filename = str(patient.patient_id) +'_chartID.pdf'
    return render_template('pdf_preview.html',filename=filename)



from flask import Flask, render_template, request, redirect, url_for, session, flash
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        passowrd = str(password)
        
        # 檢查使用者名稱和密碼

        if is_user_validate(username,password):
            session['user_level'] = 2
            session['username'] = username  # 將使用者名稱儲存在 session 中

            tmp = is_user_validate_editor(username,password)
            if tmp:
                session['user_level'] = 1
                
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

#upload csv 
UPLOAD_CSV = 'csv'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_CSV'] = UPLOAD_CSV

@app.route('/upload_csv')
def upload_csv():

    return render_template('upload_csv.html')

@app.route('/upload_csv_action', methods=['POST'])
def upload_file():
    # if 'file' not in request.files:
    #     return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_CSV'], filename))
        parse_extend_data(os.path.join(app.config['UPLOAD_CSV'], filename))
        return f"File {filename} uploaded successfully!"
    return "Invalid file type"

def parse_extend_data(filename):
    df = pd.read_csv(filename)
    df=df[["patient_id","height","weight"]]

    for index, row in df.iterrows():
        patient_id = int(row['patient_id'])
        height = int(row['height'])
        weight = int(row['weight'])
        add_patient_extend_data(patient_id,height,weight)
       
@app.route("/patient_extend_data_list", methods=['GET'])
def get_extend_data_action():
     patient_extend_data = get_patient_extend_data()
     return render_template('show_patient_extend_data.html', patient_extend_data=patient_extend_data)

if __name__ == "__main__":
    app.run(debug=False)