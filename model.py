from sqlalchemy import create_engine

# 建立資料庫連線引擎，這裡使用 SQLite 資料庫
engine = create_engine('sqlite:///example.db', echo=True)

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

from sqlalchemy.orm import sessionmaker

# 建立一個基礎類別，用來所有模型繼承
Base = declarative_base()

# 定義一個表格模型
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    level = Column(Integer)  #1:編輯者 2:瀏覽者

    def __repr__(self):
        return f"<User(email={self.email}, password={self.password},level={self.level})>"


# 將所有定義的模型表格建立到資料庫中
def create_db():
    Base.metadata.create_all(engine)

def add_user(email, password,level):

    # 建立一個 Session 類
    Session = sessionmaker(bind=engine)

    # 建立一個 session
    session = Session()

    # 建立一個新使用者
    new_user = User(email=email, password=password,level=level)

    # 新增使用者到 session
    session.add(new_user)

    # 提交交易
    session.commit()
    session.close()

def get_user():
    # 查詢所有使用者
    Session = sessionmaker(bind=engine)
    session = Session()
    users = session.query(User).all()

    # 顯示查詢結果
    user_dic = {}
    for user in users:
        user_dic[user.email] = user.password
    return user_dic


def is_user_validate(username,password):
    user_dic = get_user()
    print(username,type(username))
    print(password,type(password))
    print(user_dic)

    if username in user_dic:
        if user_dic[username] == password:
            return True
        
    return False

def get_user_editor():
    # 查詢所有使用者
    Session = sessionmaker(bind=engine)
    session = Session()
    users = session.query(User).filter(User.level == 1).all()
    print ("get_user_editor",users)
    # 顯示查詢結果
    user_dic = {}
    for user in users:
        user_dic[user.email] = user.password
    return user_dic

def is_user_validate_editor(username,password):
    user_dic = get_user_editor()
    print("is_user_validate_editor:",username,type(username))
    print("is_user_validate_editor:",password,type(password))
    print("is_user_validate_editor:",user_dic)
    
    if username in user_dic:
        if user_dic[username] == password:
            return True
        
    return False

# 定義一個表格模型
class Patient(Base):
    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True)
    patient_str_id = Column(String)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)
    drinking = Column(String)
    remarks = Column(String)
    biopsyDate = Column(Date)

    def __repr__(self):
        return f"<Patient(name={self.name}, patient_str_id={self.patient_str_id},gender={self.gender},age={self.age},drinking={self.drinking}, remarks={self.remarks})>,biopsyDate={self.biopsyDate}"
    
 
def add_patient_toDB(name,patient_str_id,gender,age,drinking,remarks,biopsyDate):

    # 建立一個 Session 類
    Session = sessionmaker(bind=engine)

    # 建立一個 session
    session = Session()

    # 建立一個新使用者
    new_patient = Patient(name=name, patient_str_id=patient_str_id, gender=gender,age=age,drinking=drinking,remarks=remarks,biopsyDate=biopsyDate)

    # 新增使用者到 session
    session.add(new_patient)

    # 提交交易
    session.commit()
    session.close()


def update_patient_name(patient_id, new_patient_str_id, new_name, new_age,new_gender, new_drinking,new_remarks,new_biopsyDate):
# 建立一個 Session 類
    Session = sessionmaker(bind=engine)
    # 建立一個 session
    session = Session()

    # 查詢指定 ID 的病人
    patient = session.query(Patient).get(patient_id)


    if patient:
        # 更新病人的姓名
        patient.patient_str_id = new_patient_str_id
        patient.name = new_name
        patient.age = new_age
        patient.gender = new_gender
        patient.drinking = new_drinking
        patient.remarks = new_remarks
        patient.biopsyDate = new_biopsyDate

        # 提交交易
        session.commit()
        print(f"病人 {patient_id} 資料已更新")
      

    else:
        print(f"未找到 ID 為 {patient_id} 的病人")

    # 關閉 session
    session.close()


def get_patient():
    # 查詢所有使用者
    Session = sessionmaker(bind=engine)
    session = Session()
    patients = session.query(Patient).all()
    return patients

    # 顯示查詢結果
    # patient_list_show = []
    # for patient in patients:
    #     patient_list_show.append(patient.name+'_'+str(patient.age)+'_'+patient.gender)
    # return patient_list_show

def get_patients_by_filters(filters):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # 開始構建查詢
    query = session.query(Patient)
    
    # 如果filters不為空，則添加過濾條件
    if filters:
        for key, value in filters.items():
            if value:  # 確保值不為None或空
                if key == 'name':
                    query = query.filter(Patient.name.contains(value))
                elif key == 'gender':
                    query = query.filter(Patient.gender == value)
                # 可以根據需要添加更多欄位的過濾條件

    patients = query.all()  # 執行查詢
    session.close()  # 關閉session以釋放資源
    return patients
    

def get_one_patient(patient_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    print("get_one_patient:",patient_id)
    patient = session.query(Patient).get(patient_id)
    print("get_one_patient:",patient)
    return patient

class PatientExtendData(Base):
    __tablename__ = 'PatientExtendData'

    patient_id = Column(Integer, primary_key=True)
    height = Column(Integer)
    weight = Column(Integer)
    def __repr__(self):
        return f"<PatientExtendData(patient_id={self.patient_id}, height={self.height}, weight={self.weight})>"



def add_patient_extend_data(patient_id, height, weight):
    # 建立一個 Session 類
    Session = sessionmaker(bind=engine)

    # 建立一個 session
    session = Session()

    # 查詢是否已存在相同的 patient_id
    existing_user = session.query(PatientExtendData).filter_by(patient_id=patient_id).first()

    if existing_user:
        # 如果存在，更新現有記錄
        existing_user.height = height
        existing_user.weight = weight
    else:
        # 如果不存在，建立一個新使用者
        new_user = PatientExtendData(patient_id=patient_id, height=height, weight=weight)
        session.add(new_user)

    # 提交交易
    session.commit()
    session.close()


def get_patient_extend_data():
    Session = sessionmaker(bind=engine)
    session = Session()
    patients = session.query(PatientExtendData).all()
    return patients


create_db()  
# add_user('nate', '20')
# get_user()