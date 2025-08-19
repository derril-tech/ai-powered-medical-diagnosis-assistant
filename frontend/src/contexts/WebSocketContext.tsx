'use client'

import { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { io, Socket } from 'socket.io-client'
import { useAuth } from '@/hooks/useAuth'

interface WebSocketContextType {
  socket: Socket | null
  connected: boolean
  sendMessage: (event: string, data: any) => void
}

const WebSocketContext = createContext<WebSocketContextType | undefined>(undefined)

interface WebSocketProviderProps {
  children: ReactNode
}

export function WebSocketProvider({ children }: WebSocketProviderProps) {
  const [socket, setSocket] = useState<Socket | null>(null)
  const [connected, setConnected] = useState(false)
  const { user } = useAuth()

  useEffect(() => {
    if (user && process.env.NEXT_PUBLIC_WS_URL) {
      const newSocket = io(process.env.NEXT_PUBLIC_WS_URL, {
        auth: {
          token: localStorage.getItem('access_token')
        },
        transports: ['websocket']
      })

      newSocket.on('connect', () => {
        console.log('WebSocket connected')
        setConnected(true)
      })

      newSocket.on('disconnect', () => {
        console.log('WebSocket disconnected')
        setConnected(false)
      })

      newSocket.on('error', (error) => {
        console.error('WebSocket error:', error)
      })

      setSocket(newSocket)

      return () => {
        newSocket.close()
        setSocket(null)
        setConnected(false)
      }
    }
  }, [user])

  const sendMessage = (event: string, data: any) => {
    if (socket && connected) {
      socket.emit(event, data)
    }
  }

  const value = {
    socket,
    connected,
    sendMessage
  }

  return (
    <WebSocketContext.Provider value={value}>
      {children}
    </WebSocketContext.Provider>
  )
}

export function useWebSocket() {
  const context = useContext(WebSocketContext)
  if (context === undefined) {
    throw new Error('useWebSocket must be used within a WebSocketProvider')
  }
  return context
}
