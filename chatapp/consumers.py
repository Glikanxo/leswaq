from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
import json
from channels.generic.websocket import WebsocketConsumer
from .models import Message,Chat
from datetime import datetime

User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        messages = Message.last_10_messages(data['chatname'])
        content = {
            'command':'messages',
            'messages' : self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        ch = data['chat']
        chat_obj = Chat.objects.get(chat_id=ch)
        if chat_obj.creator == author_user:
            cr_seen = 1
            rc_seen = 0
            if chat_obj.receiver_status != 0:
                rc_seen = 1
        else:
            cr_seen = 0
            rc_seen = 1
            if chat_obj.creator_status != 0:
                cr_seen = 1
        message = Message.objects.create(
            chat = chat_obj,
            author = author_user,
            content=data['message'],
            )
        
        chat_obj.receiver_seen = rc_seen
        chat_obj.creator_seen = cr_seen
        chat_obj.last_message = data['message']
        chat_obj.last_message_time = datetime.now()
        chat_obj.save()

        content={
            'command': 'new_message',
            'message':self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        if message.chat.creator == User.objects.filter(username=self.scope['user'].username).first():
            seen = message.chat.receiver_seen
        else:
            seen = message.chat.creator_seen
        return {
            'author' : message.author.username,
            'content':  message.content,
            'timestamp': str(message.timestamp),
            'seen':seen
        }

    commands = {
        'fetch_messages':fetch_messages,
        'new_message':new_message
     }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.chat = Chat.objects.get(chat_id=self.room_name)
        self.user = User.objects.filter(username=self.scope['user'].username).first()

        if self.user == self.chat.creator:
            self.chat.creator_status += 1
            self.chat.creator_seen == True
            self.chat.save()
        else:
            self.chat.receiver_status += 1
            self.chat.receiver_seen == True
            self.chat.save()

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group

        if self.user == self.chat.creator:
            print(Chat.objects.get(chat_id=self.room_name))
            chat = Chat.objects.get(chat_id=self.room_name)
            chat.creator_status -= 1
            chat.save()
        else:
            Chat.objects.get(chat_id=self.room_name).receiver_status -= 1
            Chat.objects.get(chat_id=self.room_name).save()

        self.send(text_data=json.dumps({"command":"online",'value':'offline',}))
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))

class ActivityConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']
        self.room_group_name = 'activity'
        user = self.scope["user"]

        if (user.is_authenticated):
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            self.accept()
            self.send_status('online')
            account = User.objects.filter(username=user.username)[0]
            account.is_online += 1
            account.save()

    def disconnect(self, close_code):
        user = self.scope["user"]
        if (user.is_authenticated):
            self.send_status('offline')
            
            account = User.objects.filter(username=user.username)[0]
            account.is_online -= 1
            account.save()
            # Leave room group
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )

    def send_status(self,status):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'status_update',
                'user': self.scope["user"].username,
                'status': status
            }
        )

    def status_update(self, event):
        message = {}
        message['user'] = event['user']
        message['status'] = event['status']
        self.send(text_data=json.dumps(message))
