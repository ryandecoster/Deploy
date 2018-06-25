from __future__ import unicode_literals
from django.db import models
import bcrypt
from django.db.models import Count

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if not postData['first_name'].isalpha():
            errors['first_name'] = 'First name contains non-alpha characters.'
        if len(postData['first_name']) < 3:
            errors['first_name'] = 'First name should be at least 3 characters.'
        if len(postData['last_name']) < 3:
            errors['last_name'] = 'Last name should be at least 3 characters.'
        if not postData['last_name'].isalpha():
            errors['last_name'] = 'Last name contains non-alpha characters.'
        if len(postData['username']) < 3:
            errors['email'] = 'Username should be at least 3 characters.'
        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters.'
        if postData['password'] != postData['confirm']:
            errors['password'] = 'Passwords do not match.'
        if User.objects.filter(username = postData['username']):
            errors['email'] = 'Username already exists.'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now= True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = UserManager()

    def __repr__(self):
        return "<User: {}|{} {} {} {}>".format(self.id, self.first_name, self.last_name, self.username, self.password)

class ItemManager(models.Manager):
    def process_addItem(self, postData):
        this_user = User.objects.get(id = postData['user_id'])
        uploaded_items = Item.objects.create(item=postData['item'], uploader = this_user)
        return uploaded_items

    def process_wish(self, postData):
        this_user = User.objects.get(id = postData['user_id'])
        this_item = Item.objects.get(id = postData['item_id'])
        liked_users = this_item.liked_users.add(this_user)
        return liked_users

    def show_wish(self, postData):
        this_item = Item.objects.get(id = postData['item_id'])
        liked_users = this_item.liked_users.all()
        return liked_users

    def addItemValidation(self, postData):
        errors = {}
        if postData['item'] == '':
            errors['item'] = 'No empty entries!'
            return errors
        if len(postData['item']) < 3:
            errors['item'] = 'Item name should be at least 3 characters.'
        return errors

class Item(models.Model):
    item = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now= True)
    updated_at = models.DateTimeField(auto_now= True)
    uploader = models.ForeignKey(User, related_name='uploaded_items')
    liked_users = models.ManyToManyField(User, related_name='liked_items')
    objects = ItemManager()
    def __repr__(self):
        return "<Secret: {}|{}>".format(self.id, self.item)



