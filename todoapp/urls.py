from django.urls import path

from .views import *

urlpatterns = [
    path('login', login, name='login'),
    path('', login, name='login'),
    path('register', register, name='register'),
    path('main', mainPage, name='main'),
    path('reset', reset, name='passreset'),
    path('confirmreset', confirmreset, name='confirmreset'),
    path('deleteToDo/<int:todo_id>', deleteToDo, name='deleteToDo'),
    # path('editToDo/<int:todo_id>', editToDo, name='editToDo'),
    path('todo_search', todo_search, name='todo_search'),
    path('doneToDo/<int:todo_id>', doneToDo, name='doneToDo'),
    path('logout', logout, name='logout'),
    path('addToDo', addToDo, name='addToDo')
]
