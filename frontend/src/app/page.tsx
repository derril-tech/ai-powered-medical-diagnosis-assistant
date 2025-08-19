'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  HeartIcon, 
  UserGroupIcon, 
  ChartBarIcon, 
  ShieldCheckIcon,
  ArrowRightIcon,
  SparklesIcon,
  AcademicCapIcon,
  ClockIcon
} from '@heroicons/react/24/outline'
import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'

const features = [
  {
    name: 'Intelligent Symptom Analysis',
    description: 'Advanced AI analyzes patient symptoms using natural language processing and medical knowledge bases.',
    icon: SparklesIcon,
  },
  {
    name: 'Differential Diagnosis Support',
    description: 'Generate comprehensive differential diagnoses ranked by likelihood with supporting evidence.',
    icon: ChartBarIcon,
  },
  {
    name: 'Evidence-Based Insights',
    description: 'Access peer-reviewed research and clinical guidelines supporting each diagnostic suggestion.',
    icon: AcademicCapIcon,
  },
  {
    name: 'Real-Time Collaboration',
    description: 'Collaborate with colleagues in real-time for complex cases and second opinions.',
    icon: UserGroupIcon,
  },
  {
    name: 'HIPAA Compliant Security',
    description: 'Enterprise-grade security ensuring patient data protection and regulatory compliance.',
    icon: ShieldCheckIcon,
  },
  {
    name: 'Rapid Analysis',
    description: 'Get diagnostic insights in seconds, not minutes, improving clinical workflow efficiency.',
    icon: ClockIcon,
  },
]

const stats = [
  { name: 'Healthcare Professionals', value: '10,000+' },
  { name: 'Diagnostic Accuracy', value: '94.7%' },
  { name: 'Time Saved Per Case', value: '15 min' },
  { name: 'Medical Conditions', value: '5,000+' },
]

export default function HomePage() {
  const { user, loading } = useAuth()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return <LoadingSpinner />
  }

  if (loading) {
    return <LoadingSpinner />
  }

  // If user is authenticated, redirect to dashboard
  if (user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-neutral-900 dark:to-neutral-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center"
          >
            <h1 className="text-4xl font-bold text-neutral-900 dark:text-white mb-4">
              Welcome back, Dr. {user.full_name}
            </h1>
            <p className="text-xl text-neutral-600 dark:text-neutral-300 mb-8">
              Ready to assist with your next diagnostic challenge?
            </p>
            <Link
              href="/dashboard"
              className="medical-button text-lg px-8 py-3"
            >
              Go to Dashboard
              <ArrowRightIcon className="ml-2 h-5 w-5" />
            </Link>
          </motion.div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white dark:bg-neutral-900">
      {/* Hero Section */}
      <div className="relative isolate px-6 pt-14 lg:px-8">
        <div className="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80">
          <div className="relative left-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 rotate-[30deg] bg-gradient-to-tr from-primary-400 to-secondary-400 opacity-20 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]" />
        </div>

        <div className="mx-auto max-w-4xl py-32 sm:py-48 lg:py-56">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            <div className="flex justify-center mb-8">
              <div className="flex items-center space-x-2 bg-primary-100 dark:bg-primary-900/30 px-4 py-2 rounded-full">
                <HeartIcon className="h-6 w-6 text-primary-600 dark:text-primary-400" />
                <span className="text-sm font-medium text-primary-700 dark:text-primary-300">
                  AI-Powered Medical Diagnosis
                </span>
              </div>
            </div>

            <h1 className="text-4xl font-bold tracking-tight text-neutral-900 dark:text-white sm:text-6xl">
              Your Intelligent
              <span className="text-primary-600 dark:text-primary-400"> Diagnostic</span>
              <br />
              Partner
            </h1>

            <p className="mt-6 text-lg leading-8 text-neutral-600 dark:text-neutral-300 max-w-2xl mx-auto">
              AuraMD empowers healthcare professionals with AI-driven diagnostic support, 
              evidence-based insights, and real-time collaboration tools to enhance patient care 
              and clinical decision-making.
            </p>

            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Link
                href="/auth/login"
                className="medical-button text-lg px-8 py-3"
              >
                Get Started
                <ArrowRightIcon className="ml-2 h-5 w-5" />
              </Link>
              <Link
                href="/demo"
                className="medical-button-secondary text-lg px-8 py-3"
              >
                Watch Demo
              </Link>
            </div>
          </motion.div>
        </div>

        <div className="absolute inset-x-0 top-[calc(100%-13rem)] -z-10 transform-gpu overflow-hidden blur-3xl sm:top-[calc(100%-30rem)]">
          <div className="relative left-[calc(50%+3rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 bg-gradient-to-tr from-secondary-400 to-primary-400 opacity-20 sm:left-[calc(50%+36rem)] sm:w-[72.1875rem]" />
        </div>
      </div>

      {/* Stats Section */}
      <motion.div 
        initial={{ opacity: 0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        viewport={{ once: true }}
        className="bg-primary-600 dark:bg-primary-800 py-16"
      >
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <dl className="grid grid-cols-1 gap-x-8 gap-y-16 text-center lg:grid-cols-4">
            {stats.map((stat, index) => (
              <motion.div 
                key={stat.name}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="mx-auto flex max-w-xs flex-col gap-y-4"
              >
                <dt className="text-base leading-7 text-primary-100">
                  {stat.name}
                </dt>
                <dd className="order-first text-3xl font-semibold tracking-tight text-white sm:text-5xl">
                  {stat.value}
                </dd>
              </motion.div>
            ))}
          </dl>
        </div>
      </motion.div>

      {/* Features Section */}
      <div className="py-24 sm:py-32 bg-neutral-50 dark:bg-neutral-800">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="mx-auto max-w-2xl lg:text-center"
          >
            <h2 className="text-base font-semibold leading-7 text-primary-600 dark:text-primary-400">
              Advanced AI Technology
            </h2>
            <p className="mt-2 text-3xl font-bold tracking-tight text-neutral-900 dark:text-white sm:text-4xl">
              Everything you need for intelligent diagnosis
            </p>
            <p className="mt-6 text-lg leading-8 text-neutral-600 dark:text-neutral-300">
              AuraMD combines cutting-edge AI with medical expertise to provide comprehensive 
              diagnostic support that enhances clinical workflows and improves patient outcomes.
            </p>
          </motion.div>

          <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
            <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-16 lg:max-w-none lg:grid-cols-3">
              {features.map((feature, index) => (
                <motion.div 
                  key={feature.name}
                  initial={{ opacity: 0, y: 40 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  className="flex flex-col medical-card p-6 hover:scale-105 transition-transform duration-200"
                >
                  <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-neutral-900 dark:text-white">
                    <feature.icon className="h-5 w-5 flex-none text-primary-600 dark:text-primary-400" />
                    {feature.name}
                  </dt>
                  <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-neutral-600 dark:text-neutral-300">
                    <p className="flex-auto">{feature.description}</p>
                  </dd>
                </motion.div>
              ))}
            </dl>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <motion.div 
        initial={{ opacity: 0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        viewport={{ once: true }}
        className="bg-primary-600 dark:bg-primary-800"
      >
        <div className="px-6 py-24 sm:px-6 sm:py-32 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
              Ready to transform your diagnostic workflow?
            </h2>
            <p className="mx-auto mt-6 max-w-xl text-lg leading-8 text-primary-100">
              Join thousands of healthcare professionals who trust AuraMD for 
              intelligent diagnostic support and evidence-based clinical insights.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Link
                href="/auth/register"
                className="bg-white px-8 py-3 text-lg font-semibold text-primary-600 shadow-sm hover:bg-primary-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white rounded-md transition-colors duration-200"
              >
                Start Free Trial
              </Link>
              <Link
                href="/contact"
                className="text-lg font-semibold leading-6 text-white hover:text-primary-100 transition-colors duration-200"
              >
                Contact Sales <span aria-hidden="true">→</span>
              </Link>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  )
}
