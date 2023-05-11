from django.shortcuts import render, get_object_or_404
from django.urls import reverse

# Create your views here.
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse, HttpResponseRedirect

# from django.contrib.auth.forms import UserCreationForm
from .models import User, Message
from django.db.models import Q
import json


def get_users(user):
    user_list = (
        User.objects.filter(Q(selling__buyer=user) | Q(buying__seller=user))
        .exclude(id=user.id)
        .distinct()
    )
    return user_list


@login_required
def homepage(request):
    # users = User.objects.filter(selling__buyer=request.user)
    first_user_pk = get_users(request.user).first().id
    return HttpResponseRedirect(reverse("chat:chatroom", args=(first_user_pk,)))


@login_required
def chatroom(request, pk: int):
    user = request.user
    user_list = get_users(user)
    other_user = get_object_or_404(User, pk=pk)
    messages = Message.objects.filter(Q(receiver=user, sender=other_user))
    messages.update(seen=True)
    messages = messages | Message.objects.filter(Q(receiver=other_user, sender=user))
    return render(
        request,
        "chat/chatroom1.html",
        {
            "other_user": other_user,
            "users": user_list,
            "user_messages": messages,
        },
    )


@login_required
def ajax_load_messages(request, pk):
    other_user = get_object_or_404(User, pk=pk)
    messages = Message.objects.filter(seen=False, receiver=request.user)

    print("messages")
    message_list = [
        {
            "sender": message.sender.email,
            "message": message.message,
            "sent": message.sender == request.user,
            "picture": other_user.avatar.url,
            "date_created": naturaltime(message.date_created),
        }
        for message in messages
    ]
    messages.update(seen=True)

    if request.method == "POST":
        message = json.loads(request.body)["message"]

        m = Message.objects.create(
            receiver=other_user, sender=request.user, message=message
        )
        message_list.append(
            {
                "sender": request.user.email,
                "username": request.user.email,
                "message": m.message,
                "date_created": naturaltime(m.date_created),
                "picture": request.user.avatar.url,
                "sent": True,
            }
        )
    print(message_list)
    return JsonResponse(message_list, safe=False)
