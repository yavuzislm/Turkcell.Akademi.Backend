from flask import Flask, request, jsonify
from flask_cors import CORS

from businessLogic.businessLogic import AuthenticationService

"Presentation Layer -> Business Layer -> Data Access Layer"

app = Flask(__name__)
CORS(app)

# İş mantığı servisini başlat...
auth_service = AuthenticationService()


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'status': 'fail',
                'message': 'JSON verisi gerekli'
            }), 400

        email = data.get('email')
        password = data.get('password')

        print(f"Login attempt for email: {email}")

        result = auth_service.authenticate_user(email, password)

        if result["success"]:
            return jsonify({
                'status': 'success',
                'message': result["message"],
                'user': result["user"]["role"],
                'userInfo': result["user"]
            }), 200
        else:
            return jsonify({
                'status': 'fail',
                'message': result["message"]
            }), 401

    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Sunucu hatası'
        }), 500


@app.route('/user/<email>', methods=['GET'])
def get_user(email):
    try:
        user_info = auth_service.get_user_info(email)

        if user_info:
            return jsonify({
                'status': 'success',
                'message': 'Giriş başarılı!',
                'user': user_info
            }), 200
        else:
            return jsonify({
                'status': 'fail',
                'message': 'Geçersiz bilgiler'
            }), 401

    except Exception as e:
        print(f"Get user error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Sunucu hatası'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)