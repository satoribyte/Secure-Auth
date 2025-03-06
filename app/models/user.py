import json
import os
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import pyotp

USER_JSON_PATH = 'data/users.json'

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    two_factor_secret = db.Column(db.String(32), nullable=True)
    is_2fa_verified = db.Column(db.Boolean, default=False)

    def __init__(self, username, password_hash=None, is_2fa_verified=False):
        self.username = username
        self.password_hash = password_hash
        self.is_2fa_verified = is_2fa_verified

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_two_factor_secret(self, secret):
        self.two_factor_secret = secret
        self.save_to_json()

    def get_two_factor_secret(self):
        return self.two_factor_secret

    def mark_2fa_verified(self):
        self.is_2fa_verified = True
        db.session.commit()
        self.save_to_json()

    @staticmethod
    def create_user(username, password_hash):
        user = User(username=username, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        user.save_to_json()
        return user

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    def validate_2fa(self, otp):
        if not self.two_factor_secret:
            return False
        totp = pyotp.TOTP(self.two_factor_secret)
        return totp.verify(otp)

    def generate_2fa_secret(self):
        return pyotp.random_base32()

    def save_to_json(self):
        users = self.load_from_json()
        users[self.username] = {
            "username": self.username,
            "password_hash": self.password_hash,
            "two_factor_secret": self.two_factor_secret,
            "is_2fa_verified": self.is_2fa_verified
        }
        with open(USER_JSON_PATH, 'w') as file:
            json.dump(users, file, indent=4)

    @staticmethod
    def load_from_json():
        if not os.path.exists(USER_JSON_PATH):
            return {}
        with open(USER_JSON_PATH, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}