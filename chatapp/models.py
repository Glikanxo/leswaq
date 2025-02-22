from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Chat(models.Model):
	chat_id = models.CharField(default='',max_length=256,unique=True)
	creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
	creator_status = models.IntegerField(default=0)
	receiver_status = models.IntegerField(default=0)
	creator_seen = models.BooleanField(default=1)
	receiver_seen = models.BooleanField(default=1)
	last_message = models.CharField(default='',max_length=256)
	last_message_time = models.DateTimeField(auto_now_add=False,null=True)
	class Meta:
		ordering=['-last_message_time']
	def __str__(self):
		return self.chat_id

class Message(models.Model):
	chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
	author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.author.username

	def last_10_messages(chatsid):
		ch = Chat.objects.filter(chat_id=chatsid).first()
		return Message.objects.order_by('timestamp').filter(chat=ch)[:30]