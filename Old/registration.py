from flask import Flask
application = Flask(__name__)

@application.route('/registration')
def registration_func():
 return render_template('registration.html')

@application.route("/registration", methods=['POST'])
def ml_predict_func():
    if request.method == 'POST':
        input_dic = {}

        input_dic['Email'] = request.form.get('Email')
        input_dic['Password'] = request.form.get('Password')


        return 'Hello ' + str(input_dic)
    return 'default value'