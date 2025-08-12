from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
#ORM (Object-Relational Mapping) başlatıyorum.

class UserInfo(Base):
    __tablename__ = 'users_info' #mySQL içerisindeki table ismim
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    sifre = Column(String(255), nullable=False)
    isim = Column(String(255))
    soyisim = Column(String(255))
    role = Column("user_role", String(50))

class UserRepository:
    def __init__(self):
        self.engine = create_engine(
            "mysql+pymysql://root:12345678@localhost:3306/mydb?charset=utf8mb4",
            echo=False
        )
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_user_by_email(self, email):
        return self.session.query(UserInfo).filter_by(email=email).first()

    def validate_user_credentials(self, email, password):
        user = self.get_user_by_email(email)
        if user and user.sifre == password:
            return {
                "email": user.email,
                "role": user.role,
                "name": user.isim
            }
        return None