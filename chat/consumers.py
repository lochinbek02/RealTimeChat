import json
import random
from time import sleep
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from .models import Message
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        for i in range(100):
            await self.send(json.dumps({'message': random.randint(1, 100)}))
            await asyncio.sleep(1)
        
    def disconnect(self, close_code):
        # Handle disconnection here
        pass



class ChatConsumerTwo(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
        # Room`ga qo‘shilish
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Room`dan chiqish
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        # Save the message to the database
        await self.save_message(message)

        # Room`dagi barcha foydalanuvchilarga xabar yuborish
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    @database_sync_to_async
    def save_message(self, message):
        user = self.scope['user']  # Assuming the user is authenticated
        Message.objects.create(user=user, room_name=self.room_name, content=message)

    # Xabarni chat`ga jo'natish
    async def chat_message(self, event):
        message = event['message']

        # WebSocket orqali xabar yuborish
        await self.send(text_data=json.dumps({
            'message': message
        }))
