import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from dataAccess.dataAccess import UserRepository, LectureRepository

class AuthenticationService:
    def __init__(self):
        self.user_repository = UserRepository()

    def authenticate_user(self, email, password):
        if not email or not password:
            return {"success": False, "message": "Email ve şifre gerekli", "user": None}
        if "@" not in email:
            return {"success": False, "message": "Geçerli bir email adresi girin", "user": None}
        if len(password) < 6:
            return {"success": False, "message": "Şifre en az 6 karakter olmalı", "user": None}

        user = self.user_repository.validate_user_credentials(email, password)
        if user:
            return {
                "success": True,
                "message": "Giriş başarılı!",
                "user": {"email": email, "role": user["role"], "name": user["name"]},
            }
        else:
            return {"success": False, "message": "Geçersiz email veya şifre", "user": None}

    def get_user_info(self, email):
        user = self.user_repository.get_user_by_email(email)
        if user:
            return {"email": email, "role": user["role"], "name": user["name"]}
        return None

    def get_all_students(self):
        return self.user_repository.get_all_students_with_course_status()


class CourseService:
    def __init__(self):
        self.repo = LectureRepository()

    def get_course(self, term: str):
        term = (term or "").strip()
        if not term:
            return None
        row = self.repo.find_course(term)
        if row:
            return {"name": row.nameOfCourse, "description": row.description}
        return None

    def list_courses(self):
        rows = self.repo.list_all_courses()
        data = []
        for r in rows:
            data.append({
                "id": r.id,
                "ders_kodu": r.idOfCourse,
                "ders_ismi": r.nameOfCourse,
                "kredi": r.credit,
                "ders_akts": r.courseskt,
                "ders_status": r.courseStatus,
            })
        return data

    def select_course(self, course_id: str):
        return self.repo.select_course(course_id)

    def unselect_course(self, course_id: str):
        return self.repo.unselect_course(course_id)

    def get_selected_courses(self):
        rows = self.repo.get_selected_courses()
        data = []
        for r in rows:
            data.append({
                "id": r.id,
                "ders_kodu": r.idOfCourse,
                "ders_ismi": r.nameOfCourse,
                "kredi": r.credit,
                "ders_akts": r.courseskt,
                "ders_status": r.courseStatus,
            })
        return data
