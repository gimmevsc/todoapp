from django.shortcuts import render, redirect
from todoapp.models import User, ToDoItems
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .utils import *
import threading

def homePage(request):
    return render(request, 'todoapp/index.html', {'title':'TO DO'})

def register(request):
    context = {'title': 'Register', 'errors': {}}
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_name = request.POST['name']
        password_hashed = make_password(password)
        
        try:
            validate_email(email)
        except ValidationError:
            context['errors']['email'] = 'Invalid email address'
        
        if User.objects.filter(email_address=email).exists():
            context['errors']['email'] = 'Email address already exists'
        
        if len(password) < 4:
            context['errors']['password'] = 'Password must be more than 4 characters'
            
        if len(user_name) < 1:
            context['errors']['username'] = 'Field is empty'
        
        if not context['errors']:
        
            user = User.objects.create(username=user_name, email_address=email, password=password_hashed)
            user.save()
    
            return redirect('login')
            
    return render(request, 'todoapp/register.html', context)


def login(request):
    context = {'title': 'Login', 'errors': {}}
    
    if request.method == 'POST':    
        
        email = request.POST['email']
        
        if not User.objects.filter(email_address=email).exists():
            context['errors']['email'] = "Email address doesn't exist"
        
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            request.session['user_id'] = user.user_id
            request.session['email'] = user.email_address
            request.session['is_authenticated'] = True
            return redirect('main')
        else:
            context['errors']['password'] = 'Invalid password'      
        
    return render(request, 'todoapp/login.html', context)



def reset(request):
    
    context = {'title': 'Reset', 'errors' : {}}
        
    if request.method == 'POST':    
        email = request.POST['email']

        if len(email) < 1:
            context['errors']['email'] = "Empty field"
            
        elif not User.objects.filter(email_address=email).exists():
            context['errors']['email'] = "Email address doesn't exist"
            
        else:
            user = User.objects.get(email_address=email)
            
            code = str(generate_code())
                    
            code_sender = threading.Thread(target=send_verification_code, args=(email, code, 'Verify your email address', 'Your verification code is'))
            code_sender.start() 
            
            request.session['reset_email_entered'] = True
            
            user.code = code
            user.save()
            
            response = redirect('confirmreset')
            response.set_cookie('email_address', email, max_age=3600)
            return response
    
    return render(request, 'todoapp/reset.html', context)



def confirmreset(request):
    context = {'title': 'Main', 'errors' : {}}
    
    if not request.session.get('reset_email_entered'):
        return redirect('passreset')
    else:
        if request.method == 'POST': 
            
            entered_code = str(request.POST.get('code'))
            new_password = request.POST.get('password')
            
            if len(new_password) < 4:
                if len(new_password) < 1:
                    context['errors']['password'] = 'Empty field'
                else:
                    context['errors']['password'] = 'Password must be more than 4 characters'
                    
            email = request.COOKIES.get('email_address')
            
            user = User.objects.get(email_address = email)
            
            if entered_code == str(user.code) and not context['errors']:
                user.password = make_password(new_password)
                user.save()
                
                del request.session['reset_email_entered']
                request.session.modified = True
                
                return redirect('login')
            elif entered_code != str(user.code):
                context['errors']['code'] = 'Wrong code'
    
    return render(request, 'todoapp/confirmreset.html', context)


# @login_required
def mainPage(request):

    context = {'title': 'Main', 'errors' : {}, 'items' : {}}
    
    email = request.session.get('email')
        
    if not email:
        return redirect('login')
    
    user = User.objects.get(email_address=email)
    
    items = ToDoItems.objects.filter(user=user)  # Retrieve to-do items for the logged-in user
    
    print(items)
    
    context['items'] = items
    
    return render(request, 'todoapp/main.html', context)



def addToDo(request):
    context = {'title': 'Add ToDo', 'errors': {}}
    
    if request.method == 'POST':
        
        email = request.session.get('email')
        
        user = User.objects.get(email_address=email)
        print(request.body)
        todo_context = request.POST.get('todo')
        
        if len(todo_context) < 1:
            context['errors']['todo'] = 'Field is empty'
        else:
            todo_item = ToDoItems.objects.create(user=user, todo_context=todo_context, is_done=False)
            todo_item.save()
            
            return redirect('main')
    
    return render(request, 'todoapp/main.html', context)


def deleteToDo(request, todo_id):
    
    if request.method == 'POST':
        
        todo = ToDoItems.objects.get(todo_id=todo_id)
        
        todo.delete()
        
        return redirect('main') 


def editToDo(request, todo_id):
    
    if request.method == 'POST':
        
        todo = ToDoItems.objects.get(todo_id=todo_id)
        
        todo.delete()
        
        return redirect('main') 


def doneToDo(request, todo_id):
    
    if request.method == 'POST':
        
        todo = ToDoItems.objects.get(todo_id=todo_id)
        
        todo.is_done = abs(todo.is_done - 1)
        
        todo.save()
        
        return redirect('main')
    

def logout(request):
    
    if request.method == 'POST':
        request.session.flush()
        
        return redirect('login')

def todo_search(request):

    if request.method == 'POST':
        
        search_query = request.POST.get('search', '')
        
        email = request.session.get('email')
        
        user = User.objects.get(email_address=email)
        
        if search_query:
            items = ToDoItems.objects.filter(user=user, todo_context__icontains=search_query)
        else:
            return redirect('main')
    else:
        items = ToDoItems.objects.filter(user=user)
    
    context = {
        'items': items,
    }
    return render(request, 'todoapp/main.html', context)