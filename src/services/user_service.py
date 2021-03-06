from werkzeug.security import check_password_hash
from flask import session, abort, request
import secrets
from entities.user import User
from repositories.user_repository import (
    user_repository as default_user_repository)

class UserService:
    def __init__(self, user_repository=default_user_repository):
        self._user_repository = user_repository

    def register_user(self, username, password, role, phone_number, email):
        user = User(username=username,
                    password=password,
                    role=role,
                    phone_number=phone_number,
                    email=email)
        if not self.check_if_username_exists(username):
            self._user_repository.register_user(user)
            self.login_user(username, password)
            return True
        return False

    def login_user(self, username, password):
        user = self._user_repository.login(username)
        if not user:
            return False
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role
            session["csrf_token"] = secrets.token_hex(16)
            return True
        return False

    def check_if_username_exists(self, username):
        return bool(self._user_repository.check_if_username_exists(username))

    def modify_username(self, new_username, id):
        user = self.get_current_user(id)
        user.username = new_username
        if not self.check_if_username_exists(user.username):
            return self._user_repository.modify_user(user)
        return False

    def modify_email(self, new_email, id):
        user = self.get_current_user(id)
        user.email = new_email
        return self._user_repository.modify_user(user)

    def modify_phone_number(self, new_phone_number, id):
        user = self.get_current_user(id)
        user.phone_number = new_phone_number
        return self._user_repository.modify_user(user)

    def get_current_user(self, id):
        return self._user_repository.get_current_user(id)

    def get_current_username(self, id):
        return self._user_repository.get_current_user(id).username

    def get_current_email(self, id):
        return self._user_repository.get_current_user(id).email

    def get_current_phone_number(self, id):
        return self._user_repository.get_current_user(id).phone_number

    def get_current_role(self, id):
        return self._user_repository.get_current_user(id).role

    def logout(self):
        del session["user_id"]
        del session["username"]
        del session["role"]
        del session['csrf_token']

    def check_csrf(self):
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

    def user_role(self):
        return session.get("role", 0)

    def require_role(self, role):
        if role > session.get("role", 0):
            abort(403)

    def get_user_id(self):
        return session.get("user_id", 0)

user_service = UserService()
