import { api } from './client'
import { User, LoginCredentials, RegisterData, TokenResponse } from '@/types/auth'

export const authApi = {
  login: async (credentials: LoginCredentials): Promise<TokenResponse> => {
    const formData = new FormData()
    formData.append('username', credentials.email)
    formData.append('password', credentials.password)
    
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    return response.data
  },

  register: async (data: RegisterData): Promise<User> => {
    const response = await api.post('/auth/register', data)
    return response.data
  },

  refreshToken: async (refreshToken: string): Promise<TokenResponse> => {
    const response = await api.post('/auth/refresh', { refresh_token: refreshToken })
    return response.data
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/auth/me')
    return response.data
  },

  logout: async (): Promise<void> => {
    await api.post('/auth/logout')
  },
}
