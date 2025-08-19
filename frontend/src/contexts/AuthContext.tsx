'use client'

import { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { useRouter } from 'next/navigation'
import { authApi } from '@/lib/api/auth'
import { User, LoginCredentials, RegisterData } from '@/types/auth'
import toast from 'react-hot-toast'

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (credentials: LoginCredentials) => Promise<void>
  register: (data: RegisterData) => Promise<void>
  logout: () => void
  refreshToken: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  // Initialize auth state
  useEffect(() => {
    initializeAuth()
  }, [])

  const initializeAuth = async () => {
    try {
      const token = localStorage.getItem('access_token')
      if (token) {
        // Verify token and get user info
        const userData = await authApi.getCurrentUser()
        setUser(userData)
      }
    } catch (error) {
      // Token is invalid, remove it
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    } finally {
      setLoading(false)
    }
  }

  const login = async (credentials: LoginCredentials) => {
    try {
      setLoading(true)
      const response = await authApi.login(credentials)
      
      // Store tokens
      localStorage.setItem('access_token', response.access_token)
      localStorage.setItem('refresh_token', response.refresh_token)
      
      // Get user data
      const userData = await authApi.getCurrentUser()
      setUser(userData)
      
      toast.success('Welcome back!')
      router.push('/dashboard')
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Login failed'
      toast.error(message)
      throw error
    } finally {
      setLoading(false)
    }
  }

  const register = async (data: RegisterData) => {
    try {
      setLoading(true)
      await authApi.register(data)
      
      // Auto-login after registration
      await login({
        email: data.email,
        password: data.password
      })
      
      toast.success('Account created successfully!')
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Registration failed'
      toast.error(message)
      throw error
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setUser(null)
    toast.success('Logged out successfully')
    router.push('/')
  }

  const refreshToken = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token')
      if (!refreshToken) {
        throw new Error('No refresh token')
      }

      const response = await authApi.refreshToken(refreshToken)
      localStorage.setItem('access_token', response.access_token)
      
      return response.access_token
    } catch (error) {
      // Refresh failed, logout user
      logout()
      throw error
    }
  }

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    refreshToken
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
