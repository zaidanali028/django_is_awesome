from django.contrib import admin
from .models import Room,Topic,Message,User
# Register your models here.



# so that it can be seen in admin panel
admin.site.register(Topic) 
admin.site.register(Room) 
admin.site.register(Message) 
admin.site.register(User) 
# 