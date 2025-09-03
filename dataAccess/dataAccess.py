from sqlalchemy import create_engine, Column, Integer, String, or_
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import QueuePool

Base = declarative_base()

class UserInfo(Base):
    __tablename__ = 'users_info'
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
            echo=False,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=3600
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

    def get_all_students_with_course_status(self):
        try:
            students = self.session.query(UserInfo).filter(UserInfo.role == 'student').all()
            
            student_list = []
            for student in students:
                # Her öğrencinin seçtiği ders sayısını hesapla
                selected_courses_count = self.session.query(lectureDetails).filter(
                    lectureDetails.courseStatus == 1
                ).count()
                
                student_data = {
                    "id": student.id,
                    "email": student.email,
                    "isim": student.isim,
                    "soyisim": student.soyisim,
                    "role": student.role,
                    "selected_courses_count": selected_courses_count,
                    "course_status": "Seçti" if selected_courses_count > 0 else "Seçmedi"
                }
                student_list.append(student_data)
            
            return student_list
        except Exception as e:
            print(f"Error in get_all_students_with_course_status: {e}")
            self.session.rollback()
            return []


class lectureDetails(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    idOfCourse = Column(String(15), nullable=False)
    courseskt = Column(Integer)
    nameOfCourse = Column(String(255), nullable=False)
    description = Column(String(500), nullable=False)
    credit = Column(Integer)
    courseStatus = Column(Integer)


class LectureRepository:
    def __init__(self):
        self.engine = create_engine(
            "mysql+pymysql://root:12345678@localhost:3306/mydb?charset=utf8mb4",
            echo=False,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=3600
        )
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def find_course(self, term: str):
        try:
            q = self.session.query(lectureDetails).filter(
                or_(
                    lectureDetails.idOfCourse == term,
                    lectureDetails.nameOfCourse.ilike(f"%{term}%")
                )
            )
            return q.first()
        except Exception as e:
            print(f"Error in find_course: {e}")
            self.session.rollback()
            return None

    def find_nameOfCourse(self, term: str):
        try:
            q = self.session.query(lectureDetails).filter(
                or_(
                    lectureDetails.idOfCourse == term,
                    lectureDetails.nameOfCourse.ilike(f"%{term}%")
                )
            )
            return q.first()
        except Exception as e:
            print(f"Error in find_nameOfCourse: {e}")
            self.session.rollback()
            return None

    def list_all_courses(self):
        try:
            return (
                self.session
                .query(lectureDetails)
                .order_by(lectureDetails.idOfCourse.asc())
                .all()
            )
        except Exception as e:
            print(f"Error in list_all_courses: {e}")
            self.session.rollback()
            return []

    # BURAYI UÇUR
    def select_course(self, course_id: str):
        try:
            course = self.session.query(lectureDetails).filter_by(idOfCourse=course_id).first()
            if course:
                course.courseStatus = 1
                self.session.commit() #session komutu ile değiştirdiğimiz "course.courseStatus = 1" değerini
                #SQL dosyamızda da değiştirmek için bunu yapıyoruz ve bu komut bize
                #UPDATE courses SET courseStatus = 1 WHERE idOfCourse = 'X' komutunu veriyor.
                return True
            return False
        except Exception as e:
            print(f"Error in select_course: {e}")
            self.session.rollback()
            return False

    def unselect_course(self, course_id: str):
        try:
            course = self.session.query(lectureDetails).filter_by(idOfCourse=course_id).first()
            if course:
                course.courseStatus = 0
                self.session.commit()
                return True
            return False
        except Exception as e:
            print(f"Error in unselect_course: {e}")
            self.session.rollback()
            return False

    def get_selected_courses(self):
        try:
            return (
                self.session
                .query(lectureDetails)
                .filter(lectureDetails.courseStatus == 1)
                .order_by(lectureDetails.idOfCourse.asc())
                .all()
            )
        except Exception as e:
            print(f"Error in get_selected_courses: {e}")
            self.session.rollback()
            return []
