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
    name = Column(String)
    age = Column(Integer)

    def __repr__(self):
        return f"<User(name={self.name}, age={self.age})>"

# 將所有定義的模型表格建立到資料庫中
def create_db():
    Base.metadata.create_all(engine)

def add_user(name, age):

    # 建立一個 Session 類
    Session = sessionmaker(bind=engine)

    # 建立一個 session
    session = Session()

    # 建立一個新使用者
    new_user = User(name=name, age=age)

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
    for user in users:
        print(user)

#create_db()    
#add_user('nate', '20')
get_user()