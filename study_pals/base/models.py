from django.db import models
# from django.contrib.auth.models import User
from  django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    #1. uncomment this, mpass
    # 2. add AUTH_USER_MODEL='app_name.User' to settings.py
    # 2. run make_migrations  
    #3. run  migrate
    # 4. create super user after migration
    # 5 .comment step1. and add the new fields you want , and repeat 2 and 3
    # 6. dont forget to add the user model to admin.py

    # # firstly pass, create the tables and then modify later
    name=models.CharField(max_length=200, null=True)
    email=models.EmailField(unique=True,null=True)
    bio=models.TextField(null=True)
    avatar=models.ImageField(null=True, default="avatar.svg")
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=[]
    # inherit from django's default user model but now,i can add fields and modify things from here




# Create your models here.


class Topic(models.Model):
    name=models.CharField(max_length=200)


    def __str__(self) :
        return self.name
    

class Room(models.Model):
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    participants=models.ManyToManyField(User,related_name='participants',blank=True)
    name=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-updated_at','created_at']


    def __str__(self) :
        return self.name
    # string representation of this model(probably used by the django admin dashboard)


    


# kkk
class Message(models.Model):
    # 1-> many relationship(btwn user and message)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
   
    # 1-> many relationship(btwn room and message)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    body=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-updated_at','created_at']

    def __str__(self) :
        return self.body[0:50]+'....'