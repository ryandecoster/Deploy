from django.shortcuts import render, redirect
from .models import User, UserManager, Item, ItemManager
from django.contrib import messages
import bcrypt

def index(request):

    return render(request, 'wishexam/index.html')

def login(request):
    if User.objects.filter(username = request.POST['username']):
        user = User.objects.get(username=request.POST['username'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            messages.error(request, "Successfully logged in!")
            return redirect('/dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect ('/')
    else:
        messages.error(request, "Invalid username or password.")
        return redirect('/')

def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], username = request.POST['username'], password = hashed)
        request.session['user_id'] = user.id
        request.session['first_name'] = user.first_name
        messages.error(request, "Successfully registered!")
        return redirect('/dashboard')

def dash(request):
    context = {
        'user_list': Item.objects.filter(liked_users__id__contains=request.session['user_id'])|Item.objects.filter(uploader__id__contains=request.session['user_id']),
        'all_users': Item.objects.exclude(uploader__id__contains=request.session['user_id']).exclude(liked_users__id__contains=request.session['user_id']),
        'id': request.session['user_id'],
        'first_name': request.session['first_name'],
    }
    return render(request, 'wishexam/dashboard.html', context)

def show(request, id):
    context = {
        'item': Item.objects.get(id=id),
    }
    return render(request, 'wishexam/show.html', context)

def logout(request):
    request.session.clear()
    messages.error(request, "You have successfully logged out!")
    return redirect('/')

def delete(request):
    this_item = Item.objects.get(id=request.POST['item_id'])
    this_item.delete()
    return redirect('/dashboard')

def remove(request, id):
    user = User.objects.get(id=request.session['user_id'])
    product = Item.objects.get(id=id)
    product.liked_users.remove(user)
    messages.error(request, "You have successfully removed this wish item!")
    return redirect('/dashboard')

def create(request):

    return render(request, 'wishexam/create.html')

def add(request):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        product = Item.objects.get(id=request.POST['item_id'])
        product.liked_users.add(user)
        messages.error(request, "You have successfully added a new item!")
        return redirect('/dashboard')

def create_item(request):
    errors = Item.objects.addItemValidation(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/create')
    else:
        if request.method == "POST":
            liked_users = Item.objects.process_addItem(request.POST)
            messages.error(request, "You have successfully added a new item!")
            return redirect('/dashboard')