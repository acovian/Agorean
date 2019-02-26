from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from ..user_app.models import User
from django.db.models import Count
from .models import Message, Like, Comment

def index(request):
    context = {
        'users' : User.objects.all(),
        'posts' : Message.objects.all().order_by('-created_at')
    }
    return render(request, 'message_app/index.html', context)

def newmessage(request):
    thing = request.session['user']
    user_id = thing['id']
    Message.objects.validate(request.POST['message'], user_id)
    return redirect(request.META.get('HTTP_REFERER'))

def delete(request, message_id):
    valid = Message.objects.destroy_message(message_id)
    return redirect(reverse('message_app:index'))

def like(request, message_id):
    thing = request.session['user']
    user_id = thing['id']
    Like.objects.validate_like(user_id, message_id)
    return redirect(request.META.get('HTTP_REFERER'))

def comment(request, id):
    thing = request.session['user']
    user_id = thing['id']
    valid, res = Comment.objects.validate_comment(request.POST, user_id, id)
    if not valid:
        for error in res:
            messages.error(request, error)
    return redirect(request.META.get('HTTP_REFERER'))

def popular(request):
    return redirect(reverse('message_app:popularpage'))

def popularpage(request):
    context = {
        'posts' : Message.objects.annotate(thing=Count('messagelikes')).order_by('-thing')
    }
    return render(request, 'message_app/popular.html', context)

def about(request):
    return render(request, 'message_app/about.html')
