import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: Date | string): string {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(new Date(date))
}

export function formatDateTime(date: Date | string): string {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(date))
}

export function formatConfidenceScore(score: number): string {
  return `${Math.round(score * 100)}%`
}

export function getConfidenceLevel(score: number): 'low' | 'moderate' | 'high' {
  if (score >= 0.8) return 'high'
  if (score >= 0.6) return 'moderate'
  return 'low'
}

export function getUrgencyColor(urgency: string): string {
  const colors = {
    emergency: 'bg-red-600 text-white',
    urgent: 'bg-orange-500 text-white',
    moderate: 'bg-yellow-500 text-white',
    routine: 'bg-green-500 text-white',
  }
  return colors[urgency as keyof typeof colors] || colors.routine
}

export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text
  return text.slice(0, maxLength) + '...'
}

export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

export function generatePatientId(): string {
  return `P-${Date.now()}-${Math.random().toString(36).substr(2, 5).toUpperCase()}`
}

export function formatMedicalLicense(license: string): string {
  return license.replace(/(\w{2})(\w{4})(\w{4})/, '$1-$2-$3')
}
