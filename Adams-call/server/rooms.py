"""
Room and session management for WebRTC communication.
"""
import uuid
import asyncio
from datetime import datetime
from typing import Dict, Set, Optional
from dataclasses import dataclass, field


@dataclass
class Participant:
    """Represents a participant in a room."""
    user_id: str
    username: str
    websocket: any
    joined_at: datetime = field(default_factory=datetime.now)
    is_audio_enabled: bool = True
    is_video_enabled: bool = True


@dataclass
class Room:
    """Represents a communication room."""
    room_id: str
    room_code: str
    created_by: str
    created_at: datetime = field(default_factory=datetime.now)
    participants: Dict[str, Participant] = field(default_factory=dict)
    max_participants: int = 10
    
    def add_participant(self, participant: Participant) -> bool:
        """Add a participant to the room."""
        if len(self.participants) >= self.max_participants:
            return False
        self.participants[participant.user_id] = participant
        return True
    
    def remove_participant(self, user_id: str) -> Optional[Participant]:
        """Remove a participant from the room."""
        return self.participants.pop(user_id, None)
    
    def get_participant(self, user_id: str) -> Optional[Participant]:
        """Get a participant by user ID."""
        return self.participants.get(user_id)
    
    def get_other_participants(self, user_id: str) -> list:
        """Get all participants except the specified user."""
        return [p for uid, p in self.participants.items() if uid != user_id]
    
    def is_empty(self) -> bool:
        """Check if room is empty."""
        return len(self.participants) == 0


class RoomManager:
    """Manages all rooms and participants."""
    
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        self.room_codes: Dict[str, str] = {}  # code -> room_id mapping
        self.user_rooms: Dict[str, str] = {}  # user_id -> room_id mapping
        self._lock = asyncio.Lock()
    
    def _generate_room_code(self) -> str:
        """Generate a unique 6-character room code."""
        while True:
            code = uuid.uuid4().hex[:6].upper()
            if code not in self.room_codes:
                return code
    
    async def create_room(self, user_id: str) -> Room:
        """Create a new room."""
        async with self._lock:
            room_id = str(uuid.uuid4())
            room_code = self._generate_room_code()
            room = Room(
                room_id=room_id,
                room_code=room_code,
                created_by=user_id
            )
            self.rooms[room_id] = room
            self.room_codes[room_code] = room_id
            return room
    
    async def get_room_by_code(self, code: str) -> Optional[Room]:
        """Get a room by its code."""
        room_id = self.room_codes.get(code.upper())
        if room_id:
            return self.rooms.get(room_id)
        return None
    
    async def get_room(self, room_id: str) -> Optional[Room]:
        """Get a room by ID."""
        return self.rooms.get(room_id)
    
    async def join_room(self, room_code: str, participant: Participant) -> Optional[Room]:
        """Join a room by code."""
        async with self._lock:
            room = await self.get_room_by_code(room_code)
            if room and room.add_participant(participant):
                self.user_rooms[participant.user_id] = room.room_id
                return room
            return None
    
    async def leave_room(self, user_id: str) -> Optional[tuple]:
        """Leave current room. Returns (room, participant) or None."""
        async with self._lock:
            room_id = self.user_rooms.pop(user_id, None)
            if room_id:
                room = self.rooms.get(room_id)
                if room:
                    participant = room.remove_participant(user_id)
                    # Clean up empty rooms
                    if room.is_empty():
                        del self.rooms[room_id]
                        del self.room_codes[room.room_code]
                    return (room, participant)
            return None
    
    async def get_user_room(self, user_id: str) -> Optional[Room]:
        """Get the room a user is currently in."""
        room_id = self.user_rooms.get(user_id)
        if room_id:
            return self.rooms.get(room_id)
        return None
    
    def get_stats(self) -> dict:
        """Get room manager statistics."""
        return {
            "total_rooms": len(self.rooms),
            "total_participants": sum(len(r.participants) for r in self.rooms.values())
        }


# Global room manager instance
room_manager = RoomManager()
