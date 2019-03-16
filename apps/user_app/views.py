from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import User
from ..message_app.models import Message

# Create your views here.
def index(request):
    if "user" not in request.session:
        return render(request, template_name="user_app/index.html")
    else:
        return redirect(reverse("message_app:index"))

def register(request):
    valid, res = User.objects.validate_register(request.POST)
    if valid:
        email = request.POST["email"]
        getbyemail = User.objects.get(email=email)
        request.session["user"] = {
            "id" : getbyemail.id,
            "username": getbyemail.username,
            "first_name": getbyemail.first_name,
            "last_name": getbyemail.last_name,
            "email": getbyemail.email
        }
        return redirect(reverse("message_app:index"))
    else:
        for error in res:
            messages.error(request, error)
        return redirect(reverse("user_app:index"))

def login(request):
    valid, res = User.objects.validate_login(request.POST)
    if valid:
        email = request.POST["email"]
        getbyemail = User.objects.get(email=email)
        request.session["user"] = {
            "id": getbyemail.id,
            "username": getbyemail.username,
            "email": getbyemail.email,
            "first_name": getbyemail.first_name,
            "last_name": getbyemail.last_name,
        }
        return redirect(reverse("message_app:index"))
    else:
        for error in res:
            messages.error(request, error)
        return redirect(reverse("user_app:index"))

def user(request, id):
    user = User.objects.get(id=id)
    # 'posts' : Message.objects.annotate(thing=Count('messagelikes')).order_by('-thing')
    context = {
        "user": user,
        "messages": Message.objects.filter(user=User.objects.get(id=id)).order_by("-created_at")
    }
    return render(request, "user_app/user.html", context)

def settings(request, user_id):
    context = {
        "user": User.objects.get(id=user_id)
    }
    return render(request, "user_app/settings.html", context)

def update_information(request, user_id):
    User.objects.update_information(request.POST, user_id)
    return redirect(reverse("user_app:user", kwargs={"id":user_id}))

def delete(request, user_id):
    User.objects.destroy_user(user_id)
    return redirect(reverse("user_app:logout"))

def logout(request):
    del request.session["user"]
    return redirect(reverse("user_app:index"))
