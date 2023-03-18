from django.shortcuts import render,redirect
from .models import Room,Message,Topic,User
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from .forms import RoomForm,UserForm,MyUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout

# Create your views here.






##################################################################################################
def home(request):
    q=request.GET.get('q') if request.GET.get("q") != None else ""
    topics=Topic.objects.all()[0:6]
    rooms=Room.objects.filter(
        Q(name__icontains=q)|
        Q(topic__name__icontains=q)|
        Q(description__icontains=q)|
        Q(host__username__icontains=q)
    )
    all_messages=Message.objects.filter(
        Q(room__topic__name__icontains=q)|
        Q(room__name__icontains=q)|
        Q(user__username__icontains=q)
    )
   
    room_count=Room.objects.count()
    context={'rooms':rooms,'topics':topics,'room_count':room_count,'all_messages':all_messages}
    return render(request,'base/home.html',context)
##################################################################################################

















##################################################################################################
def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by("-created")
    participants=room.participants.all()
    if request.method=="POST":
        message=Message.objects.create(
            user=request.user,body=request.POST.get("body"),
            room=room

        )
        room.participants.add(request.user)
        return redirect('room',message.room.id)

    context={'room':room,"room_messages":room_messages,'participants' :participants}
    return render(request,'base/room.html',context)
##################################################################################################
























##################################################################################################
@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)
##################################################################################################












##################################################################################################
@login_required(login_url="login")
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)
##################################################################################################




##################################################################################################
@login_required(login_url="login")
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user!=room.host and request.user.is_superuser==False:
        return HttpResponse("This is not your room. <a href='/'>Go back</a>")
    if request.method=="POST":
        room.delete()
        return redirect("home")
    
    context={'obj':room}
    return render(request,'base/delete.html',context)
##################################################################################################



##################################################################################################
@login_required(login_url="login")
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    if request.user!=message.user and request.user.is_superuser==False:
        return HttpResponse("This is not your room. <a href='/'>Go back</a>")
    if request.method=="POST":
        message.delete()
        return redirect("room",message.room.id)
    
    context={'obj':message}
    return render(request,'base/delete.html',context)
##################################################################################################










##################################################################################################
def loginPage(request):
    page="Login"
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method=="POST":
        email=request.POST.get("email").lower()
        password=request.POST.get("password")

        try:
            user=User.objects.get(email=email)
        except:
            messages.error(request,"Incorrect username or password")
            
        user= authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            messages.error(request,"Incorrect username or password")
            return redirect("login")
        
    context={'page':page}
    return render(request,'base/login_register.html',context)
##################################################################################################


##################################################################################################
def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("home")
    else:
        return redirect('home')
##################################################################################################



##################################################################################################
def registerPage(request):
    form=MyUserCreationForm
    page="register"
    if request.method=="POST":
        form=MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect("home")
        else:
            messages.error(request,"Couldn't create account. Try Again.")
    context={"form":form,'page':page}
    return render(request,'base/login_register.html',context)
##################################################################################################








##################################################################################################
def profilePage(request,pk):
    user=User.objects.get(id=pk)
    topics=Topic.objects.all()[0:6]
    rooms=Room.objects.filter(
        Q(host=user)
        )       
    all_messages=user.message_set.all().order_by("-created")
    room_count=Room.objects.count()
    context={'room_count':room_count,'user':user,"topics":topics,"rooms":rooms,"all_messages":all_messages}
    return render(request,'base/profile.html',context)
##################################################################################################



##################################################################################################
def updateUser(request):
    user=request.user
    form = UserForm(instance=user)
    if request.method=="POST":
        form=UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect("user-profile",pk=user.id)
        else:
            messages.error(request,"ناموفق")
    return render(request,'base/update-user.html',{"form":form})
##################################################################################################




##################################################################################################
def topicsPage(request):
    q=request.GET.get("q") if request.GET.get("q") !=None else ""
    topics=Topic.objects.filter(
        Q(name__icontains=q)
    )
    topic_count=Topic.objects.count()
    return render(request,'base/topics.html',{'topics':topics,'topic_count':topic_count})
##################################################################################################






##################################################################################################
def activitiesPage(request):
    all_messages=Message.objects.filter()
    return render(request,'base/activity.html',{'all_messages':all_messages})
##################################################################################################