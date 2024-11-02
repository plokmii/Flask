from sqlalchemy import create_engine

# 建立資料庫連線引擎，這裡使用 SQLite 資料庫
engine = create_engine('sqlite:///example.db', echo=True)

from sqlalchemy import Column, Integer, String
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

    def __repr__(self):
        return f"<User(email={self.email}, password={self.password})>"

# 將所有定義的模型表格建立到資料庫中
def create_db():
    Base.metadata.create_all(engine)

def add_user(email, password):

    # 建立一個 Session 類
    Session = sessionmaker(bind=engine)

    # 建立一個 session
    session = Session()

    # 建立一個新使用者
    new_user = User(email=email, password=password)

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


# 定義一個表格模型
class Patient(Base):
    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)
    drinking = Column(String)

    def __repr__(self):
        return f"<Patient(name={self.name}, gender={self.gender},age={self.age},drinking={self.drinking})>"
    
 
def add_patient_toDB(name,gender,age,drinking):

    # 建立一個 Session 類
    Session = sessionmaker(bind=engine)

    # 建立一個 session
    session = Session()

    # 建立一個新使用者
    new_patient = Patient(name=name, gender=gender,age=age,drinking=drinking)

    # 新增使用者到 session
    session.add(new_patient)

    # 提交交易
    session.commit()
    session.close()


def update_patient_name(patient_id, new_name, new_gender, new_age,new_drinking):
# 建立一個 Session 類
    Session = sessionmaker(bind=engine)
    # 建立一個 session
    session = Session()

    # 查詢指定 ID 的病人
    patient = session.query(Patient).get(patient_id)


    if patient:
        # 更新病人的姓名
        patient.name = new_name
        patient.gender = new_gender
        patient.age = new_age
        patient.drinking = new_drinking
        
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

def get_one_patient(patient_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    print("get_one_patient:",patient_id)
    patient = session.query(Patient).get(patient_id)
    print("get_one_patient:",patient)
    return patient


create_db()    
# add_user('nate', '20')
# get_user()