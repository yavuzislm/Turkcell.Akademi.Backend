from sqlalchemy import create_engine, Column, Integer, String, or_
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
# ORM (Object-Relational Mapping) başlatıyorum.

class UserInfo(Base):
    __tablename__ = 'users_info'  # mySQL içerisindeki table ismimi giriyorum.
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    sifre = Column(String(255), nullable=False)
    isim = Column(String(255))
    soyisim = Column(String(255))
    role = Column("user_role", String(50))  # DB kolonu user_role

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

# --- Ders tablosu modeli ---
class lectureDetails(Base):
    __tablename__ = 'courses'
    courseskt = Column(Integer, primary_key=True)        # PK
    idOfCourses = Column(String(15), nullable=False, unique=True)  # örn: CEN121
    nameOfCourse = Column(String(255), nullable=False)            # örn: Calculus I
    description = Column(String(500), nullable=False)             # açıklama

# --- Ders repository (ayrı sınıf) ---
class LectureRepository:
    def __init__(self):
        self.engine = create_engine(
            "mysql+pymysql://root:12345678@localhost:3306/mydb?charset=utf8mb4",
            echo=False
        )
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def find_course(self, term: str):
        q = self.session.query(lectureDetails).filter(
            or_(
                lectureDetails.idOfCourses == term,
                lectureDetails.nameOfCourse.ilike(f"%{term}%")
            ))
        """""
        SELECT *
        FROM courses
        WHERE idOfCourses = :term
        OR nameOfCourse LIKE CONCAT('%', :term, '%')
        LIMIT 1; Aslında yazdığım kod ile buradaki gibi sql'de oluşacak bir if koşulu oluşturuyomuşum.
        Bu sayede dönüş olarak MySQL'den dönen ilk değer dönüyor.
        ilike komutu ile büyük küçük harf önemsiz oluyor.
        % -> işareti ise sql tablosunda herhangi bir yerde olabilir demek.
        """""
        return q.first()

    def find_nameOfCourse(self, term: str):
        q = self.session.query(lectureDetails).filter(
            or_(
                lectureDetails.idOfCourses == term,
                lectureDetails.nameOfCourse.ilike(f"%{term}%")
            ))
        """""
        SELECT *
        FROM courses
        WHERE idOfCourses = :term
        OR nameOfCourse LIKE CONCAT('%', :term, '%')
        LIMIT 1; Aslında yazdığım kod ile buradaki gibi sql'de oluşacak bir if koşulu oluşturuyomuşum.
        Bu sayede dönüş olarak MySQL'den dönen ilk değer dönüyor.
        ilike komutu ile büyük küçük harf önemsiz oluyor.
        % -> işareti ise sql tablosunda herhangi bir yerde olabilir demek.
        """""
        return q.first()
