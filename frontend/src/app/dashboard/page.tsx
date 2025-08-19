'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  PlusIcon,
  UserGroupIcon,
  ChartBarIcon,
  ClockIcon,
  HeartIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline'
import { useAuth } from '@/hooks/useAuth'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'

// Example dashboard for healthcare professionals
export default function DashboardPage() {
  const { user, loading } = useAuth()
  const [activeTab, setActiveTab] = useState('overview')

  if (loading) {
    return <LoadingSpinner />
  }

  if (!user) {
    return <div>Please log in to access the dashboard</div>
  }

  const stats = [
    { name: 'Active Patients', value: '127', icon: UserGroupIcon, change: '+12%' },
    { name: 'Diagnoses Today', value: '23', icon: ChartBarIcon, change: '+8%' },
    { name: 'Avg Response Time', value: '1.2s', icon: ClockIcon, change: '-15%' },
    { name: 'Accuracy Rate', value: '94.7%', icon: HeartIcon, change: '+2%' },
  ]

  const recentCases = [
    {
      id: '1',
      patient: 'Patient A',
      complaint: 'Chest pain and shortness of breath',
      urgency: 'urgent',
      confidence: 0.87,
      status: 'completed'
    },
    {
      id: '2',
      patient: 'Patient B',
      complaint: 'Persistent headache with nausea',
      urgency: 'moderate',
      confidence: 0.73,
      status: 'in_progress'
    },
    {
      id: '3',
      patient: 'Patient C',
      complaint: 'Abdominal pain, lower right quadrant',
      urgency: 'emergency',
      confidence: 0.91,
      status: 'completed'
    }
  ]

  return (
    <div className="min-h-screen bg-neutral-50 dark:bg-neutral-900">
      {/* Header */}
      <div className="bg-white dark:bg-neutral-800 shadow-sm border-b border-neutral-200 dark:border-neutral-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-neutral-900 dark:text-white">
                Welcome back, Dr. {user.full_name}
              </h1>
              <p className="text-neutral-600 dark:text-neutral-300">
                {user.specialization} • {user.hospital_affiliation}
              </p>
            </div>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="medical-button"
            >
              <PlusIcon className="h-5 w-5 mr-2" />
              New Diagnosis
            </motion.button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <motion.div
              key={stat.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="medical-card p-6"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-neutral-600 dark:text-neutral-300">
                    {stat.name}
                  </p>
                  <p className="text-2xl font-semibold text-neutral-900 dark:text-white">
                    {stat.value}
                  </p>
                </div>
                <stat.icon className="h-8 w-8 text-primary-600 dark:text-primary-400" />
              </div>
              <div className="mt-4">
                <span className="text-sm text-green-600 dark:text-green-400">
                  {stat.change}
                </span>
                <span className="text-sm text-neutral-500 dark:text-neutral-400 ml-1">
                  vs last week
                </span>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Recent Cases */}
        <div className="medical-card p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-neutral-900 dark:text-white">
              Recent Diagnosis Cases
            </h2>
            <button className="medical-button-secondary text-sm">
              View All Cases
            </button>
          </div>

          <div className="overflow-hidden">
            <table className="min-w-full divide-y divide-neutral-200 dark:divide-neutral-700">
              <thead className="bg-neutral-50 dark:bg-neutral-800">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">
                    Patient
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">
                    Chief Complaint
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">
                    Urgency
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">
                    AI Confidence
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-neutral-800 divide-y divide-neutral-200 dark:divide-neutral-700">
                {recentCases.map((case_item) => (
                  <tr key={case_item.id} className="hover:bg-neutral-50 dark:hover:bg-neutral-700">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-neutral-900 dark:text-white">
                      {case_item.patient}
                    </td>
                    <td className="px-6 py-4 text-sm text-neutral-600 dark:text-neutral-300">
                      {case_item.complaint}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full urgency-${case_item.urgency}`}>
                        {case_item.urgency}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-600 dark:text-neutral-300">
                      <div className="flex items-center">
                        <div className="w-16 bg-neutral-200 dark:bg-neutral-700 rounded-full h-2 mr-2">
                          <div 
                            className="bg-primary-600 h-2 rounded-full" 
                            style={{ width: `${case_item.confidence * 100}%` }}
                          ></div>
                        </div>
                        {Math.round(case_item.confidence * 100)}%
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                        case_item.status === 'completed' 
                          ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300'
                          : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300'
                      }`}>
                        {case_item.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* AI Insights Panel */}
        <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="medical-card p-6">
            <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-4">
              AI Insights
            </h3>
            <div className="space-y-4">
              <div className="flex items-start space-x-3">
                <HeartIcon className="h-5 w-5 text-green-500 mt-1" />
                <div>
                  <p className="text-sm font-medium text-neutral-900 dark:text-white">
                    Diagnostic Accuracy Improved
                  </p>
                  <p className="text-sm text-neutral-600 dark:text-neutral-300">
                    Your diagnostic accuracy has increased by 2% this week
                  </p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <ExclamationTriangleIcon className="h-5 w-5 text-yellow-500 mt-1" />
                <div>
                  <p className="text-sm font-medium text-neutral-900 dark:text-white">
                    Pattern Alert
                  </p>
                  <p className="text-sm text-neutral-600 dark:text-neutral-300">
                    Increased respiratory symptoms in recent cases
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="medical-card p-6">
            <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-4">
              Quick Actions
            </h3>
            <div className="space-y-3">
              <button className="w-full medical-button-secondary text-left">
                Start New Diagnosis Session
              </button>
              <button className="w-full medical-button-secondary text-left">
                Review Pending Cases
              </button>
              <button className="w-full medical-button-secondary text-left">
                Access Medical Literature
              </button>
              <button className="w-full medical-button-secondary text-left">
                Collaborate with Colleagues
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
