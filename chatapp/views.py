from django.contrib.auth.decorators import login_required
from account.models import Account
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from .models import Message,Chat
from django.http import HttpResponse

def index(request):
	if not request.user.is_authenticated:
		return redirect('login')
	convos = Chat.objects.filter(creator=request.user).exclude(last_message='') or Chat.objects.filter(receiver=request.user).exclude(last_message='')
	context = {
		'convos' : convos
	}
	return render(request, 'indexchat.html', context)
@login_required
def room(request, room_name):
	if Account.objects.filter(username=room_name).first():
		if not Account.objects.filter(username=room_name).first() == request.user:
			receiver = Account.objects.get(username=room_name)
			if not (Chat.objects.filter(creator=request.user,receiver=receiver).first() or Chat.objects.filter(creator=receiver,receiver=request.user).first()):
				instance = Chat.objects.create(chat_id=request.user.username + receiver.username,creator=request.user,receiver=receiver)
				lol = Chat.objects.filter(creator=request.user,receiver=receiver).first()
			else:
				if Chat.objects.filter(creator=request.user,receiver=receiver).first():
					lol = Chat.objects.filter(creator=request.user,receiver=receiver).first()
				elif Chat.objects.filter(creator=receiver,receiver=request.user).first():
					lol = Chat.objects.filter(creator=receiver,receiver=request.user).first()
			return render(request, 'room.html', {
				'room_name_json': mark_safe(json.dumps(room_name)),
				'username':  mark_safe(json.dumps(request.user.username)),
				'receiver': Account.objects.filter(username=room_name).first(),
				'chat': lol.chat_id,
			})
		else:
			return HttpResponse("<center><h2>You can't start a conversation with yourself</h2></center>")
	else:
		return HttpResponse('<center><h2>No user with that name</h2></center>')