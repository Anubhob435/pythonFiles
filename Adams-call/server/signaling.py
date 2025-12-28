"""
WebSocket signaling server for WebRTC communication.
"""
import json
import asyncio
from aiohttp import web, WSMsgType
from typing import Dict, Set
from .rooms import room_manager, Participant, Room
from .auth import get_user_from_token


class SignalingServer:
    """WebSocket signaling server for WebRTC."""
    
    def __init__(self):
        self.connections: Dict[str, web.WebSocketResponse] = {}
    
    async def handle_websocket(self, request: web.Request) -> web.WebSocketResponse:
        """Handle WebSocket connections for signaling."""
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        user_data = None
        user_id = None
        
        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    try:
                        data = json.loads(msg.data)
                        message_type = data.get("type")
                        
                        # Handle authentication
                        if message_type == "auth":
                            token = data.get("token")
                            user_data = await get_user_from_token(token)
                            if user_data:
                                user_id = user_data["user_id"]
                                self.connections[user_id] = ws
                                await self._send(ws, {
                                    "type": "auth_success",
                                    "user_id": user_id,
                                    "username": user_data["username"]
                                })
                            else:
                                await self._send(ws, {
                                    "type": "auth_error",
                                    "error": "Invalid token"
                                })
                            continue
                        
                        # Require authentication for other messages
                        if not user_data:
                            await self._send(ws, {
                                "type": "error",
                                "error": "Not authenticated"
                            })
                            continue
                        
                        # Handle different message types
                        if message_type == "create_room":
                            await self._handle_create_room(ws, user_data)
                        
                        elif message_type == "join_room":
                            room_code = data.get("room_code")
                            await self._handle_join_room(ws, user_data, room_code)
                        
                        elif message_type == "leave_room":
                            await self._handle_leave_room(user_data)
                        
                        elif message_type == "offer":
                            await self._relay_to_room(user_data, data)
                        
                        elif message_type == "answer":
                            await self._relay_to_room(user_data, data)
                        
                        elif message_type == "ice_candidate":
                            await self._relay_to_room(user_data, data)
                        
                        elif message_type == "chat_message":
                            await self._handle_chat_message(user_data, data)
                        
                        elif message_type == "media_state":
                            await self._handle_media_state(user_data, data)
                        
                    except json.JSONDecodeError:
                        await self._send(ws, {
                            "type": "error",
                            "error": "Invalid JSON"
                        })
                
                elif msg.type == WSMsgType.ERROR:
                    print(f"WebSocket error: {ws.exception()}")
                    break
        
        finally:
            # Clean up on disconnect
            if user_id:
                self.connections.pop(user_id, None)
                await self._handle_leave_room(user_data)
        
        return ws
    
    async def _send(self, ws: web.WebSocketResponse, data: dict):
        """Send a message to a WebSocket."""
        try:
            if not ws.closed:
                await ws.send_json(data)
        except Exception as e:
            print(f"Error sending message: {e}")
    
    async def _handle_create_room(self, ws: web.WebSocketResponse, user_data: dict):
        """Handle room creation."""
        room = await room_manager.create_room(user_data["user_id"])
        
        # Auto-join the creator to the room
        participant = Participant(
            user_id=user_data["user_id"],
            username=user_data["username"],
            websocket=ws
        )
        await room_manager.join_room(room.room_code, participant)
        
        await self._send(ws, {
            "type": "room_created",
            "room_id": room.room_id,
            "room_code": room.room_code
        })
    
    async def _handle_join_room(self, ws: web.WebSocketResponse, user_data: dict, room_code: str):
        """Handle room joining."""
        if not room_code:
            await self._send(ws, {
                "type": "error",
                "error": "Room code required"
            })
            return
        
        # Check if room exists
        room = await room_manager.get_room_by_code(room_code)
        if not room:
            await self._send(ws, {
                "type": "error",
                "error": "Room not found"
            })
            return
        
        # Get existing participants before joining
        existing_participants = [
            {"user_id": p.user_id, "username": p.username}
            for p in room.participants.values()
        ]
        
        # Create participant and join
        participant = Participant(
            user_id=user_data["user_id"],
            username=user_data["username"],
            websocket=ws
        )
        
        joined_room = await room_manager.join_room(room_code, participant)
        if not joined_room:
            await self._send(ws, {
                "type": "error",
                "error": "Failed to join room (room may be full)"
            })
            return
        
        # Notify the joining user
        await self._send(ws, {
            "type": "room_joined",
            "room_id": room.room_id,
            "room_code": room.room_code,
            "participants": existing_participants
        })
        
        # Notify existing participants about new user
        for p in room.get_other_participants(user_data["user_id"]):
            other_ws = self.connections.get(p.user_id)
            if other_ws:
                await self._send(other_ws, {
                    "type": "user_joined",
                    "user_id": user_data["user_id"],
                    "username": user_data["username"]
                })
    
    async def _handle_leave_room(self, user_data: dict):
        """Handle room leaving."""
        if not user_data:
            return
        
        result = await room_manager.leave_room(user_data["user_id"])
        if result:
            room, participant = result
            # Notify remaining participants
            for p in room.participants.values():
                other_ws = self.connections.get(p.user_id)
                if other_ws:
                    await self._send(other_ws, {
                        "type": "user_left",
                        "user_id": user_data["user_id"],
                        "username": user_data["username"]
                    })
    
    async def _relay_to_room(self, user_data: dict, data: dict):
        """Relay WebRTC signaling messages to room participants."""
        room = await room_manager.get_user_room(user_data["user_id"])
        if not room:
            return
        
        target_user_id = data.get("target_user_id")
        
        # Add sender info
        data["from_user_id"] = user_data["user_id"]
        data["from_username"] = user_data["username"]
        
        if target_user_id:
            # Send to specific user
            target_ws = self.connections.get(target_user_id)
            if target_ws:
                await self._send(target_ws, data)
        else:
            # Broadcast to all other participants
            for p in room.get_other_participants(user_data["user_id"]):
                other_ws = self.connections.get(p.user_id)
                if other_ws:
                    await self._send(other_ws, data)
    
    async def _handle_chat_message(self, user_data: dict, data: dict):
        """Handle chat messages."""
        room = await room_manager.get_user_room(user_data["user_id"])
        if not room:
            return
        
        message = {
            "type": "chat_message",
            "from_user_id": user_data["user_id"],
            "from_username": user_data["username"],
            "message": data.get("message", ""),
            "timestamp": data.get("timestamp")
        }
        
        # Broadcast to all participants including sender
        for p in room.participants.values():
            ws = self.connections.get(p.user_id)
            if ws:
                await self._send(ws, message)
    
    async def _handle_media_state(self, user_data: dict, data: dict):
        """Handle media state changes (mute/unmute, camera on/off)."""
        room = await room_manager.get_user_room(user_data["user_id"])
        if not room:
            return
        
        # Update participant state
        participant = room.get_participant(user_data["user_id"])
        if participant:
            if "audio_enabled" in data:
                participant.is_audio_enabled = data["audio_enabled"]
            if "video_enabled" in data:
                participant.is_video_enabled = data["video_enabled"]
        
        # Broadcast state change to other participants
        for p in room.get_other_participants(user_data["user_id"]):
            other_ws = self.connections.get(p.user_id)
            if other_ws:
                await self._send(other_ws, {
                    "type": "media_state",
                    "user_id": user_data["user_id"],
                    "username": user_data["username"],
                    "audio_enabled": data.get("audio_enabled"),
                    "video_enabled": data.get("video_enabled")
                })


# Global signaling server instance
signaling_server = SignalingServer()
