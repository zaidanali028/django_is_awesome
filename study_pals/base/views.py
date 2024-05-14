from django.shortcuts import render,redirect
from django.db.models import Q
from .models import Room,Topic,Message,User
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import RoomForm,UserForm

from django.http import HttpResponse
# Create your views here.


def registration_page(request):
    page='register'

    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            # commit=False is required so that the user object can be used as soon as its created
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home_route')
        else:
            messages.error(request,'An error occured during registration')
    context={'form':form,'page':page}
    return render(request,'base/forms/login_register.html',context)
def login_page(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home_route')
 

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            err_msg=User.objects.all()
            return HttpResponse(err_msg)

        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home_route')
        else:
            messages.error(request,'User/Password does not exist')


    context={'page':page}
    return render(request,'base/forms/login_register.html',context)

def logout_user(request):
    logout(request)
    return redirect('home_route')
def home(request):
    query_data=request.GET.get('q') if request.GET.get('q') != None else ''
    topics=Topic.objects.all()[0:5]
    rooms=Room.objects.filter(
        
        Q(topic__name__icontains=query_data) |
          Q(name__icontains=query_data)| 
          Q(description__icontains=query_data) 
    )
    room_count=rooms.count()
    room_messages=Message.objects.filter(
        Q(room__name__icontains=query_data) |
        Q(room__topic__name__icontains=query_data) 
        # meaning look into the messages model and get all the messages whose room's topic's name mactches query

    )

    # get all rooms whose topic's name is q . icotains -> meaning it maches at least a specific part of the query_data

    context ={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return  render(request, 'base/home.html',context)

def user_profile(request,pk):
    try:
        user=User.objects.get(id=pk)

    except:
        err_msg='User does not exist'
        return HttpResponse(err_msg)
    rooms=user.room_set.all()
    # it uses the host because it uses the User model to create the relation
    topics=Topic.objects.all()
    messages=user.message_set.all()

    context={'user':user,'rooms':rooms,'room_messages':messages,'topics':topics}
    return render(request,'base/user/profile.html',context)
    
def room(request,pk):
    try:
        room=Room.objects.get(id=pk)

    except:
        err_msg='Room does not exist'
        return HttpResponse(err_msg)

    if(request.method=='POST'):
        body=request.POST.get('body')
        Message.objects.create(
            user=request.user,
            room=room,
            body=body)
        room.participants.add(request.user)
        # add the user who just commented to participants of this toom

        return redirect('room_route',pk=room.id)

      
    messages=room.message_set.all().order_by('-created_at')
    # messag_set (meaning get the room's messages(1->many relationship))

    participants=room.participants.all()
    # get all participants in a specific room

    context ={'room':room,'room_messages':messages,'participants':participants}
    return  render(request, 'base/room.html',context)

@login_required(login_url='login_route')    
def create_room(request):
    form=RoomForm()
    topics=Topic.objects.all()
    context ={'form':form,'topics':topics}
    if(request.method=='POST'):
        print(request.POST)

        form=RoomForm(request.POST)
        if(form.is_valid()):
            room=form.save(commit=False)
            # inorder to get an instance of the saved data
            room.host=request.user
            room.save()

            return redirect('home_route')

    return render(request,'base/forms/room_form.html',context)


@login_required(login_url='login_route')    
def edit_room(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    if request.user!=room.host:
        return HttpResponse('You are not allowed here')
    # 
    if(request.method=='POST'):
        form=RoomForm(request.POST,instance=room)
        if(form.is_valid()):
            form.save()
            return redirect('home_route')

    
    context={'form':form,'room':room}
    
    return render(request,'base/forms/eidt_room_form.html',context)


@login_required(login_url='login_route')    
def delete_room(request,pk):
    try:
        room=Room.objects.get(id=pk)
        if request.user!=room.host:
            return HttpResponse('You are not allowed here')
        if(request.method=='POST'):
            room.delete()
            return redirect('home_route')
    except:
        err_msg='Room does not exist'
        return HttpResponse(err_msg)

    context={'obj':room}
    return render(request,'base/forms/delete_forms.html',context)



@login_required(login_url='login_route')    
def delete_message(request,pk):
    page='delete_message'
    try:
        message=Message.objects.get(id=pk)
        if request.user!=message.user:
            return HttpResponse('You are not allowed here')
        if(request.method=='POST'):
            message.delete()
            return redirect('home_route',)

    except:
        err_msg='Message does not exist'
        return HttpResponse(err_msg)

    context={'obj':message,'page':page}
    return render(request,'base/forms/delete_forms.html',context)

@login_required(login_url='login_route')   
def edit_user(request):
    user=request.user
    form = UserForm(instance=user)
    if request.method=='POST':
            form = UserForm(request.POST,request.FILES ,instance=user)
            if form.is_valid():
                form.save()
                return redirect('user_profile_route',pk=user.id)
            else:
                print(form)

        

    context={'form':form}
    return render(request,'base/forms/edit_user_form.html',context)


def browse_topics(request):
    query_data=request.GET.get('q') if request.GET.get('q') != None else ''

    
    topics=Topic.objects.filter(
        Q(name__icontains=query_data) |
        Q(room__name__icontains=query_data) 

    )
    context={'topics':topics}
    return render(request,'base/topics.html',context)


def recent_activities(request):
    messages=Message.objects.all()
    context={'all_messages':messages}
    return render(request,'base/recent_activities.html',context)
