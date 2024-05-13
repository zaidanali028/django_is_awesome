from django.db import models
from django.contrib.auth.models import User

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