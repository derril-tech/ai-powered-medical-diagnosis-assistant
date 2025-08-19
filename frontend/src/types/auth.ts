export interface User {
  id: string
  email: string
  full_name: string
  role: 'doctor' | 'nurse' | 'admin' | 'specialist'
  medical_license?: string
  specialization?: string
  hospital_affiliation?: string
  is_active: boolean
  is_verified: boolean
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  full_name: string
  role: 'doctor' | 'nurse' | 'admin' | 'specialist'
  medical_license?: string
  specialization?: string
  hospital_affiliation?: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}
