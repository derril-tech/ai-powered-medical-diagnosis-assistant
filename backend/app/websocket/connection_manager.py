"""
WebSocket Connection Manager
Real-time communication for medical consultations
"""

from typing import Dict, List
from fastapi import WebSocket
import json
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_sessions: Dict[str, str] = {}  # user_id -> session_id mapping

    async def connect(self, websocket: WebSocket, user_id: str):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        
        # Send welcome message
        await self.send_personal_message({
            "type": "connection_established",
            "message": "Connected to AuraMD real-time services",
            "user_id": user_id
        }, user_id)

    def disconnect(self, user_id: str):
        """Remove WebSocket connection"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.user_sessions:
            del self.user_sessions[user_id]

    async def send_personal_message(self, message: dict, user_id: str):
        """Send message to specific user"""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(json.dumps(message))
            except Exception as e:
                print(f"Error sending message to {user_id}: {e}")
                # Remove broken connection
                self.disconnect(user_id)

    async def broadcast_to_session(self, message: dict, session_id: str):
        """Broadcast message to all users in a session"""
        for user_id, user_session_id in self.user_sessions.items():
            if user_session_id == session_id:
                await self.send_personal_message(message, user_id)

    async def broadcast_diagnosis_update(self, diagnosis_data: dict, session_id: str):
        """Broadcast diagnosis updates to relevant users"""
        message = {
            "type": "diagnosis_update",
            "data": diagnosis_data,
            "session_id": session_id,
            "timestamp": asyncio.get_event_loop().time()
        }
        await self.broadcast_to_session(message, session_id)

    async def send_ai_analysis_progress(self, user_id: str, progress: dict):
        """Send AI analysis progress updates"""
        message = {
            "type": "ai_analysis_progress",
            "progress": progress,
            "timestamp": asyncio.get_event_loop().time()
        }
        await self.send_personal_message(message, user_id)

    async def send_consultation_invite(self, from_user_id: str, to_user_id: str, session_id: str):
        """Send consultation invitation"""
        message = {
            "type": "consultation_invite",
            "from_user_id": from_user_id,
            "session_id": session_id,
            "timestamp": asyncio.get_event_loop().time()
        }
        await self.send_personal_message(message, to_user_id)

    def get_active_users(self) -> List[str]:
        """Get list of active user IDs"""
        return list(self.active_connections.keys())

    def is_user_online(self, user_id: str) -> bool:
        """Check if user is currently online"""
        return user_id in self.active_connections
