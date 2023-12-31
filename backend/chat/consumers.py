import json
from chat import async_db
from .async_db import ACTION, TARGET
from rest_framework.exceptions import ValidationError
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Check if user is authenticated
        if self.scope['user'].is_anonymous:
            return await self.close(code=1000)
        else:
            self.user = self.scope['user']
        # Set online status
        await async_db.setOnlineUser(self.user)
        # Join all chat group
        self.channels = await async_db.getUserChannels(self.user)
        for channel in self.channels:
            group_name = f'group_{channel.id}'
            await self.channel_layer.group_add(group_name, self.channel_name)
        # Set a group for only user
        await self.channel_layer.group_add(f'user_{self.user.id}', self.channel_name)
        # Accept ws connect
        await self.accept()

    async def disconnect(self, close_code):
        # Change offline status
        await async_db.setOfflineUser(self.userId)
        # Leave all chat group
        for channel in self.channels:
            group_name = f'group_{channel.id}'
            await self.channel_layer.group_discard(group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            text_data_json['data'] = await self.dbAsyncHandle(text_data_json)
            target = text_data_json['target']
            # Send message to user
            if target == TARGET.USER:
                userId = text_data_json['targetId']
                await self.channel_layer.group_send(
                    f'user_{userId}', {"type": "chat.send", "text_data_json": text_data_json}
                )
            # Send message to group
            elif target == TARGET.CHANNEL:
                channelId = text_data_json['targetId']
                await self.channel_layer.group_send(
                    f'group_{channelId}', {"type": "chat.send", "text_data_json": text_data_json}
                )
        except Exception as e:
            text_data = json.dumps({"error_message": str(e)})
            # Send error message to user send
            await self.send(text_data=text_data)

    # Receive message from group
    async def chat_send(self, event):
        text_data_json = event["text_data_json"]
        text_data = json.dumps(text_data_json)
        # Send message to WebSocket
        await self.send(text_data=text_data)

    async def dbAsyncHandle(self, text_data_json):
        action = text_data_json.get('action')
        data = text_data_json.get('data')

        if action == ACTION.CREATE_MESSAGE:
            return await async_db.createMessage(data)
        if action == ACTION.REMOVE_MESSAGE:
            return await async_db.deleteMessage(data)
        if action == ACTION.CREATE_REACTION:
            return await async_db.createReaction(data)
        if action == ACTION.REMOVE_REACTION:
            return await async_db.deleteReaction(data)
        if action == ACTION.ADD_MEMBER:
            return await async_db.addMember(data)
        if action == ACTION.REMOVE_MEMBER:
            return await async_db.removeMember(data)
        if action == ACTION.SET_NICKNAME:
            return await async_db.setNickname(data)
        if action == ACTION.SET_CHANNEL_TITLE:
            return await async_db.setChannelTitle(data)
        if action == ACTION.FRIEND_REQUEST:
            return await async_db.friendRequest(self.user, data)
        if action == ACTION.FRIEND_ACCEPT:
            return await async_db.friendAccept(self.user, data)