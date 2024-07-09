from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', )
    list_display_links = ('user_id', )
    
class ToDoItemsAdmin(admin.ModelAdmin):
    list_display = ('todo_id', )
    list_display_links = ('todo_id', )

admin.site.register(User, UserAdmin)
admin.site.register(ToDoItems, ToDoItemsAdmin)