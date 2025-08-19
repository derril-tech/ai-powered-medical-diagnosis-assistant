'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useForm, useFieldArray } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import {
  PlusIcon,
  TrashIcon,
  SparklesIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'

// Symptom analysis form schema
const symptomSchema = z.object({
  name: z.string().min(1, 'Symptom name is required'),
  description: z.string().optional(),
  severity: z.enum(['mild', 'moderate', 'severe', 'critical']),
  duration: z.enum(['acute', 'subacute', 'chronic']),
  bodyLocation: z.string().optional(),
  associatedSymptoms: z.string().optional(),
  triggers: z.string().optional(),
  relievingFactors: z.string().optional(),
})

const diagnosisSchema = z.object({
  patientId: z.string().min(1, 'Patient ID is required'),
  chiefComplaint: z.string().min(1, 'Chief complaint is required'),
  symptoms: z.array(symptomSchema).min(1, 'At least one symptom is required'),
  medicalHistory: z.string().optional(),
})

type DiagnosisFormData = z.infer<typeof diagnosisSchema>

interface SymptomAnalyzerProps {
  patientId?: string
  onAnalysisComplete?: (result: any) => void
}

export function SymptomAnalyzer({ patientId, onAnalysisComplete }: SymptomAnalyzerProps) {
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [currentStep, setCurrentStep] = useState(1)

  const { control, register, handleSubmit, formState: { errors }, watch } = useForm<DiagnosisFormData>({
    resolver: zodResolver(diagnosisSchema),
    defaultValues: {
      patientId: patientId || '',
      chiefComplaint: '',
      symptoms: [{ 
        name: '', 
        severity: 'moderate', 
        duration: 'acute',
        description: '',
        bodyLocation: '',
        associatedSymptoms: '',
        triggers: '',
        relievingFactors: ''
      }],
      medicalHistory: ''
    }
  })

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'symptoms'
  })

  const onSubmit = async (data: DiagnosisFormData) => {
    setIsAnalyzing(true)
    try {
      // Simulate AI analysis - replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      const mockResult = {
        sessionId: 'session-123',
        differentialDiagnoses: [
          {
            conditionName: 'Acute Myocardial Infarction',
            confidenceScore: 0.87,
            aiReasoning: 'Chest pain with radiation, elevated cardiac markers, and ECG changes suggest acute MI.',
            differentialRank: 1
          },
          {
            conditionName: 'Unstable Angina',
            confidenceScore: 0.73,
            aiReasoning: 'Chest pain pattern consistent with unstable angina, but biomarkers needed.',
            differentialRank: 2
          },
          {
            conditionName: 'Pulmonary Embolism',
            confidenceScore: 0.65,
            aiReasoning: 'Shortness of breath and chest pain could indicate PE, D-dimer recommended.',
            differentialRank: 3
          }
        ],
        recommendedTests: [
          'ECG (12-lead)',
          'Cardiac enzymes (Troponin I/T)',
          'Complete Blood Count',
          'D-dimer',
          'Chest X-ray'
        ],
        urgencyLevel: 'emergency',
        clinicalReasoning: 'Patient presents with acute chest pain and dyspnea. Given the symptom constellation and severity, immediate cardiac evaluation is warranted.',
        redFlags: [
          'Severe chest pain',
          'Shortness of breath',
          'Potential cardiac event'
        ]
      }
      
      setAnalysisResult(mockResult)
      onAnalysisComplete?.(mockResult)
    } catch (error) {
      console.error('Analysis failed:', error)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const addSymptom = () => {
    append({ 
      name: '', 
      severity: 'moderate', 
      duration: 'acute',
      description: '',
      bodyLocation: '',
      associatedSymptoms: '',
      triggers: '',
      relievingFactors: ''
    })
  }

  const getConfidenceColor = (score: number) => {
    if (score >= 0.8) return 'diagnosis-confidence-high'
    if (score >= 0.6) return 'diagnosis-confidence-moderate'
    return 'diagnosis-confidence-low'
  }

  const getUrgencyColor = (level: string) => {
    const colors = {
      emergency: 'urgency-emergency',
      urgent: 'urgency-urgent',
      moderate: 'urgency-moderate',
      routine: 'urgency-routine'
    }
    return colors[level as keyof typeof colors] || 'urgency-routine'
  }

  if (analysisResult) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="space-y-6"
      >
        {/* Analysis Results Header */}
        <div className="medical-card p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-neutral-900 dark:text-white flex items-center">
              <SparklesIcon className="h-6 w-6 text-primary-600 mr-2" />
              AI Diagnosis Analysis
            </h2>
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${getUrgencyColor(analysisResult.urgencyLevel)}`}>
              {analysisResult.urgencyLevel.toUpperCase()}
            </div>
          </div>
          <p className="text-neutral-600 dark:text-neutral-300">
            {analysisResult.clinicalReasoning}
          </p>
        </div>

        {/* Differential Diagnoses */}
        <div className="medical-card p-6">
          <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-4">
            Differential Diagnoses
          </h3>
          <div className="space-y-4">
            {analysisResult.differentialDiagnoses.map((diagnosis, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className={`p-4 rounded-lg border-2 ${getConfidenceColor(diagnosis.confidenceScore)}`}
              >
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-semibold">
                    #{diagnosis.differentialRank} {diagnosis.conditionName}
                  </h4>
                  <div className="flex items-center space-x-2">
                    <div className="w-24 bg-neutral-200 dark:bg-neutral-700 rounded-full h-2">
                      <div 
                        className="bg-current h-2 rounded-full transition-all duration-500" 
                        style={{ width: `${diagnosis.confidenceScore * 100}%` }}
                      />
                    </div>
                    <span className="text-sm font-medium">
                      {Math.round(diagnosis.confidenceScore * 100)}%
                    </span>
                  </div>
                </div>
                <p className="text-sm opacity-90">
                  {diagnosis.aiReasoning}
                </p>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Recommended Tests */}
        <div className="medical-card p-6">
          <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-4">
            Recommended Diagnostic Tests
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {analysisResult.recommendedTests.map((test, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.05 }}
                className="flex items-center space-x-3 p-3 bg-primary-50 dark:bg-primary-900/20 rounded-lg"
              >
                <CheckCircleIcon className="h-5 w-5 text-primary-600 dark:text-primary-400" />
                <span className="text-sm font-medium text-neutral-900 dark:text-white">
                  {test}
                </span>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Red Flags */}
        {analysisResult.redFlags.length > 0 && (
          <div className="medical-card p-6 border-l-4 border-red-500">
            <h3 className="text-lg font-semibold text-red-700 dark:text-red-400 mb-4 flex items-center">
              <ExclamationTriangleIcon className="h-5 w-5 mr-2" />
              Clinical Red Flags
            </h3>
            <ul className="space-y-2">
              {analysisResult.redFlags.map((flag, index) => (
                <li key={index} className="text-sm text-red-600 dark:text-red-400 flex items-center">
                  <span className="w-2 h-2 bg-red-500 rounded-full mr-2" />
                  {flag}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex space-x-4">
          <button
            onClick={() => setAnalysisResult(null)}
            className="medical-button-secondary"
          >
            New Analysis
          </button>
          <button className="medical-button">
            Save to Patient Record
          </button>
          <button className="medical-button-secondary">
            Share with Colleague
          </button>
        </div>
      </motion.div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="max-w-4xl mx-auto space-y-6"
    >
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Step 1: Basic Information */}
        <div className="medical-card p-6">
          <h2 className="text-xl font-semibold text-neutral-900 dark:text-white mb-6">
            Patient Information & Chief Complaint
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                Patient ID
              </label>
              <input
                {...register('patientId')}
                className="medical-input"
                placeholder="Enter patient ID"
              />
              {errors.patientId && (
                <p className="text-red-500 text-sm mt-1">{errors.patientId.message}</p>
              )}
            </div>
            
            <div className="md:col-span-1">
              <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                Chief Complaint
              </label>
              <input
                {...register('chiefComplaint')}
                className="medical-input"
                placeholder="Primary reason for consultation"
              />
              {errors.chiefComplaint && (
                <p className="text-red-500 text-sm mt-1">{errors.chiefComplaint.message}</p>
              )}
            </div>
          </div>

          <div className="mt-6">
            <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
              Medical History (Optional)
            </label>
            <textarea
              {...register('medicalHistory')}
              rows={3}
              className="medical-input"
              placeholder="Relevant medical history, medications, allergies..."
            />
          </div>
        </div>

        {/* Step 2: Symptoms */}
        <div className="medical-card p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-neutral-900 dark:text-white">
              Symptom Analysis
            </h2>
            <button
              type="button"
              onClick={addSymptom}
              className="medical-button-secondary text-sm"
            >
              <PlusIcon className="h-4 w-4 mr-1" />
              Add Symptom
            </button>
          </div>

          <AnimatePresence>
            {fields.map((field, index) => (
              <motion.div
                key={field.id}
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="border border-neutral-200 dark:border-neutral-700 rounded-lg p-4 mb-4"
              >
                <div className="flex items-center justify-between mb-4">
                  <h4 className="font-medium text-neutral-900 dark:text-white">
                    Symptom {index + 1}
                  </h4>
                  {fields.length > 1 && (
                    <button
                      type="button"
                      onClick={() => remove(index)}
                      className="text-red-500 hover:text-red-700 p-1"
                    >
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1">
                      Symptom Name *
                    </label>
                    <input
                      {...register(`symptoms.${index}.name`)}
                      className="medical-input"
                      placeholder="e.g., chest pain"
                    />
                    {errors.symptoms?.[index]?.name && (
                      <p className="text-red-500 text-xs mt-1">
                        {errors.symptoms[index]?.name?.message}
                      </p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1">
                      Severity *
                    </label>
                    <select {...register(`symptoms.${index}.severity`)} className="medical-input">
                      <option value="mild">Mild</option>
                      <option value="moderate">Moderate</option>
                      <option value="severe">Severe</option>
                      <option value="critical">Critical</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1">
                      Duration *
                    </label>
                    <select {...register(`symptoms.${index}.duration`)} className="medical-input">
                      <option value="acute">Acute (&lt; 24h)</option>
                      <option value="subacute">Subacute (1-7 days)</option>
                      <option value="chronic">Chronic (&gt; 7 days)</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1">
                      Body Location
                    </label>
                    <input
                      {...register(`symptoms.${index}.bodyLocation`)}
                      className="medical-input"
                      placeholder="e.g., chest, abdomen"
                    />
                  </div>

                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1">
                      Description
                    </label>
                    <input
                      {...register(`symptoms.${index}.description`)}
                      className="medical-input"
                      placeholder="Detailed description of the symptom"
                    />
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>

        {/* Submit Button */}
        <div className="flex justify-center">
          <motion.button
            type="submit"
            disabled={isAnalyzing}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="medical-button text-lg px-8 py-3 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isAnalyzing ? (
              <>
                <LoadingSpinner size="sm" className="mr-2" />
                Analyzing Symptoms...
              </>
            ) : (
              <>
                <SparklesIcon className="h-5 w-5 mr-2" />
                Analyze with AI
              </>
            )}
          </motion.button>
        </div>
      </form>
    </motion.div>
  )
}
