from __future__ import unicode_literals

from django.db import models

class UserManager(models.Manager):
    def create_user(self, email, username, first_name, last_name, password):
        self.create(email=email, username=username, first_name=first_name, last_name=last_name, password=password)

    def compare_passwords(self, user, password):
        if user.password == password:
            return True
        else:
            return False

    def validate_register(self, data):
        password = data['password']
        errors = []
        if len(data['email'])<=1:
            errors.append('* email cannot be blank')
        if len(data['username'])<=1:
            errors.append('* username cannot be blank')
        if len(data['first_name'])<1:
            errors.append('* first name cannot be left empty')
        if len(data['last_name'])<1:
            errors.append('* last name cannot be left empty')
        if len(password)<=7:
            errors.append('* password must contain at least eight characters')
        if password != data['confirm_password']:
            errors.append('* passwords do not match')
        if self.filter(email=data['email']).exists():
            errors.append('* email already exists in database')
        if errors:
            return (False, errors)
        else:
            user = self.create_user(data['email'], data['username'], data['first_name'], data['last_name'], data['password'])
            return (True, user)

    def validate_login(self, data):
        password = data['password']
        errors = []
        if len(data['email'])<1:
            errors.append('* please include an email in order to log in')
        if len(password)<1:
            errors.append('* please input your password in order to log in')
        if errors:
            return (False, errors)
        try:
            user = self.get(email=data['email'])
            if self.compare_passwords(user, password):
                return (True, user)
            else:
                errors.append("* password does not match account")
                return(False, errors)
        except:
            errors.append('* account does not yet exist')
            return (False, errors)

    def update_information(self, data, id):
        user = self.filter(id=id)
        if data['username']:
            user.update(username=data['username'])
        if data['first_name']:
            user.update(first_name=data['first_name'])
        if data['last_name']:
            user.update(last_name=data['last_name'])
        if data['email']:
            user.update(email=data['email'])
        if data['password']:
            user.update(password=data['password'])
        return True

    def destroy_user(self, user_id):
        user_id = int(user_id)
        user = User.objects.get(id=user_id)
        user.delete()
        return True

class User(models.Model):
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=125)
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
